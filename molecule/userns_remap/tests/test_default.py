from json import loads
from os import environ
from pathlib import Path
from typing import Optional

from testinfra.utils.ansible_runner import AnsibleRunner


_runner = AnsibleRunner(environ["MOLECULE_INVENTORY_FILE"])
testinfra_hosts = _runner.get_hosts("instance")


def test_run_container(host) -> None:
    subuid_entry = _get_entry(host, Path("/etc/subuid"), "dockremap")
    assert subuid_entry is not None

    subgid_entry = _get_entry(host, Path("/etc/subgid"), "dockremap")
    assert subgid_entry is not None

    subuid = subuid_entry[1]
    subgid = subgid_entry[1]
    docker_dir_path = Path(f"/var/lib/docker/{subuid}.{subgid}")
    assert host.file(str(docker_dir_path)).is_directory

    args: tuple[str, ...]
    args = (
        "docker",
        "container",
        "run",
        "--name=say-hello",
        "hello-world",
    )
    cmd = host.run_expect(expected=[0], command=" ".join(args))
    assert "Hello from Docker!" in cmd.stdout

    args = ("docker", "container", "inspect", "say-hello")
    cmd = host.run_expect(expected=[0], command=" ".join(args))

    container_info = loads(cmd.stdout)[0]
    container_id = container_info["Id"]
    container_path = Path(docker_dir_path, "containers", container_id)
    assert host.file(str(container_path)).is_directory


def _get_entry(host, path: Path, name: str) -> Optional[tuple[str, int, int]]:
    content = host.file(str(path)).content_string
    entries = [tuple(line.split(":")) for line in content.splitlines()]
    matches = [entry for entry in entries if entry[0] == name]
    if matches:
        login, first_id, count = matches[0]
        return login, int(first_id), int(count)
    return None
