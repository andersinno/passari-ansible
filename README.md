passari-ansible
======================

Ansible playbook to provision a CentOS 7 system for digital preservation.

To get started, install Ansible. On Fedora-based systems such as CentOS, you can run:

```
sudo yum install ansible
```

After this, you can run the playbook by running:

```
ansible-playbook site.yml -i hosts
```

Adjust the host settings in `hosts` if needed. Configure the new hosts as by making a copy of `group_vars/all` (file containing the default settings) and editing it as necessary.
