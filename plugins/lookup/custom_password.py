# (c) 2012, Daniel Hokka Zakrisson <daniel@hozac.com>
# (c) 2013, Javier Candeira <javier@candeira.com>
# (c) 2013, Maykel Moya <mmoya@speedyrails.com>
# (c) 2016, David Lundgren <dlundgren@syberisle.net>
#
# This file is part of Ansible
#
# Ansible is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Ansible is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Ansible.  If not, see <http://www.gnu.org/licenses/>.
#
# MODIFIED TO ALLOW CUSTOM PATHS
#
DOCUMENTATION = """
    author: David Lundgren
    lookup: custom_password
    options:
        lookup_file_paths:
            type: list
            default: []
            ini:
                - key: lookup_file_paths
                  section: defaults
            yaml:
                key: defaults.lookup_file_paths
"""
import os
from string import ascii_letters, digits
import string
import random

from ansible import utils
from ansible import constants as C
from ansible.errors import AnsibleError
from ansible.plugins.lookup import LookupBase
from ansible.parsing.splitter import parse_kv

# ansible 2.4
try:
    from ansible.parsing.plugin_docs import read_docstring

    # load the definitions
    dstring = read_docstring(__file__.replace('.pyc', '.py'), verbose = False, ignore_errors = False)
    if dstring.get('doc', False):
        if 'options' in dstring['doc'] and isinstance(dstring['doc']['options'], dict):
            C.config.initialize_plugin_configuration_definitions('lookup', 'custom_password', dstring['doc']['options'])
except:
    None

DEFAULT_LENGTH = 20
VALID_PARAMS = frozenset(('length', 'encrypt', 'chars'))

def _parse_parameters(term):
    # Hacky parsing of params
    # See https://github.com/ansible/ansible-modules-core/issues/1968#issuecomment-136842156
    # and the first_found lookup For how we want to fix this later
    first_split = term.split(' ', 1)
    if len(first_split) <= 1:
        # Only a single argument given, therefore it's a path
        relpath = term
        params = dict()
    else:
        relpath = first_split[0]
        params = parse_kv(first_split[1])
        if '_raw_params' in params:
            # Spaces in the path?
            relpath = ' '.join((relpath, params['_raw_params']))
            del params['_raw_params']

            # Check that we parsed the params correctly
            if not term.startswith(relpath):
                # Likely, the user had a non parameter following a parameter.
                # Reject this as a user typo
                raise AnsibleError('Unrecognized value after key=value parameters given to password lookup')
        # No _raw_params means we already found the complete path when
        # we split it initially

    # Check for invalid parameters.  Probably a user typo
    invalid_params = frozenset(params.keys()).difference(VALID_PARAMS)
    if invalid_params:
        raise AnsibleError('Unrecognized parameter(s) given to password lookup: %s' % ', '.join(invalid_params))

    # Set defaults
    params['length'] = int(params.get('length', DEFAULT_LENGTH))
    params['encrypt'] = params.get('encrypt', None)

    params['chars'] = params.get('chars', None)
    if params['chars']:
        tmp_chars = []
        if ',,' in params['chars']:
            tmp_chars.append(u',')
        tmp_chars.extend(c for c in params['chars'].replace(',,', ',').split(',') if c)
        params['chars'] = tmp_chars
    else:
        # Default chars for password
        params['chars'] = ['ascii_letters', 'digits', ".,:-_"]

    return relpath, params

class LookupModule(LookupBase):
    def run(self, terms, variables=None, **kwargs):
        ret = []

        for term in terms:
            relpath, params = _parse_parameters(term)

            # get password or create it if file doesn't exist
            paths = self.get_paths(variables)
            foundPath = None
            for path in paths:
                path = os.path.join(path, relpath)
                if os.path.exists(path):
                    foundPath = path
                    break

            path = foundPath
            if not os.path.exists(path):
                pathdir = os.path.dirname(path)
                if not os.path.isdir(pathdir):
                    try:
                        os.makedirs(pathdir, mode=0o700)
                    except OSError, e:
                        raise AnsibleError("cannot create the path for the password lookup: %s (error was %s)" % (pathdir, str(e)))

                chars = "".join([getattr(string,c,c) for c in params['use_chars']]).replace('"','').replace("'",'')
                password = ''.join(random.choice(chars) for _ in range(params['length']))

                if params['encrypt'] is not None:
                    salt = self.random_salt()
                    content = '%s salt=%s' % (password, salt)
                else:
                    content = password
                with open(path, 'w') as f:
                    os.chmod(path, 0o600)
                    f.write(content + '\n')
            else:
                content = open(path).read().rstrip()
                password = content
                salt = None

                try:
                    sep = content.rindex(' salt=')
                except ValueError:
                    # No salt
                    pass
                else:
                    salt = password[sep + len(' salt='):]
                    password = content[:sep]

                # crypt requested, add salt if missing
                if params['encrypt'] is not None and salt is None:
                    # crypt requested, add salt if missing
                    salt = self.random_salt()
                    content = '%s salt=%s' % (password, salt)
                    with open(path, 'w') as f:
                        os.chmod(path, 0o600)
                        f.write(content + '\n')
                elif params['encrypt'] is None and salt:
                    with open(path, 'w') as f:
                        os.chmod(path, 0o600)
                        f.write(password + '\n')

            if params['encrypt']:
                password = utils.do_encrypt(password, params['encrypt'], salt=salt)



            ret.append(password)

        return ret


    def random_salt(self):
        salt_chars = ascii_letters + digits + './'
        return utils.random_password(length=8, chars=salt_chars)

    def get_paths(self, vars):
        paths = []
        basedir = self.get_basedir(vars)
        try:
            # Ansible 2.4
            lookupPaths = C.config.get_config_value('lookup_file_paths', None, 'lookup', 'custom_password')
        except AttributeError:
            # Ansible 2.3
            lookupPaths = C.get_config(C.p, C.DEFAULTS, 'lookup_file_paths', None, [], value_type='list')
        except TypeError:
            # Ansible 2.2.x and below
            lookupPaths = C.get_config(C.p, C.DEFAULTS, 'lookup_file_paths', None, [], islist=True)

        for path in lookupPaths:
            path = os.path.join(utils.path.unfrackpath(path), 'files')
            if os.path.exists(path):
                paths.append(path)

        if '_original_file' in vars:
            paths.append(self._loader.path_dwim_relative(basedir, '', vars['_original_file']))

        if 'playbook_dir' in vars:
            paths.append(vars['playbook_dir'])

        paths.append(self._loader.path_dwim(basedir))

        unq = []
        [unq.append(i) for i in paths if not unq.count(i)]

        return unq