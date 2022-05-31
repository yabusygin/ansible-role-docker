Ansible Role: docker
====================

![Test workflow status](https://github.com/yabusygin/ansible-role-docker/workflows/test/badge.svg)
![Release workflow status](https://github.com/yabusygin/ansible-role-docker/workflows/release/badge.svg)

An Ansible role installing [Docker Engine][Engine] and
[Docker Compose][Compose] on Linux (Debian/Ubuntu).

[Engine]: https://docs.docker.com/engine/
[Compose]: https://docs.docker.com/compose/

Requirements
------------

None.

Role Variables
--------------

### Docker Daemon Configuration ###

The Docker daemon configuration file (`/etc/docker/daemon.json`) content may be
set explicitly with `docker_config` variable:

```yaml
docker_config:
  userns-remap: default
  insecure-registries:
    - registry.example.com:5000
```

The default configuration file content is following:

```json
{
    "log-driver": "json-file",
    "log-opts": {
        "max-size": "10m",
        "max-file": "3"
    }
}
```

### community.docker Modules Dependencies ###

Dependencies of [community.docker][Collection] modules are installed by default.
Set `docker_ansible_dependencies_install` to `no` to disable installation.

[Collection]: https://docs.ansible.com/ansible/latest/collections/community/docker/index.html

### Checking of Iptables Rules Managed by Docker ###

The role checks iptables rules added by Docker. If they are absent Docker daemon
is restarted. To disable this behaviour set `docker_iptables_check` variable
to `no`.

Dependencies
------------

None.

Example Playbook
----------------

Default setup:

```yaml
---
- name: "example #1"
  hosts: server
  tasks:
    - name: install Docker
      ansible.builtin.import_role:
        name: yabusygin.docker
```

Customized setup:

```yaml
---
- name: "example #2"
  hosts: server
  tasks:
    - name: install Docker
      ansible.builtin.import_role:
        name: yabusygin.docker
      vars:
        docker_config:
          userns-remap: default
          log-driver: json-file
          log-opts:
            max-size: 10m
            max-file: "3"
          insecure-registries:
            - registry.example.com:5000
        docker_ansible_dependencies_install: no
```

License
-------

MIT

Author Information
------------------

Alexey Busygin \<yaabusygin@gmail.com\>
