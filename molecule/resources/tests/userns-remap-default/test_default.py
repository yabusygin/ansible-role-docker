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


def test_userns_hello_world_container(host):
    entry = _get_entry(host=host, path="/etc/subuid", name="dockremap")
    assert entry is not None

    subuid = entry[1]

    entry = _get_entry(host=host, path="/etc/subgid", name="dockremap")
    assert entry is not None

    subgid = entry[1]

    namespaced_dir_path = "/var/lib/docker/{}.{}".format(subuid, subgid)
    assert host.file(path=namespaced_dir_path).is_directory

    args = (
        "docker", "container", "run",
        "--name", "say-hello",
        "hello-world",
    )
    cmd = host.run_test(command=" ".join(args))
    assert "Hello from Docker!" in cmd.stdout

    matches = host.docker.get_containers(name="say-hello")
    assert len(matches) == 1

    container_id = matches[0].id
    container_path = namespaced_dir_path + "/containers/" + container_id
    assert host.file(path=container_path).is_directory


def _get_entry(host, path, name):
    content = host.file(path).content_string
    entries = [
        tuple(line.split(":"))
        for line in content.splitlines()
    ]
    matches = [
        entry
        for entry in entries
        if entry[0] == name
    ]
    if matches:
        return matches[0]
    return None
