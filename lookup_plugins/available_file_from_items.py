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
DOCUMENTATION = """
    author: David Lundgren
    lookup: available_file_from_items
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

from ansible import utils
from ansible import constants as C
from ansible.plugins.lookup import LookupBase

# ansible 2.4
try:
    from ansible.parsing.plugin_docs import read_docstring

    # load the definitions
    dstring = read_docstring(__file__, verbose = False, ignore_errors = False)
    if dstring.get('doc', False):
        if 'options' in dstring['doc'] and isinstance(dstring['doc']['options'], dict):
            C.config.initialize_plugin_configuration_definitions('lookup', 'available_file_from_items', dstring['doc']['options'])
except:
    None

class LookupModule(LookupBase):
    def run(self, terms, variables=None, **kwargs):
        ret = []

        for item in terms['items']:
            self._templar.set_available_variables({'item':item})
            content = self.resolve_available_file_path(self._templar.template(terms['name'], preserve_trailing_newlines=True), variables)
            if content:
                item[terms['key']] = content
                ret.append(item)

        return ret

    def get_paths(self, vars):
        paths = []
        basedir = self.get_basedir(vars)

        try:
            # Ansible 2.4
            lookupPaths = C.config.get_config_value('lookup_file_paths', None, 'lookup', 'available_file_from_items')
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

    def resolve_available_file_path(self, file, vars):
        ret = None
        for path in self.get_paths(vars):
            path = os.path.join(path, 'files', file)
            if os.path.exists(path):
                ret = path
                break

        return ret