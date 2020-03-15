[![Build Status](https://travis-ci.org/stdevel/ansible-uyuni.svg?branch=master)](https://travis-ci.org/stdevel/ansible-mosquitto)

# mosquitto

This role installs and configures the MQTT broker [Eclipse mosquitto](http://mosquitto.org).

## Requirements

This system requires an internet connection and a supported Linux distribution:
- Enterprise Linux 7
  - Red Hat Enterprise Linux
  - CentOS
  - Scientific Linux
  - Oracle Linux
- Debian
  - Buster
  - stretch

## Role Variables

| Variable | Default | Description |
| -------- | ------- | ----------- |
| `configure_epel` | `true` | Configures the [EPEL repository](https://fedoraproject.org/wiki/EPEL) on EL7 |
| `configure_acl` | `true` | Configures ACLs |
| `allow_anonymous` | `false` | Allows/forbids anonymous access |
| `user_topics` | `[{user: admin, password: 23cu53, global_readwrite: true}]` | Configures users and topics (*see also ACLs*) |

### ACLs

To configure ACLs, `user_topics` needs to be assigned to a list with at least one `user` object with the following settings:

| Variable | Description |
| -------- | ----------- |
| `password` | Password |
| `global_read` | Global read access to all topics |
| `global_write` | Global write access to all topics |
| `global_readwrite` | Global read/write access to all topics |
| `topics` | List of topics user has (un)limited access to |

Please only specify **one** of `global_read`, `global_write` or `global_readwrite`.

To assign topics, assign a list to the `topics` element - the following settings are possible:

| Variable | Description |
| -------- | ----------- |
| `name` | Topic name |
| `type` | Access type (*`read`, `write`, `readwrite`*) |

Refer to the following example:
```yml
user_topics:
  - user: pinkepank
    password: trololo
    global_readwrite: true
  - user: giertz
    password: chad
    topics:
    global_read: true
  - user: bb8
    password: bleepbleep
    topics:
      - name: r2d2/target
        type: read
      - name: falcon/power
        type: write
      - name: luke/status
        type: readwrite
```
- User `pinkepank` has global read/write access
- User `giertz` has global read access
- User `bb8` has access to various topics
  - Read access to `r2d2/target`
  - Write access to `falcon/power`
  - Read/write access to `luke/status`

## Dependencies

No dependencies.

## Example Playbook

Refer to the following example:

```
    - hosts: servers
      roles:
         - stdevel.mosquitto
```

Set variables if required, e.g.:
```
---
- hosts: bee.giertz.loc
  remote_user: root
  roles:
    - role: stdevel.mosquitto
      user_topics:
        - user: pinkepank
          password: trololo
          global_readwrite: true
```

License
-------

BSD

Author Information
------------------

Christian Stankowic (info@cstan.io)
