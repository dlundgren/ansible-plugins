# Module :: sasldb

Add or remove Postfix configuration

## Requirements

- saslpasswd2
- sasldblistusers2

## Synopsis

- Modifies a sasldb file

## Parameters

| Parameter | Choices/Defaults | Comments |
| :-------- | :--------------- | :----- |
| dest      | | The file to modify |
| name      | | Name of the user to mange |
| password  | | Required when `state=present` |
| realm     | Default: `hostname` | Name of the realm to use |
| state     | **Choices**: <ul><li>absent</li><li>**present**</li></ul> | Whether the use should be present or absent |

## Examples

```yaml
- sasldb:
    dest: /var/spool/postfix/etc/sasldb2
    name: test
    realm: relay.example.com
    password: testpass
```