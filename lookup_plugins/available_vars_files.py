# Ansible lookup plugin for getting the first available file
# (c) 2015,2016 David Lundgren <dlundgren@syberisle.net>

# For each item if the path exists along the regular paths then the first found entry will be returned.
# This operates differently from the file or found-file plugins as it is not an error if the file is not found.

import os
import codecs

from ansible import utils
from ansible import constants as C
from ansible.errors import AnsibleError
from ansible.plugins.lookup import LookupBase

class LookupModule(LookupBase):
    def run(self, terms, variables=None, **kwargs):
        ret = []

        if isinstance(terms, basestring):
            terms = [terms]

        paths = self.get_paths(inject)
        for term in terms:
            for path in paths:
                path = os.path.abspath(os.path.join(path, "vars", term))
                if os.path.exists(path):
                    ret.append(path)
                    break

        return ret

    def get_paths(self, inject):
        paths = []

        for path in C.get_config(C.p, C.DEFAULTS, 'lookup_vars_paths', None, [], islist=True):
            path = utils.unfrackpath(path)
            if os.path.exists(path):
                paths.append(path)

        if '_original_file' in inject:
            paths.append(utils.path_dwim_relative(inject['_original_file'], '', None, self.basedir, check=False))

        if 'playbook_dir' in inject and paths[0] != inject['playbook_dir']:
            paths.append(inject['playbook_dir'])

        paths.append(utils.path_dwim(self.basedir, ''))

        return paths

