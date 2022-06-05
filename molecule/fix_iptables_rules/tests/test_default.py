from os import environ

from testinfra.utils.ansible_runner import AnsibleRunner


_runner = AnsibleRunner(environ["MOLECULE_INVENTORY_FILE"])
testinfra_hosts = _runner.get_hosts("instance")


def test_iptables_restore(host):
    _clear_iptables(host=host)

    vars = {
        "docker_ansible_dependencies_install": False,
    }
    result = _ansible_role(host=host, role_name="yabusygin.docker", vars=vars)

    assert result["changed"]
    assert len(host.iptables.rules(table="filter", chain="DOCKER")) > 0
    assert len(host.iptables.rules(table="nat", chain="DOCKER")) > 0


def _clear_iptables(host):
    host.run_expect(
        expected=[0],
        command="iptables --table=filter --flush")
    host.run_expect(
        expected=[0],
        command="iptables --table=filter --delete-chain")
    host.run_expect(
        expected=[0],
        command="iptables --table=nat --flush")
    host.run_expect(
        expected=[0],
        command="iptables --table=nat --delete-chain")


def _ansible_role(host, role_name, vars):
    result = host.ansible(module_name="ansible.builtin.setup")

    extra_vars = {
        "ansible_facts": {
            key.removeprefix("ansible_"): value
            for key, value in result["ansible_facts"].items()
        },
    }
    extra_vars.update(vars)

    return host.ansible(
        module_name="ansible.builtin.import_role",
        module_args=f"name={role_name}",
        extra_vars=extra_vars,
        check=False)
