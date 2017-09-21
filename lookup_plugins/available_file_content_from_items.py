# Ansible lookup plugin for getting the first available file
# (c) 2015,2016 David Lundgren <dlundgren@syberisle.net>

# For each item if the path exists along the regular paths then the first found entry will used.
#
# This will put the content of the found file into the items data
#
DOCUMENTATION = """
    author: David Lundgren
    lookup: available_file_content_from_items
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
from ansible.utils import template

# ansible 2.4
try:
    from ansible.plugins import get_plugin_class
    from ansible.parsing.plugin_docs import read_docstring

    # load the definitions
    dstring = read_docstring(__file__, verbose = False, ignore_errors = False)
    if dstring.get('doc', False):
        if 'options' in dstring['doc'] and isinstance(dstring['doc']['options'], dict):
            C.config.initialize_plugin_configuration_definitions('lookup', 'available_file_content_from_items', dstring['doc']['options'])
except:
    None

class LookupModule(LookupBase):
    def run(self, terms, variables=None, **kwargs):
        ret = []
        for item in terms['items']:
            content = self.load_file_content(template.template_from_string('', terms['name'], {'item':item}), variables)
            if content:
                item[terms['key']] = content;
                ret.append(item)

        return ret

    def load_file_content(self, file, vars):
        ret = None
        for path in self.get_paths(vars):
            path = os.path.join(path, 'files', file)
            if os.path.exists(path):
                with open (path, "r") as myfile:
                    ret = myfile.read()
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
            # Ansible 2.4
            lookupPaths = C.config.get_config_value('lookup_file_paths', None, 'lookup', 'available_file_content_from_items')
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

        unq = []
        [unq.append(i) for i in paths if not unq.count(i)]

        return unq