# Ganeti installation tutorial for RHEL/CentOS/others

This documentation is the short version for RHEL/CentOS/others 7.x and 8.x.

**The DRBD disk template cannot be used with el8 because kmod-drbd84 and drbd84-utils for ELRepo el8 have not been released.**

Official full version:

- [Ganeti's documentation](http://docs.ganeti.org/ganeti/current/html/) > [Ganeti installation tutorial](http://docs.ganeti.org/ganeti/current/html/install.html)

Upgrade / update to the latest version:

* [Upgrade guides (update-rhel-*)](https://github.com/jfut/ganeti-rpm/tree/master/doc/)

## Installing the base system

Ganeti works on a single node, but we recommend a configuration with 3 or more nodes.
With two nodes, there is a problem with voting to determine the master during a master failover.

**Mandatory** on all nodes.

Note that Ganeti requires the hostnames of the systems.

e.g. DNS or `/etc/hosts`:

```
127.0.0.1       localhost
# cluster name
192.168.1.1     gcluster
# node names
192.168.1.11    node1.example.com node1
192.168.1.12    node2.example.com node2
192.168.1.13    node3.example.com node3
# instance names
192.168.1.101   instance1.example.com instance1
192.168.1.102   instance2.example.com instance2
```

## Installing The Hypervisor

Ganeti supports Xen, KVM, and LXC. The KVM hypervisor is the most commonly used on RHEL/CentOS/Scientific CentOS.

**Mandatory** on all nodes.

- KVM on RHEL/CentOS/others **7.x**

The oldest version of qemu supported by Ganeti is `qemu-2.11`. Therefore, it is recommended to install `qemu-kvm-ev`(version `2.12.x`) instead of `qemu-kvm`(version `1.5.x`) on `el7`.

```bash
# centos-release-qemu-ev - QEMU Enterprise Virtualization packages from the CentOS Virtualization SIG repository
yum install centos-release-qemu-ev
yum install qemu-kvm-ev libvirt python-virtinst virt-install bridge-utils
```

- KVM on RHEL/CentOS/others **8.x**

```bash
dnf install qemu-kvm libvirt python-virtinst virt-install bridge-utils
```

### KVM settings

- KVM on RHEL/CentOS/others

**Mandatory** on all nodes.

(Optional) Service configuration for libvirt.

Enable services:

```bash
systemctl enable libvirtd.service
systemctl enable ksm.service
systemctl enable ksmtuned.service
```

Disable unused virbrX:

```bash
systemctl start libvirtd.service

virsh net-autostart default --disable
virsh net-destroy default
```

Create bridge interface:

`br0` is an example of bridge interface.

- Using NetworkManager

```bash
nmcli connection add type bridge autoconnect yes ipv4.method disabled ipv6.method ignore bridge.stp no bridge.forward-delay 0 con-name "br0" ifname "br0"
nmcli connection modify "eno1" connection.slave-type bridge connection.master "br0"
nmcli connection modify br0 ipv4.method manual ipv4.addresses "192.168.1.11/24 192.168.1.254" ipv4.dns "192.168.1.1,"192.168.1.2"
nmcli connection up br0
nmcli connection down eno1
nmcli connection up bridge-slave-eno1

# VLAN filter support on bridge(VLAN aware bridge)
# Require ganeti-2.16.2-1 RPM or later
# set VLAN 100: gnt-instance modify --net 0:modify,vlan=100 instance1
nmcli connection modify br0 bridge.vlan-filtering yes
nmcli connection down br0
nmcli connection up br0
```

You can setup it easily by using [nmcli-cli](https://github.com/jfut/nmcli-cli).

```bash
nmcli-cli-bridge-add -x br1 eno1
nmcli-cli-ipv4 -x br1 static 192.168.1.11/24 192.168.1.254 "192.168.1.1,"192.168.1.2"
nmcli connection modify br0 bridge.vlan-filtering yes

nmcli connection up br0
nmcli connection down eno1
nmcli connection up bridge-slave-eno1
```

Allow to bridge interface access.

- Using iptables

Edit `/etc/sysconfig/iptables`:

```
*filter
...
-A INPUT -j REJECT --reject-with icmp-host-prohibited
## FORWARD
-A FORWARD -m physdev --physdev-is-bridged -j ACCEPT
COMMIT
```

Apply firewall rules:

```bash
iptables-restore < /etc/sysconfig/iptables
```

## Setting up yum/dnf repositories

**Mandatory** on all nodes.

Install ELRepo repository for DRBD packages:

```bash
# RHEL/CentOS/others **7.x**
yum install elrepo-release
yum-config-manager --disable elrepo

# RHEL/CentOS/others **8.x**
dnf install elrepo-release
dnf config-manager --disable elrepo
```

Install EPEL repository for dependency packages:

```bash
# RHEL/CentOS/others **7.x**
yum install epel-release
yum-config-manager --disable epel

# RHEL/CentOS/others **8.x**
dnf install epel-release
dnf config-manager --disable epel
```

Install Integ Ganeti repository:

```bash
# RHEL/CentOS/others **7.x**
yum install https://jfut.integ.jp/linux/ganeti/7/x86_64/integ-ganeti-release-7-2.el7.noarch.rpm
yum-config-manager --disable integ-ganeti

# RHEL/CentOS/others **8.x**
dnf install https://jfut.integ.jp/linux/ganeti/8/x86_64/integ-ganeti-release-8-1.el7.noarch.rpm
dnf config-manager --disable integ-ganeti
```

## Installing DRBD

**kmod-drbd84 and drbd84-utils for el8 in ELRepo have not been released.**

**Mandatory** on all nodes.

Install DRBD package:

```bash
yum --enablerepo=elrepo install kmod-drbd84 drbd84-utils
```

- RHEL/CentOS/others **7.x and later**

Create `/etc/modules-load.d/drbd.conf`:

```bash
echo "drbd" >> /etc/modules-load.d/drbd.conf
```

Create `/etc/modprobe.d/drbd.conf`:

```bash
echo "options drbd minor_count=128 usermode_helper=/bin/true" >> /etc/modprobe.d/drbd.conf
```

Load DRBD kernel module:

```bash
systemctl start systemd-modules-load
```

## Configuring LVM

**Mandatory** on all nodes.

The volume group is required to be at least 20GiB.

If you haven't configured your LVM volume group at install time you
need to do it before trying to initialize the Ganeti cluster. This is
done by formatting the devices/partitions you want to use for it and
then adding them to the relevant volume group.

```bash
pvcreate /dev/sda3
vgcreate vmvg /dev/sda3
```

or

```bash
pvcreate /dev/sdb1
pvcreate /dev/sdc1
vgcreate vmvg /dev/sdb1 /dev/sdc1
```

If you want to add a device later you can do so with the *vgextend*
command:

```bash
pvcreate /dev/sdd1
vgextend vmvg /dev/sdd1
```

(Optional) it is recommended to configure LVM not to scan the DRBD
devices for physical volumes. This can be accomplished by editing
`/etc/lvm/lvm.conf` and adding the
`/dev/drbd[0-9]+` regular expression to the
`filter` variable, like this:

```bash
filter = ["r|/dev/cdrom|", "r|/dev/drbd[0-9]+|" ]
```

## Installing Ganeti

**Mandatory** on all nodes.

- Install Ganeti:

```bash
yum --enablerepo=epel,integ-ganeti install ganeti
```

- (Optional) Install Ganeti Instance Debootstrap and snf-image:

```bash
yum --enablerepo=epel,integ-ganeti install ganeti-instance-debootstrap snf-image
```

Required ports(default):

Several network ports must be available and opened so the different nodes can communicate properly between them.

- ganeti-noded: 1811/tcp
- ganeti-confd: 1814/udp
- ganeti-rapi: 5080/tcp
- ganeti-mond: 1815/tcp
- ganeti-metad: 80/tcp
- DRBD/VNC port for instances: 11000/tcp - 14999/tcp

Service configuration:

```bash
systemctl enable ganeti.target
systemctl enable ganeti-confd.service
systemctl enable ganeti-noded.service
systemctl enable ganeti-wconfd.service
systemctl enable ganeti-rapi.service
systemctl enable ganeti-luxid.service
systemctl enable ganeti-kvmd.service

# Optional: ganeti-mond is the daemon providing the Ganeti monitoring functionality.
systemctl enable ganeti-mond.service

# Optional: ganeti-metad is the daemon providing the metadata service.
# If you want to disable ganeti-metad:
systemctl enable ganeti-metad.service
```

## Initializing the cluster

**Mandatory** on one node per cluster.

Create ~/.ssh directory.

```bash
if [[ ! -d ~/.ssh ]]; then mkdir ~/.ssh; chmod 600 ~/.ssh; fi
```

Initialize a cluster.

```bash
gnt-cluster init --vg-name <VOLUMEGROUP> --master-netdev <MASTERINTERFACE> --nic-parameters link=<BRIDGEINTERFACE> <CLUSTERNAME>
```

Example for KVM:

```bash
# gnt-cluster init --vg-name vmvg --master-netdev <MASTERINTERFACE> --enabled-hypervisors kvm --nic-parameters link=<BRIDGEINTERFACE> gcluster
gnt-cluster init --vg-name vmvg --master-netdev eno1 --enabled-hypervisors kvm --nic-parameters link=br0 gcluster
```

Set default metavg parameter for DRBD disk

```bash
gnt-cluster modify -D drbd:metavg=vmvg
```

Enable use_bootloader for using VM's boot loader.

```bash
gnt-cluster modify --hypervisor-parameters kvm:kernel_path=
```

## Verifying the cluster

**Mandatory** on master node.

```bash
gnt-cluster verify
```

## Joining the nodes to the cluster

**Mandatory** on master node.

After you have initialized your cluster you need to join the other nodes
to it. You can do so by executing the following command on the master
node.

```bash
gnt-node add <NODENAME>
gnt-node add node2

gnt-node add node3

... and more node.
```

**Troubleshooting**

- `gnt-node add node2` returns with the error:

```
Node daemon on node2.example.com didn't answer queries within 10.0 seconds
```
Make sure that you have port 1811 open (`lokkit -p 1811:tcp`)

- `gnt-cluster verify` on master returns an error after `Verifying node status`:

```
ERROR: node node2.example.com: ssh communication with node 'node1.example.com': ssh problem: ssh_exchange_identification: read: Connection reset by peer\'r\n
```

Initiate a manual ssh connection from node2 to node1 and vice versa.

## Manage ganeti services

**Mandatory** on all nodes.

### Start

```bash
systemctl start ganeti.target
systemctl start ganeti-kvmd.service

# Optional: ganeti-metad is the daemon providing the metadata service.
systemctl start ganeti-metad.service
```

### Stop

```bash
systemctl stop ganeti-metad.service
systemctl stop ganeti-kvmd.service
systemctl stop ganeti.target
```

## Setting up and managing virtual instances

**Mandatory** on master node.

### Setting up virtual instances

- Setting up RHEL/CentOS/others

We recommend to use [Ganeti Instance Image](https://github.com/osuosl/ganeti-instance-image).

- Setting up Debian (require ganeti-instance-debootstrap)

Installation will be successful, but gnt-instance console doesn't work.

```bash
gnt-instance add -t drbd -n node1:node2 -o debootstrap+default --disk 0:size=8G -B vcpus=2,maxmem=1024,minmem=512 instance1
```

