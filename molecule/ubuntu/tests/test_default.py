"""Test role."""

import os

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ["MOLECULE_INVENTORY_FILE"]
).get_hosts("instance")


def test_hello_world(host):
    """Run hello-world container."""
    cmd = host.run_test(command="docker container run hello-world")

    assert "Hello from Docker!" in cmd.stdout
