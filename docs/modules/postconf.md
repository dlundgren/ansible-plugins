# Module :: postconf

Add or remove Postfix configuration

## Synopsis

- Add or remove postfix configuration
- Uses postconf

## Parameters

| Parameter | Choices/Defaults | Comments |
| :-------- | :--------------- | :----- |
| name      | | Name of the configuration value to manage |
| state     | **Choices**: <ul><li>absent</li><li>**present**</li></ul> | Whether the var should be present or absent |
| value     | | Required when `state=present` |

## Examples

```yaml
- postconf:
    name: relayhost
    value: "relay.example.com"

- postconf:
    name: "{{ item.name }}"
    value: "{{ item.value }}"
  with_items:
    - name: inet_interfaces
      value: all
    - name: inet_protocols
      value: all
```