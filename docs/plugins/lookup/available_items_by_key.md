# Plugin :: lookup :: available_items_by_key

Given a list of items it will return those items that have the given key.

## Usage
 
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