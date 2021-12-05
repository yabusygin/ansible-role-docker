from os import environ

from requests import get
from testinfra.utils.ansible_runner import AnsibleRunner


_runner = AnsibleRunner(environ["MOLECULE_INVENTORY_FILE"])
testinfra_hosts = _runner.get_hosts("instance")


def test_compose_binary_sha256(host):
    release_url = "https://api.github.com/repos/docker/compose/releases/latest"
    response = get(release_url)
    response_payload = response.json()
    version = response_payload["name"]

    download_url = "https://github.com/docker/compose/releases/download"
    sha256_url = f"{download_url}/{version}/docker-compose-Linux-x86_64.sha256"
    response = get(sha256_url)
    response_payload = response.text.splitlines()
    sha256sum_entry = response_payload[0]
    expect = sha256sum_entry.split(" ")[0]

    actual = host.file("/usr/bin/docker-compose").sha256sum
    assert expect == actual
