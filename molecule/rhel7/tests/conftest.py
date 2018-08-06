import pytest

# Load ansible facts
@pytest.fixture(scope="module")
def AnsibleFacts(host):
    return host.ansible("setup")['ansible_facts']

# Load role defaults
@pytest.fixture(scope="module")
def AnsibleDefaults(host):
    return host.ansible("include_vars","../../defaults/main.yml")["ansible_facts"]

# Load role vars
@pytest.fixture(scope="module")
def AnsibleVars(host):
    return host.ansible("include_vars","../../vars/main.yml")["ansible_facts"]

# Load vars depending on the os family
@pytest.fixture(scope="module")
def AnsibleVarsFamily(host, AnsibleFacts):
    ansible_os_family = AnsibleFacts['ansible_os_family']
    return host.ansible("include_vars","../../vars/%s.yml" % ansible_os_family)["ansible_facts"]

# Load role vars in the same way as ansible does.
# Order: role defaults, facts, vars.
@pytest.fixture(scope="module")
def AnsibleAllVars(host, AnsibleFacts, AnsibleVars, AnsibleDefaults):
    result= AnsibleDefaults
    result.update(AnsibleFacts)
    result.update(AnsibleVars)
    return result


# Load role vars in the same way as ansible does, using AnsibleVarsVer.
# Order: role defaults, facts, vars.
@pytest.fixture(scope="module")
def AnsibleAllVarsFamily(host, AnsibleFacts, AnsibleVars, AnsibleVarsFamily, AnsibleDefaults):
    result= AnsibleDefaults
    result.update(AnsibleFacts)
    result.update(AnsibleVars)
    result.update(AnsibleVarsFamily)
    return result