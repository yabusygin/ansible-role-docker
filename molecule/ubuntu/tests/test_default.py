"""Test role."""

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
