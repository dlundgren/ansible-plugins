# Ansible lookup plugin for getting the content of the first available file
# (c) 2015,2016 David Lundgren <dlundgren@syberisle.net>
#
# MIT License

# This will return a list of files that found out of those passed in

import os

from ansible import utils
from ansible import constants as C
from ansible.plugins.lookup import LookupBase

class LookupModule(LookupBase):

    def run(self, terms, variables=None, **kwargs):
        ret = []

        if not isinstance(terms, list):
            terms = [terms]

        for term in terms:
            for path in self.get_paths(variables):
                path = os.path.join(path, 'files', term)
                if os.path.exists(path):
                    ret.append(path)
                    break

        return ret

    def get_paths(self, vars):
        paths = []
        basedir = self.get_basedir(vars)
        try:
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
