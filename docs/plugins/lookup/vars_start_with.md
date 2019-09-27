# Plugins :: lookup :: vars_start_with

Lookup templated value of variables that start with a prefix.

```yaml
packages_group: "{{ lookup('vars_start_with', 'packages_group_', wantlist=True) | default([]) }}"
packages_no_php: "{{ lookup('vars_start_with', 'packages_group_', '!packages_group_php', wantlist=True) | default([]) }}"

packages_group_web:
  - nginx
packages_group_php:
  - php-cli
```

Results:
```yaml
packages_group:
  - nginx
  - php-cli
packages_no_php:
  - nginx
```

This allows you to separate variables in to groups, and then coalesce them in to a global variable. This is useful when
you need to specify different packages for different groups, but only want to deal with using one group_var to install
all necessary packages.