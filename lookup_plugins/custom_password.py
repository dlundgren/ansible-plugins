from ansible import utils, errors
import os
import errno
from ansible import constants as C
from string import ascii_letters, digits
import string
import random


class LookupModule(object):

    LENGTH = 20

    def __init__(self, length=None, encrypt=None, basedir=None, **kwargs):
        self.basedir = basedir

    def random_salt(self):
        salt_chars = ascii_letters + digits + './'
        return utils.random_password(length=8, chars=salt_chars)

    def get_paths(self, inject):
        paths = []

        for path in C.get_config(C.p, C.DEFAULTS, 'lookup_file_paths', None, [], islist=True):
            path = os.path.join(utils.unfrackpath(path), 'files')
            if os.path.exists(path):
                paths.append(path)

        if 'playbook_dir' in inject:
            paths.append(inject['playbook_dir'])

        unq = []
        [unq.append(i) for i in paths if not unq.count(i)]

        return unq

    def run(self, terms, inject=None, **kwargs):

        terms = utils.listify_lookup_plugin_terms(terms, self.basedir, inject)

        ret = []

        for term in terms:
            # you can't have escaped spaces in yor pathname
            params = term.split()
            relpath = params[0]

            paramvals = {
                'length': LookupModule.LENGTH,
                'encrypt': None,
                'chars': ['ascii_letters','digits',".,:-_"],
            }

            # get non-default parameters if specified
            try:
                for param in params[1:]:
                    name, value = param.split('=')
                    assert(name in paramvals)
                    if name == 'length':
                        paramvals[name] = int(value)
                    elif name == 'chars':
                        use_chars=[]
                        if ",," in value:
                            use_chars.append(',')
                        use_chars.extend(value.replace(',,',',').split(','))
                        paramvals['chars'] = use_chars
                    else:
                        paramvals[name] = value
            except (ValueError, AssertionError), e:
                raise errors.AnsibleError(e)

            length  = paramvals['length']
            encrypt = paramvals['encrypt']
            use_chars = paramvals['chars']

            # get password or create it if file doesn't exist
            paths = self.get_paths(inject)
            foundPath = None
            for path in paths:
                path = utils.path_dwim(path, relpath)
                if os.path.exists(path):
                    foundPath = path
                    break

            if not foundPath:
                path = paths.pop()
                if not os.path.exists(path):
                    pathdir = os.path.dirname(path)
                    if not os.path.isdir(pathdir):
                        try:
                            os.makedirs(pathdir, mode=0700)
                        except OSError, e:
                            raise errors.AnsibleError("cannot create the path for the password lookup: %s (error was %s)" % (pathdir, str(e)))

                    chars = "".join([getattr(string,c,c) for c in use_chars]).replace('"','').replace("'",'')
                    password = ''.join(random.choice(chars) for _ in range(length))

                    if encrypt is not None:
                        salt = self.random_salt()
                        content = '%s salt=%s' % (password, salt)
                    else:
                        content = password
                    with open(path, 'w') as f:
                        os.chmod(path, 0600)
                        f.write(content + '\n')
            else:
                content = open(path).read().rstrip()
                sep = content.find(' ')

                if sep >= 0:
                    password = content[:sep]
                    salt = content[sep+1:].split('=')[1]
                else:
                    password = content
                    salt = None

                # crypt requested, add salt if missing
                if (encrypt is not None and not salt):
                    salt = self.random_salt()
                    content = '%s salt=%s' % (password, salt)
                    with open(path, 'w') as f:
                        os.chmod(path, 0600)
                        f.write(content + '\n')
                # crypt not requested, remove salt if present
                elif (encrypt is None and salt):
                    with open(path, 'w') as f:
                        os.chmod(path, 0600)
                        f.write(password + '\n')

            if encrypt:
                password = utils.do_encrypt(password, encrypt, salt=salt)

            ret.append(password)

        return ret