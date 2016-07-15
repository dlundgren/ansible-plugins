# Ansible lookup plugin for getting available items based on a key existing in the item
# (c) 2015, David Lundgren <dlundgren@syberisle.net>

# For each item of the value(array) of each item if the key exists then the item will be returned
#
#vars/users.yml
# users:
#   - username: dlundgren
#     password: encrypted-password
#   - username: flogrow
#
# roles/user/tasks/main.yml
# - name: Install users
#   user:
#     username: "{{ item.username }}"
#     password: "{{ item.password }}"
#     state: present
#   with_available_items:
#     items: "{{ users }}"
#     key: password
#

from ansible.plugins.lookup import LookupBase

class LookupModule(LookupBase):
    def run(self, terms, variables=None, **kwargs):
        ret = []

        key = terms['key']
        for item in terms['items']:
            if key in item:
                ret.append(item)

        return ret