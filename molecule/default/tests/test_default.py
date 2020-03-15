"""
Molecule unit tests
"""
import os
import testinfra.utils.ansible_runner

TESTINFRA_HOSTS = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']
).get_hosts('all')


def test_packages(host):
    """
    check if packages are installed
    """
    # get variables from file
    ansible_vars = host.ansible("include_vars", "file=main.yml")
    # check packages
    for pkg in ansible_vars["ansible_facts"]["os_packages"]:
        assert host.package(pkg).is_installed


def test_service(host):
    """
    check if service is running
    """
    # get variables from file
    ansible_vars = host.ansible("include_vars", "file=main.yml")
    # check service
    service = ansible_vars["ansible_facts"]["os_service"]
    assert host.service(service).is_running
    assert host.service(service).is_enabled


def test_ports_listen(host):
    """
    check if ports are listening
    """
    for port in [1883]:
        assert host.socket("tcp://0.0.0.0:%s" % port).is_listening


def test_configuration(host):
    """
    check configuration
    """
    # get variables from file
    ansible_vars = host.ansible("include_vars", "file=main.yml")
    config_files = [
        '/etc/mosquitto/mosquitto.conf',
        '/etc/mosquitto/conf.d/acl.conf',
        '/etc/mosquitto/pwfile'
    ]
    with host.sudo():
        # check if files exist
        for config_file in config_files:
            assert host.file(config_file).exists
        # check if ACLs are defined
        acl_files = [
            "/etc/mosquitto/pwfile",
            "/etc/mosquitto/conf.d/acl"
        ]
        for user in ansible_vars["ansible_facts"]["user_topics"]:
            for acl_file in acl_files:
                assert host.file(acl_file).contains(user['user'])
