import os

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ["MOLECULE_INVENTORY_FILE"]
).get_hosts("instance")


def test_iptables_filter(host):
    cmd = host.run_expect(
        expected=[0],
        command="iptables --table filter --list-rules",
    )
    stdout_lines = cmd.stdout.splitlines()
    assert "-N DOCKER" in stdout_lines


def test_iptables_nat(host):
    cmd = host.run_expect(
        expected=[0],
        command="iptables --table nat --list-rules",
    )
    stdout_lines = cmd.stdout.splitlines()
    assert "-N DOCKER" in stdout_lines
