# Module :: etc_hosts

Adds or removes entries from an /etc/hosts formatted file

## Synopsis

- Modifies an /etc/hosts formatted file

## Parameters

| Parameter | Choices/Defaults | Comments |
| :-------- | :--------------- | :----- |
| address   | | IP Adress of the host |
| file      | **Default**: /etc/hosts | 
| name      | | Name of the host |  
| state     | **Choices**: <ul><li>absent</li><li>**present**</li></ul> | Whether or not the host should be associated to the address |

## Examples

```yaml
# remove localhost pairing (not usually recommended)
- etc_hosts:
    name: localhost
    value: 127.0.0.1
    state: absent

- etc_hosts:
    name: "{{ item.key }}"
    value: "{{ item.value }}"
  with_dict:
    host1: 127.0.2.1
    host2: 127.0.2.3

# Edit a different file
- etc_hosts:
    name: "{{ item.key }}"
    value: "{{ item.value }}"
    file: /etc/generated/hosts.custom
  with_dict:
    host1: 127.0.2.1
    host2: 127.0.2.3
```