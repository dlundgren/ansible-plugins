# Plugin :: lookup :: available_files

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