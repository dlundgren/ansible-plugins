# Ansible lookup plugin for getting the first available file
# (c) 2015,2016 David Lundgren <dlundgren@syberisle.net>

# For each item if the path exists along the regular paths then the first found entry will be returned.
# This operates differently from the file or found-file plugins as it is not an error if the file is not found.

import os

from ansible import utils
from ansible import constants as C
from ansible.plugins.lookup import LookupBase

class LookupModule(LookupBase):
    def run(self, terms, variables=None, **kwargs):
        ret = []

        if isinstance(terms, basestring):
            terms = [terms]

        paths = self.get_paths(variables)
        for term in terms:
            for path in paths:
                path = os.path.abspath(path, 'files', term)
                if os.path.exists(path):
                    ret.append(path)
                    break

        return ret

    def get_paths(self, vars):
        paths = []
        basedir = self.get_basedir(vars)

        paths.append(self._loader.path_dwim(basedir))

        if '_original_file' in vars:
            paths.append(self._loader.path_dwim_relative(basedir, '', vars['_original_file']))

        if 'playbook_dir' in vars:
            paths.append(vars['playbook_dir'])

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

        unq = []
        [unq.append(i) for i in paths if not unq.count(i)]

        return unq