Ansible Role: docker
====================

![Test workflow status](https://github.com/yabusygin/ansible-role-docker/workflows/test/badge.svg)
![Release workflow status](https://github.com/yabusygin/ansible-role-docker/workflows/release/badge.svg)

An Ansible role installing [Docker Engine][Engine] and
[Docker Compose][Compose] on Linux (Debian/Ubuntu).

[Engine]: https://docs.docker.com/install/
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

### Ansible Modules Dependencies ###

Dependencies of the following Ansible modules are installed by default:

*   [docker_container](https://docs.ansible.com/ansible/latest/modules/docker_container_module.html)
*   [docker_image](https://docs.ansible.com/ansible/latest/modules/docker_image_module.html)
*   [docker_network](https://docs.ansible.com/ansible/latest/modules/docker_network_module.html)
*   [docker_volume](https://docs.ansible.com/ansible/latest/modules/docker_volume_module.html)
*   [docker_compose](https://docs.ansible.com/ansible/latest/modules/docker_compose_module.html)
*   [docker_login](https://docs.ansible.com/ansible/latest/modules/docker_login_module.html)

To disable installation of Ansible module dependencies set
`docker_modules_dependencies_install` variable to `no`.

### Compose Binary ###

To install [Docker Compose binary][Compose Releases] set
`docker_compose_binary_install` variable to `yes`. The latest Compose version is
installed by default. Use `docker_compose_binary_version` variable to specify
the particular version to install. To change the default Compose executable
installation path (`/usr/bin/docker-compose`) override
`docker_compose_binary_path` variable value.

[Compose Releases]: https://github.com/docker/compose/releases

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
- hosts: production
  tasks:
    - import_role:
        name: yabusygin.docker
```

Customized setup:

```yaml
---
- hosts: production
  tasks:
    - import_role:
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
        docker_modules_dependencies_install: no
        docker_compose_binary_install: yes
        docker_compose_binary_version: 1.23.2
        docker_compose_binary_path: /home/user/.local/bin/docker-compose
```

License
-------

MIT

Author Information
------------------

Alexey Busygin \<yaabusygin@gmail.com\>
