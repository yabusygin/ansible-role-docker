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
            "log-driver": "journald",
            "log-opts": {
                "tag": "{{.Name}}/{{.FullID}}",
                "env": "TEST1,TEST2"
            }
        }
        """
    )
    actual = host.file(path="/etc/docker/daemon.json").content_string
    assert expect == actual
