# Module :: postconf

Add or remove postfix configuration

This uses Postfix's postconf binary to make changes to the configuration

```yaml
- postconf:
    name: relayhost
    value: "relay.example.com"
```

## Defaults

```yaml
state: present
```
