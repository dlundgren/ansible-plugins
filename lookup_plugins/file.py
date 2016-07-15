# Ansible lookup plugin for getting the content of the file
# (c) 2015, David Lundgren <dlundgren@syberisle.net>
#
# MIT License

# For each item will find the first file and return it's content

import os
import codecs

from ansible import utils
from ansible import constants as C
from ansible.errors import AnsibleError
from ansible.plugins.lookup import LookupBase

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

        for path in C.get_config(C.p, C.DEFAULTS, 'lookup_file_paths', None, [], islist=True):
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