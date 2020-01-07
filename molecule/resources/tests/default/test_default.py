import os
import re
import textwrap

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
