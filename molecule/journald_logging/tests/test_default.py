from json import loads
from os import environ

from testinfra.utils.ansible_runner import AnsibleRunner

_runner = AnsibleRunner(environ["MOLECULE_INVENTORY_FILE"])
testinfra_hosts = _runner.get_hosts("instance")


def test_journalctl(host):
    args = (
        "docker", "container", "run",
        "--rm",
        "--name=say-hello",
        "--env=TEST1=foo",
        "--env=TEST2=bar",
        "hello-world",
    )
    host.run_test(command=" ".join(args))
    args = (
        "journalctl",
        "--output=json",
        "--no-pager",
        "CONTAINER_NAME=say-hello",
    )
    cmd = host.run_test(command=" ".join(args))
    log_lines = cmd.stdout.splitlines()
    assert len(log_lines) > 0

    log_entries = [
        loads(s=line)
        for line in log_lines
    ]
    matches = [
        entry
        for entry in log_entries
        if entry["MESSAGE"] == "Hello from Docker!"
    ]
    assert len(matches) > 0

    log_entry = matches[-1]
    expect_tag = "say-hello/" + log_entry["CONTAINER_ID_FULL"]
    assert log_entry["CONTAINER_TAG"] == expect_tag
    assert log_entry["SYSLOG_IDENTIFIER"] == expect_tag
    assert log_entry["TEST1"] == "foo"
    assert log_entry["TEST2"] == "bar"
