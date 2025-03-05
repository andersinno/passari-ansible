# Passari Ansible

Ansible playbooks to provision AlmaLinux 9 based hosts for system for
digital preservation with Passari.

## Installing Ansible

To get started, install Ansible. On Fedora-based systems such
AlmaLinux, you can run:

    sudo dnf install ansible

On Debian-based systems, you can run:

    sudo apt-get install ansible

You may also install Ansible using Python's Pip package manager and
utilize the provided `requirements.txt` file. Use a separate virtual
environment to avoid conflicts with system packages:

    python3 -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt

## Configuration

To configure the Ansible playbooks, you need to create an inventory.
There is an example inventory in `inventory/example` which you can copy
to e.g. `inventory/production` and modify as needed.

The inventory should contain the hosts that you want to provision and
the groups that they belong to. The groups are used to apply roles to
the hosts.

The inventory should also contain the variables that are used to
configure the hosts. The variables are stored in the `group_vars` and
`host_vars` directories.

## Running the Playbooks

When Ansible is installed, you can run the playbook by running:

    ansible-playbook -J -i inventory/YOUR_INVENTORY site.yml

### Testing the Playbooks with a Single Host

It's also possible to test the playbooks with a single host by using
the `inventory/example` inventory and defining the connection settings
in `inventory/example/host_vars/example-host/connection.yml`.  There is
a template file in that directory that you can copy and modify.

To run the playbook with the example inventory, you can run:

    ansible-playbook -i inventory/example site.yml

## Architecture

The Ansible playbooks are divided into roles which are used to provision
the hosts. The hosts belong to groups which define the roles that are
applied to them.

The host groups are:

- `workflow_workers`
- `web_ui_hosts`
- `database_hosts`
- `backup_hosts`

The roles are:

- `common`: Common packages and settings for all hosts
- `passari_workflow`: Passari Workflow Worker
- `passari_web_ui`: Passari Web User Interface
- `validators`: Installs software used in the SIP validation
- `passari_packages`: Installation packages for the Workflow and Web UI
- `passari_user`: Create the user account for the Passari services
- `python_install`: Provide another Python version (used for Passari)
- `nginx`: Nginx web server for serving the Web UI
- `uwsgi`: uWSGI application server for the Web UI
- `letsencrypt`: Let's Encrypt CertBot for renewing TLS certificates
- `postgresql`: PostgreSQL database for the web UI and Workflow
- `redis`: Redis key-value store for the Workflow Workers
- `passari_backup`: Backup the Passari database

The dependency tree of the host groups and roles is as follows. Note
that the `common` role is applied to all hosts, but it is not shown in
the graph.

```mermaid
graph TD;
    WW[workflow_workers];
    WW --> WF[passari_workflow];
    WF --> validators;
    WF --> passari_user;
    WF --> passari_packages;

    WH[web_ui_hosts];
    WH --> WU[passari_web_ui];
    WH --> letsencrypt;
    letsencrypt --> nginx;
    WU --> passari_user;
    WU --> passari_packages;
    WU --> nginx;
    WU --> uwsgi;
    uwsgi --> nginx;
    passari_packages --> python_install;

    DH[database_hosts];
    DH --> postgresql;
    DH --> redis;

    backup_hosts --> passari_backup;
```
