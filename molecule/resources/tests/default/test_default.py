import os
import re
import textwrap

import requests

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


def test_compose_version(host):
    cmd = host.run_test(command="docker-compose version --short")
    current_version = cmd.stdout.strip()

    response = requests.get(
        url="https://api.github.com/repos/docker/compose/releases/latest",
    )
    latest_version = response.json()["name"]

    assert current_version == latest_version
