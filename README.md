Ansible Role: docker
====================

![Test workflow status](https://github.com/yabusygin/ansible-role-docker/workflows/test/badge.svg)

An Ansible role installing [Docker CE][Engine] and [Docker Compose][Compose]
on Linux (Debian/Ubuntu).

[Engine]: https://docs.docker.com/install/
[Compose]: https://docs.docker.com/compose/

Requirements
------------

None.

Role Variables
--------------

All variables are optional. An example of variable usage provided
in *Example Playbook* section.

### Logging ###

By default the following configuration is applied:

```json
{
    "log-driver": "json-file",
    "log-opts": {
        "max-size": "10m",
        "max-file": "3"
    }
}
```

`docker_log_driver` variable could be used to override the default logging
driver. Custom logging options could be specified with `docker_log_options`
variable.

### Non-root Users ###

A list of [non-root Docker users][Non-Root User] is set with `docker_users` variable.

[Non-Root User]: https://docs.docker.com/install/linux/linux-postinstall/#manage-docker-as-a-non-root-user

### User Namespace Remapping ###

To enable [user namespace remapping feature][userns-remap] set
`docker_userns_remap_enable` variable to `yes`. Docker creates `dockremap` user
and group for this purpose by default. To speficy custom user and (optionally)
group use `docker_userns_remap_user` and `docker_userns_remap_group` variables
accordingly.

[userns-remap]: https://docs.docker.com/engine/security/userns-remap/

### Insecure Registries ###

[Insecure (using HTTP transport) registries][Insecure Registries] are specified
with `docker_insecure_registries` variable.

[Insecure Registries]: https://docs.docker.com/registry/insecure/

### Custom Docker Daemon config ###

Docker Daemon config (`/etc/docker/daemon.json`) content could be set explicitly
with `docker_config` variable. The following two variable sets are equivalent:

```yaml
---
docker_userns_remap_enable: yes
```

```yaml
---
docker_config:
  userns-remap: "default"
  log-driver: json-file
  log-opts:
    max-size: 10m
    max-file: "3"
```

### Ansible Modules Dependencies ###

Dependencies of the following Ansible modules are installed by default:

*   [docker_container](https://docs.ansible.com/ansible/latest/modules/docker_container_module.html)
*   [docker_image](https://docs.ansible.com/ansible/latest/modules/docker_image_module.html)
*   [docker_network](https://docs.ansible.com/ansible/latest/modules/docker_network_module.html)
*   [docker_volume](https://docs.ansible.com/ansible/latest/modules/docker_volume_module.html)
*   [docker_compose](https://docs.ansible.com/ansible/latest/modules/docker_compose_module.html)
*   [docker_login](https://docs.ansible.com/ansible/latest/modules/docker_login_module.html)

[Docker Compose Python package][docker-compose] is also installed.

To disable installation of Ansible module dependencies set
`docker_modules_dependencies_install` variable to `no`.

[docker-compose]: https://pypi.org/project/docker-compose/

### Compose Binary ###

To install [Docker Compose binary][Compose Releases] set
`docker_compose_binary_install` variable to `yes`. Note that Docker Compose
Python package is already installed in default configuration (see
*Ansible Modules Dependencies* section).

The latest Compose version is installed by default. Use
`docker_compose_binary_version` variable to specify the particular version
to install. To change the default Compose executable installation path
(`/usr/bin/docker-compose`) override `docker_compose_binary_path` variable
value.

[Compose Releases]: https://github.com/docker/compose/releases

Dependencies
------------

None.

Example Playbook
----------------

```yaml
---
- hosts: production
  roles:
    - role: yabusygin.docker
  vars:
    docker_insecure_registries:
      - "registry1.example.com:5001"
      - "registry2.example.com:5002"

    docker_log_driver: journald
    docker_log_options:
      - name: tag
        value: "{% raw %}{{.Name}}/{{.FullID}}{% endraw %}"
      - name: env
        value:
          - LOCATION
          - SERVICE_VERSION

    docker_userns_remap_enable: yes
    docker_userns_remap_user: userns-remap-user
    docker_userns_remap_group: userns-remap-group

    docker_users:
      - docker-admin-1
      - docker-admin-2

    docker_modules_dependencies_install: no

    docker_compose_binary_install: yes
    docker_compose_binary_version: 1.23.2
    docker_compose_binary_path: /usr/local/bin/docker-compose
```

License
-------

MIT

Author Information
------------------

Alexey Busygin \<busygin.contact@yandex.ru\>
