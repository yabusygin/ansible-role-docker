import os

import requests

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ["MOLECULE_INVENTORY_FILE"]
).get_hosts("instance")


def test_compose_binary_version(host):
    cmd = host.run_test(command="/usr/bin/docker-compose version --short")
    current_version = cmd.stdout.strip()

    response = requests.get(
        url="https://api.github.com/repos/docker/compose/releases/latest",
    )
    latest_version = response.json()["name"]

    assert current_version == latest_version


def test_pypi_package_is_absent(host):
    packages = host.pip_package.get_packages(pip_path="pip3")
    assert "docker-compose" not in packages
