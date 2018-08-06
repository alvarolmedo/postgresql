testinfra_hosts = ["Node"]


def test_postgresql_packages(host, AnsibleAllVars):
    version_terse = str(AnsibleAllVars["postgresql_version"]).replace('.','')
    packages = ["postgresql%s-server" % version_terse, "postgresql%s" % version_terse, "postgresql%s-contrib" % version_terse]
    for package in packages:
        pg_package = host.package(package)
        assert pg_package.is_installed

def test_postgresql_running_as_root_and_enabled(host, AnsibleAllVarsFamily):
    service_name = AnsibleAllVarsFamily["postgresql_service_name"]
    postgresql_service = host.service(service_name)
    assert postgresql_service.is_running
    assert postgresql_service.is_enabled


def test_postgresql_start_stop(host, AnsibleAllVarsFamily):
    service_name = AnsibleAllVarsFamily["postgresql_service_name"]
    stop_postgresql(host, AnsibleAllVarsFamily)
    postgresql_service = host.service(service_name)
    assert not postgresql_service.is_running
    start_postgresql(host, AnsibleAllVarsFamily)
    assert postgresql_service.is_running
    restart_postgresql(host, AnsibleAllVarsFamily)
    assert postgresql_service.is_running


def start_postgresql(host, AnsibleAllVarsFamily):
    service_name = AnsibleAllVarsFamily["postgresql_service_name"]
    srv_mgr = host.ansible("setup")["ansible_facts"]["ansible_service_mgr"]

    if srv_mgr == "systemd":
        host.command.run_expect([0], "systemctl start %s" % service_name)
    else:
        host.command.run_expect([0], "service %s start" % service_name)


def restart_postgresql(host, AnsibleAllVarsFamily):
    service_name = AnsibleAllVarsFamily["postgresql_service_name"]
    srv_mgr = host.ansible("setup")["ansible_facts"]["ansible_service_mgr"]

    if srv_mgr == "systemd":
        host.command.run_expect([0], "systemctl restart %s" % service_name)
    else:
        host.command.run_expect([0], "service %s restart" % service_name)


def stop_postgresql(host, AnsibleAllVarsFamily):
    service_name = AnsibleAllVarsFamily["postgresql_service_name"]
    srv_mgr = host.ansible("setup")["ansible_facts"]["ansible_service_mgr"]

    if srv_mgr == "systemd":
        host.command.run_expect([0], "systemctl stop %s" % service_name)
    else:
        host.command.run_expect([0], "service %s stop" % service_name)
