# Ansible lookup plugin for getting the first available file
# (c) 2015, David Lundgren <dlundgren@syberisle.net>

# For each item if the path exists along the regular paths then the first found entry will used.
#
# This will put the content of the found file into the items data
#

from ansible import utils, errors
from ansible.utils import template

import os
import codecs

class LookupModule(object):
    def __init__(self, basedir=None, **kwargs):
        self.basedir = basedir

    def run(self, terms, inject=None, **kwargs):
        ret = []

        playbookDir = None
        if 'playbook_dir' in inject:
            playbookDir = inject['playbook_dir']

        for item in terms['items']:
            content = self.loadFileContent(template.template_from_string('', terms['name'], {'item':item}), playbookDir)
            if content:
                item[terms['key']] = content;
                ret.append(item)

        return ret

    def loadFileContent(self, file, playbookDir):
        ret = None
        basedir_path = utils.path_dwim(self.basedir, file)
        playbook_path = None

        if playbookDir:
            playbook_path = os.path.join(playbookDir, file)

        for path in (basedir_path, playbook_path):
            path = os.path.abspath(path)
            if os.path.exists(path):
                with open (path, "r") as myfile:
                    ret = myfile.read()
                break

        return ret