"""Test role."""

import json
import os
import re

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ["MOLECULE_INVENTORY_FILE"]
).get_hosts("instance")


def test_hello_world(host):
    """Run hello-world container."""
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
    config = json.loads(
        s=host.file(path="/etc/docker/daemon.json").content_string,
    )
    assert set(config.keys()) == {"log-driver", "log-opts"}
    assert config["log-driver"] == "json-file"
    assert set(config["log-opts"]) == {"max-size", "max-file"}
    assert config["log-opts"]["max-size"] == "10m"
    assert config["log-opts"]["max-file"] == "3"
