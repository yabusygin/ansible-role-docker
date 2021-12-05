from os import environ

from packaging.version import parse, Version
from testinfra.utils.ansible_runner import AnsibleRunner


_runner = AnsibleRunner(environ["MOLECULE_INVENTORY_FILE"])
testinfra_hosts = _runner.get_hosts("instance")


def test_run_container(host):
    args = ("docker", "container", "run", "hello-world")
    cmd = host.run_expect(expected=[0], command=" ".join(args))
    assert "Hello from Docker!" in cmd.stdout


def test_ansible_modules_dependencies(host):
    packages = host.pip.get_packages(pip_path="pip3")

    assert "docker" in packages
    installed_version = parse(version=packages["docker"]["version"])
    assert installed_version >= Version("1.10.0")

    assert "PyYAML" in packages
    installed_version = parse(version=packages["PyYAML"]["version"])
    assert installed_version >= Version("3.11")

    assert "docker-compose" in packages
    installed_version = parse(version=packages["docker-compose"]["version"])
    assert installed_version >= Version("1.7.0")
