from os import environ
from pathlib import Path

from testinfra.utils.ansible_runner import AnsibleRunner


_runner = AnsibleRunner(environ["MOLECULE_INVENTORY_FILE"])
testinfra_hosts = _runner.get_hosts("instance")


def test_run_container(host):
    subuid_entry = _get_entry(host, Path("/etc/subuid"), "dockremap")
    assert subuid_entry is not None

    subgid_entry = _get_entry(host, Path("/etc/subgid"), "dockremap")
    assert subgid_entry is not None

    subuid = subuid_entry[1]
    subgid = subgid_entry[1]
    docker_dir_path = Path("/var/lib/docker/{}.{}".format(subuid, subgid))
    assert host.file(str(docker_dir_path)).is_directory

    args = (
        "docker", "container", "run",
        "--name=say-hello",
        "hello-world",
    )
    cmd = host.run_test(command=" ".join(args))
    assert "Hello from Docker!" in cmd.stdout

    matches = host.docker.get_containers(name="say-hello")
    assert len(matches) == 1

    container_info = matches[0]
    container_id = container_info.id
    container_path = Path(docker_dir_path, "containers", container_id)
    assert host.file(str(container_path)).is_directory


def _get_entry(host, path, name):
    content = host.file(str(path)).content_string
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
