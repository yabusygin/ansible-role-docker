import os
import textwrap

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ["MOLECULE_INVENTORY_FILE"]
).get_hosts("instance")


def test_daemon_config(host):
    expect = textwrap.dedent(
        """\
        {
            "userns-remap": "default",
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


def test_user(host):
    assert host.user(name="dockremap").exists


def test_subuid(host):
    subuid_content = host.file(path="/etc/subuid").content_string
    subuid_entries = [
        tuple(line.split(":"))
        for line in subuid_content.splitlines()
    ]
    matches = [
        entry
        for entry in subuid_entries
        if entry[0] == "dockremap"
    ]
    assert len(matches) == 1
