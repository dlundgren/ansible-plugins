# Ansible lookup plugin for getting the first available file given a list of items and a template
# (c) 2015,2016 David Lundgren <dlundgren@syberisle.net>
#
# Given a list of items it will attempt to find a file in the regular list of paths that is similar to the name
#
# - name: Add SSH keys
#  authorized_key:
#    user: "{{ item.username }}"
#    state: present
#    key: "{{ lookup('file', item.pubkey) }} }}"
#    manage_dir: yes
#    path: '/home/{{ item.username }}/.ssh/authorized_keys'
#  with_available_file_from_items:
#    items: "{{ users }}"
#    name: files/ssh/keys/{{ item.username }}.pubkeys
#    key: pubkey
#
# This will look in the {role}/files/ssh/keys/, {playbook}/files/ssh/keys/ folders for the {username}.pubkeys file.
# If the file is not found then the user is not returned in the list of items to be used.

import os

from ansible import utils
from ansible import constants as C
from ansible.utils import template
from ansible.plugins.lookup import LookupBase

class LookupModule(LookupBase):
    def run(self, terms, variables=None, **kwargs):
        ret = []

        for item in terms['items']:
            content = self.resolve_available_file_path(template.template_from_string('', terms['name'], {'item':item}), variables)
            if content:
                item[terms['key']] = content
                ret.append(item)

        return ret

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

    def resolve_available_file_path(self, file, vars):
        ret = None

        for path in self.get_paths(vars):
            path = os.path.join(path, 'files', file)
            if os.path.exists(path):
                ret = path
                break

        return ret