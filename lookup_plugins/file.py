# Ansible lookup plugin for getting the content of the file
# (c) 2015,2016 David Lundgren <dlundgren@syberisle.net>
#
# MIT License

# For each item will find the first file and return it's content
DOCUMENTATION = """
    author: David Lundgren
    lookup: file
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
import codecs

from ansible import utils
from ansible import constants as C
from ansible.errors import AnsibleError
from ansible.plugins.lookup import LookupBase

# ansible 2.4
try:
    from ansible.parsing.plugin_docs import read_docstring

    # load the definitions
    dstring = read_docstring(__file__, verbose = False, ignore_errors = False)
    if dstring.get('doc', False):
        if 'options' in dstring['doc'] and isinstance(dstring['doc']['options'], dict):
            C.config.initialize_plugin_configuration_definitions('lookup', 'file', dstring['doc']['options'])
except:
    None

class LookupModule(LookupBase):
    def run(self, terms, variables=None, **kwargs):
        for term in terms:
            for path in self.get_paths(variables):
                path = os.path.join(path, 'files', term)
                if os.path.exists(path):
                    return [codecs.open(path, encoding="utf8").read().rstrip()]
                    break
            else:
                raise AnsibleError("could not locate file in lookup: %s" % term)

    def get_paths(self, vars):
        paths = []
        basedir = self.get_basedir(vars)

        try:
            # Ansible 2.4
            lookupPaths = C.config.get_config_value('lookup_file_paths', None, 'lookup', 'file')
        except AttributeError:
            # Ansible 2.3
            lookupPaths = C.get_config(C.p, C.DEFAULTS, 'lookup_file_paths', None, [], value_type='list')
        except TypeError:
            # Ansible 2.2.x and below
            lookupPaths = C.get_config(C.p, C.DEFAULTS, 'lookup_file_paths', None, [], islist=True)

        for path in lookupPaths:
            path = utils.path.unfrackpath(path)
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