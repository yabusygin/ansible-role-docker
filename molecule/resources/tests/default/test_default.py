import os
import re
import textwrap

import packaging.version

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ["MOLECULE_INVENTORY_FILE"]
).get_hosts("instance")


def test_hello_world_container(host):
    cmd = host.run_test(command="docker container run hello-world")
    assert "Hello from Docker!" in cmd.stdout


def test_docker_group_members(host):
    content = host.file(path="/etc/group").content_string
    match = re.search(
        pattern=r"^docker:x:\d+:$",
        string=content,
        flags=re.MULTILINE,
    )
    assert match


def test_daemon_config(host):
    expect = textwrap.dedent(
        """\
        {
            "log-driver": "json-file",
            "log-opts": {
                "max-size": "10m",
                "max-file": "3"
            }
        }
        """
    )
    actual = host.file(path="/etc/docker/daemon.json").content_string
    assert expect == actual


def test_ansible_modules_dependencies(host):
    packages = host.pip_package.get_packages(pip_path="pip3")

    assert "docker" in packages
    min_version = packaging.version.Version(version="1.10.0")
    installed_version = packaging.version.parse(
        version=packages["docker"]["version"],
    )
    assert installed_version >= min_version

    assert "PyYAML" in packages
    min_version = packaging.version.Version(version="3.11")
    installed_version = packaging.version.parse(
        version=packages["PyYAML"]["version"],
    )
    assert installed_version >= min_version

    assert "docker-compose" in packages
    min_version = packaging.version.Version(version="1.7.0")
    installed_version = packaging.version.parse(
        version=packages["docker-compose"]["version"],
    )
    assert installed_version >= min_version
