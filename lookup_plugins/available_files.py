# Ansible lookup plugin for getting the first available file
# (c) 2015, David Lundgren <dlundgren@syberisle.net>

# For each item if the path exists along the regular paths then the first found entry will be returned.
# This operates differently from the file or found-file plugins as it is not an error if the file is not found.

from ansible import utils, errors
import os
import codecs

class LookupModule(object):
    def __init__(self, basedir=None, **kwargs):
        self.basedir = basedir

    def run(self, terms, inject=None, **kwargs):
        ret = []

        if isinstance(terms, basestring):
            terms = [terms]

        for term in terms:
            basedir_path = utils.path_dwim(self.basedir, term)
            relative_path = None
            playbook_path = None

            # Special handling of the file lookup, used primarily when the
            # lookup is done from a role. If the file isn't found in the
            # basedir of the current file, use dwim_relative to look in the
            # role/files/ directory, and finally the playbook directory
            # itself (which will be relative to the current working dir)
            if '_original_file' in inject:
                relative_path = utils.path_dwim_relative(inject['_original_file'], 'files', term, self.basedir, check=False)
            if 'playbook_dir' in inject:
                playbook_path = os.path.join(inject['playbook_dir'], term)

            for path in (basedir_path, relative_path, playbook_path):
                path = os.path.abspath(path)
                if os.path.exists(path):
                    ret.append(path)
                    break


        return ret