# ansible-plugins

Custom modules for ansible.

This repository contains plugins that override file, first_found, found_files, and vars_files plugins with 
ones that allow to look int custom locations

You can control this by setting lookup_file_paths or lookup_vars_paths in your ansible.cfg

# Lookup plugins

### available_file_content

Use this when you need the content out of the first available file in a list.

### available_file_content_from_items

This acts similarly to available_file_content only inserts the content into the item when found

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
    name: files/ssh/keys/{{ item.username }}.pubkeys
    key: pubkey
```

This will look in the {role}/files/ssh/keys/, {playbook}/files/ssh/keys/ folders for the {username}.pubkeys file.

If the file is not found then the user is not returned in the list of items to be used, otherwise the item.pubkey is
filled with the content of the given file

### available_file_from_items

Given a list of items it will attempt to find a file in the regular list of paths that is similar to the name

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
    name: files/ssh/keys/{{ item.username }}.pubkeys
    key: pubkey
```

This will look in the {role}/files/ssh/keys/, {playbook}/files/ssh/keys/ folders for the {username}.pubkeys file.

If the file is not found then the user is not returned in the list of items to be used.

### available_files

Given a list of files it will find the first available file.

```yaml
- name: Include application variables
  include_vars: "{{ item }}"
  with_available_files:
    - vars/common/myapp.yml
    - vars/apps/myapp/global.yml
```

The first available file will be utilized. It will search the {role}/files/ssh/keys/, {playbook}/files/ssh/keys/
folders to find that file.

### available_items_with_key

Given a list of items it will return those items that have the given key.

#### arguments
 
vars/users.yml
```yaml
users:
  - username: dlundgren
    password: encrypted-password
  - username: flogrow
```
roles/user/tasks/main.yml
```yaml
- name: Install users
  user:
    username: "{{ item.username }}"
    password: "{{ item.password }}"
    state: present
  with_available_items_by_key:
    items: "{{ users }}"
    key: password
```