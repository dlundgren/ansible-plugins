# ansible-plugins

Custom plugins and modules for Ansible 2, and Python 3.

You can find the Ansible 1.x versions of these modules in the [ansible-1.x branch](https://github.com/dlundgren/ansible-plugins/tree/ansible-1.x)
You can find the Ansible 2.x and Python 2 versions of these modules in the [python-2 branch](https://github.com/dlundgren/ansible-plugins/tree/python-2)

This repository contains plugins that override file, first_found, found_files, and vars_files plugins with 
ones that allow to look int custom locations.

You can control this by setting lookup_file_paths or lookup_vars_paths in your ansible.cfg

# Documentation

## Modules

- [etc_hosts](docs/modules/etc_hosts.md)
- [postconf](docs/modules/postconf.md)
- [sasldb](docs/modules/sasldb.md)

## Plugins

- Lookup
  - [available_file_content_from_items](docs/plugins/lookup/available_file_content_from_items.md)
  - [available_file_from_items](docs/plugins/lookup/available_file_from_items.md)
  - [available_files](docs/plugins/lookup/available_files.md)
  - [available_items_by_key](docs/plugins/lookup/available_items_by_key.md)
  - [available_vars_files](docs/plugins/lookup/available_vars_files.md)
  - [custom_password](docs/plugins/lookup/custom_password.md)
  - [vars_dict_start_with](docs/plugins/lookup/vars_dict_start_with.md)
  - [vars_start_with](docs/plugins/lookup/vars_start_with.md)
- Lookup (overridden)
  - [file](docs/plugins/lookup/overridden.md)
  - [first_found](docs/plugins/lookup/overridden.md)
  - [found_files](docs/plugins/lookup/overridden.md)
  - [vars_files](docs/plugins/lookup/overridden.md)
- Callback
  - [updates_tracker](docs/plugins/callback-updates_tracker.md) 

# Lookup plugins

### available_file_content


