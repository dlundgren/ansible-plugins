# Plugin :: lookup :: available_file_content_from_items

This acts similarly to available_file_content only inserts the content into the item when found

**NOTE:** The way you add template data in the `name` field has changed in Ansible 2.x. You now have to escape the {{ and }}
```yaml
- name: Add SSH keys
  authorized_key:
    user: "{{ item.username }}"
    state: present
    key: "{{ lookup('file', item.pubkey) }} }}"
    manage_dir: yes
    path: '/home/{{ item.username }}/.ssh/authorized_keys'
  with_available_file_from_items:
    items: "{{ users }}"
    name: files/ssh/keys/{{ '{{' }} item.username {{ '}}' }}.pubkeys
    key: pubkey
```

This will look in the {role}/files/ssh/keys/, {playbook}/files/ssh/keys/ folders for the {username}.pubkeys file.

If the file is not found then the user is not returned in the list of items to be used, otherwise the item.pubkey is
filled with the content of the given file
