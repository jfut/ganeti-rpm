# Ganeti installation tutorial for RHEL/CentOS/Scientific Linux

This documentation is the short version for RHEL/CentOS/Scientific Linux.

Official full version:

- [Ganeti's documentation](http://docs.ganeti.org/ganeti/current/html/) > [Ganeti installation tutorial](http://docs.ganeti.org/ganeti/current/html/install.html)

New versions and updating:

* [Upgrade guides](https://github.com/jfut/ganeti-rpm/tree/master/doc/)

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

**Mandatory** on all nodes.

- KVM on RHEL/CentOS/Scientific Linux **7.x and later**

```
yum install qemu-kvm libvirt python-virtinst virt-install bridge-utils
```

### KVM settings

- KVM on RHEL/CentOS/Scientific Linux

**Mandatory** on all nodes.

(Optional) Service configuration for libvirt:

- RHEL/CentOS/Scientific Linux **7.x and later**

Enable services:

```
systemctl enable libvirtd.service
systemctl enable ksm.service
systemctl enable ksmtuned.service
```

Disable unused virbrX:

```
systemctl start libvirtd.service

virsh net-autostart default --disable
virsh net-destroy default
```

Create bridge interface:

br0 is an example of bridge interface.

- Using NetworkManager

```
nmcli connection add type bridge autoconnect yes ipv4.method disabled ipv6.method ignore bridge.stp no bridge.forward-delay 0 con-name "br0" ifname "br0"
nmcli connection modify "eno1" connection.slave-type bridge connection.master "br0"
nmcli connection modify br0 ipv4.method manual ipv4.addresses "192.168.1.11/24 192.168.1.254" ipv4.dns "192.168.1.254"
nmcli connection up br0
nmcli connection down eth0
nmcli connection up bridge-slave-eth0

# VLAN filter support on bridge(VLAN aware bridge)
# Require ganeti-2.16.2-1 RPM or later
# set VLAN 100: gnt-instance modify --net 0:modify,vlan=100 instance1
nmcli connection modify br0 bridge.vlan-filtering yes
nmcli connection down br0
nmcli connection up br0
```

You can setup it easily by using [nmcli-cli](https://github.com/jfut/nmcli-cli).

- Using manual configuration

Edit `/etc/sysconfig/network-scripts/ifcfg-eth0`:

```
DEVICE="eth0"
BOOTPROTO="static"
HWADDR="??:??:??:??:??:??"
ONBOOT="yes"
BRIDGE="br0"
```

Edit `/etc/sysconfig/network-scripts/ifcfg-br0`:

```
DEVICE="br0"
TYPE=Bridge
BOOTPROTO="static"
IPADDR="192.168.1.11"
NETMASK="255.255.255.0"
ONBOOT="yes"
```

Apply network configurations.

```
/etc/init.d/network restart
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

```
iptables-restore < /etc/sysconfig/iptables
```

## Setting up yum repositories

**Mandatory** on all nodes.

Install ELRepo repository:

e.g. RHEL/CentOS **7.x**:

```
rpm --import http://elrepo.org/RPM-GPG-KEY-elrepo.org
yum install https://www.elrepo.org/elrepo-release-7.0-3.el7.elrepo.noarch.rpm
yum-config-manager --disable elrepo
```

e.g. Scientific Linux:

```
yum install yum-conf-elrepo
yum-config-manager --disable elrepo
```

Install EPEL repository:

e.g. Scientific Linux:

```
yum install yum-conf-epel
yum-config-manager --disable epel
```

Install Integ Ganeti repository:

- RHEL/CentOS/Scientific Linux **7.x**

```
yum install http://jfut.integ.jp/linux/ganeti/7/x86_64/integ-ganeti-release-7-2.el7.noarch.rpm
yum-config-manager --disable integ-ganeti
```

## Installing DRBD

**Mandatory** on all nodes.

Install DRBD package:

```
yum --enablerepo=elrepo install drbd84-utils kmod-drbd84
```

- RHEL/CentOS/Scientific Linux **7.x and later**

Create `/etc/modules-load.d/drbd.conf`:

```
drbd
```

Create `/etc/modprobe.d/drbd.conf`:

```
options drbd minor_count=128 usermode_helper=/bin/true
```

Load DRBD kernel module:

```
systemctl start systemd-modules-load
```

## Configuring LVM

**Mandatory** on all nodes.

The volume group is required to be at least 20GiB.

If you haven't configured your LVM volume group at install time you
need to do it before trying to initialize the Ganeti cluster. This is
done by formatting the devices/partitions you want to use for it and
then adding them to the relevant volume group.

```
pvcreate /dev/sda3
vgcreate vmvg /dev/sda3
```

or

```
pvcreate /dev/sdb1
pvcreate /dev/sdc1
vgcreate vmvg /dev/sdb1 /dev/sdc1
```

If you want to add a device later you can do so with the *vgextend*
command:

```
pvcreate /dev/sdd1
vgextend vmvg /dev/sdd1
```

(Optional) it is recommended to configure LVM not to scan the DRBD
devices for physical volumes. This can be accomplished by editing
`/etc/lvm/lvm.conf` and adding the
`/dev/drbd[0-9]+` regular expression to the
`filter` variable, like this:

```
filter = ["r|/dev/cdrom|", "r|/dev/drbd[0-9]+|" ]
```

## Installing Ganeti

**Mandatory** on all nodes.

- Install Ganeti:

```
yum --enablerepo=epel,integ-ganeti install ganeti
```

- (Optional) Install Ganeti Instance Debootstrap and snf-image:

```
yum --enablerepo=epel,integ-ganeti install ganeti-instance-debootstrap snf-image
```

Required ports:

Several network ports must be available and opened so the different nodes can communicate properly between them.

- ganeti-noded: 1811/tcp
- ganeti-confd: 1814/udp
- ganeti-rapi: 5080/tcp
- ganeti-mond: 1815/tcp
- ganeti-metad: 80/tcp
- DRBD port for instances: 11000/tcp - 14999/tcp
- VNC port: 5900/tcp

Service configuration:

- RHEL/CentOS/Scientific Linux **7.x and later**

```
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

```
if [[ ! -d ~/.ssh ]]; then mkdir ~/.ssh; chmod 600 ~/.ssh; fi
```

Initialize a cluster.

```
gnt-cluster init --vg-name <VOLUMEGROUP> --master-netdev <MASTERINTERFACE> --nic-parameters link=<BRIDGEINTERFACE> <CLUSTERNAME>
```

Example for KVM:

```
gnt-cluster init --vg-name vmvg --master-netdev <MASTERINTERFACE> --enabled-hypervisors kvm --nic-parameters link=<BRIDGEINTERFACE> gcluster
e.g. gnt-cluster init --vg-name vmvg --master-netdev eth0 --enabled-hypervisors kvm --nic-parameters link=br0 gcluster
```

Set default metavg parameter for DRBD disk

```
gnt-cluster modify -D drbd:metavg=vmvg
```

Enable use_bootloader for using VM's boot loader.

```
gnt-cluster modify --hypervisor-parameters kvm:kernel_path=
```

## Verifying the cluster

**Mandatory** on master node.

```
gnt-cluster verify
```

## Joining the nodes to the cluster

**Mandatory** on master node.

After you have initialized your cluster you need to join the other nodes
to it. You can do so by executing the following command on the master
node.

```
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

## Setting up and managing virtual instances

**Mandatory** on master node.

### Setting up virtual instances

- Setting up RHEL/CentOS/Scientific Linux

We recommend to use [Ganeti Instance Image](https://github.com/osuosl/ganeti-instance-image).

- Setting up Debian (require ganeti-instance-debootstrap)

Installation will be successful, but gnt-instance console doesn't work.

```
gnt-instance add -t drbd -n node1:node2 -o debootstrap+default --disk 0:size=8G -B vcpus=2,maxmem=1024,minmem=512 instance1
```

