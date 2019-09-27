# Plugins :: lookup :: vars_dict_start_with

Lookup templated value of variables that start with a prefix, and combine them as part of a dictionary

```yaml
test_dict: "{{ lookup('vars_start_with', 'test_dict_') | default([]) }}"
test_no_where: "{{ lookup('vars_start_with', 'test_dict_', '!test_dict_somewhere') | default([]) }}"
test_dict_something:
  something:
    - some where
test_dict_somewhere:
  somewhere:
    - some thing
```

Result when `test_dict` is used:
```yaml
test_dict:
  something:
    - some where
  somewhere:
    - some thing
test_no_where:
  something:
    - some where
```

This allows you to separate variables in group_vars, and then coalesce them in to a global variable.