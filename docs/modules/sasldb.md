# Module :: sasldb

Interact with sasldb files

This uses saslpasswd2 and sasldblistusers2 to change users in a sasl file

```yaml
- sasldb:
    dest: /var/spool/postfix/etc/sasldb2
    name: test
    realm: relay.example.com
    password: testpass
```

#### Defaults

```yaml
dest: /etc/sasldb2
realm: <hostname>
state: present
```