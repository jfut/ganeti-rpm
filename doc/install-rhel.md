# Ganeti installation tutorial for RHEL/AlmaLinux/Rocky Linux/others

This is a short guide for RHEL/AlmaLinux/Rocky Linux/others 8.x, 9.x, and 10.x.

Official documentation:

- [Ganeti's documentation](http://docs.ganeti.org/ganeti/current/html/) > [Ganeti installation tutorial](http://docs.ganeti.org/ganeti/current/html/install.html)

Upgrade/update to the latest version:

* [Upgrade / update guides (update-rhel-*)](https://github.com/jfut/ganeti-rpm/tree/main/doc)

## Installing the base system

Ganeti can run on a single node, but we recommend a configuration with three or more nodes.
With only two nodes, quorum issues can prevent electing a new master during failover.

**Mandatory** on all nodes.

Ensure that every node has a resolvable hostname.

For example, configure DNS or `/etc/hosts`:

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

## Installing the hypervisor

Ganeti supports Xen, KVM, and LXC. KVM is the most commonly used hypervisor on RHEL/AlmaLinux/CentOS/Rocky Linux/others.

**Mandatory** on all nodes.

```bash
# KVM on RHEL/AlmaLinux/Rocky Linux/others **8.x**
dnf install qemu-kvm libvirt virt-install

# KVM on RHEL/AlmaLinux/Rocky Linux/others **9.x or later**
dnf install qemu-kvm libvirt virt-install ksmtuned
```

### KVM settings

- KVM on RHEL/AlmaLinux/CentOS/Rocky Linux/others

**Mandatory** on all nodes.

Optional: configure libvirt services.

Enable services:

```bash
systemctl enable libvirtd.service
systemctl enable ksm.service
systemctl enable ksmtuned.service
```

Disable the unused `virbrX` network:

```bash
systemctl start libvirtd.service

virsh net-autostart default --disable
virsh net-destroy default
```

Create a bridge interface:

The interface `br0` is used as an example.

- Using NetworkManager:
  - physical interface: eno1
  - bridge interface: br0
  - ipv4.addresses: 192.168.1.11/24
  - ipv4.gateway: 192.168.1.254
  - ipv4.dns: "192.168.1.1,192.168.1.2"

```bash
nmcli connection add type bridge autoconnect yes ipv4.method disabled ipv6.method ignore bridge.stp no bridge.forward-delay 0 con-name br0 ifname br0
nmcli connection modify eno1 connection.slave-type bridge connection.master br0
nmcli connection modify br0 ipv4.method manual ipv4.addresses "192.168.1.11/24"
nmcli connection modify br0 ipv4.gateway "192.168.1.254" ipv4.dns "192.168.1.1,192.168.1.2"
nmcli connection up br0; nmcli connection down eno1; nmcli connection up eno1 &

# VLAN filter support on bridge(VLAN aware bridge)
# Require ganeti-2.16.2-1 RPM or later
# set VLAN 100: gnt-instance modify --net 0:modify,vlan=100 instance1
nmcli connection modify br0 bridge.vlan-filtering yes
nmcli connection down br0; nmcli connection up br0 &
```

You can set it up easily by using [nmcli-cli](https://github.com/jfut/nmcli-cli).

```bash
nmcli-cli-bridge-add -x br1 eno1
nmcli-cli-ipv4 -x br1 static 192.168.1.11/24 192.168.1.254 "192.168.1.1,"192.168.1.2"
nmcli connection modify br0 bridge.vlan-filtering yes

nmcli connection up br0
nmcli connection down eno1
nmcli connection up eno1
```

Allow traffic on the bridge interface.

- Using iptables

Edit `/etc/sysconfig/iptables`:

```
*filter
...
-A INPUT -j REJECT --reject-with icmp-host-prohibited
# FORWARD
-A FORWARD -m physdev --physdev-is-bridged -j ACCEPT
COMMIT
```

Edit `/etc/sysconfig/ip6tables`:

```
...
-A INPUT -j REJECT --reject-with icmp6-adm-prohibited
# FORWARD
-A FORWARD -m physdev --physdev-is-bridged -j ACCEPT
COMMIT
```

Apply firewall rules:

```bash
iptables-restore < /etc/sysconfig/iptables
ip6tables-restore < /etc/sysconfig/ip6tables
```

## Setting up dnf repositories

**Mandatory** on all nodes.

Install ELRepo repository for DRBD packages:

```bash
dnf install elrepo-release
dnf config-manager --disable elrepo
```

Install EPEL repository for dependency packages:

```bash
dnf install epel-release
dnf config-manager --disable epel
```

Install Integ Ganeti repository:

```bash
# RHEL/AlmaLinux/Rocky Linux/others **8.x**
dnf install https://jfut.integ.jp/linux/ganeti/8/x86_64/integ-ganeti-release-8-1.el8.noarch.rpm
dnf config-manager --disable integ-ganeti

# RHEL/AlmaLinux/Rocky Linux/others **9.x**
dnf install https://jfut.integ.jp/linux/ganeti/9/x86_64/integ-ganeti-release-9-1.el9.noarch.rpm
dnf config-manager --disable integ-ganeti

# RHEL/AlmaLinux/Rocky Linux/others **10.x**
dnf install https://jfut.integ.jp/linux/ganeti/10/x86_64/integ-ganeti-release-10-1.el10.noarch.rpm
dnf config-manager --disable integ-ganeti
```

## Installing DRBD

**Mandatory** on all nodes.

Install the DRBD package:

```bash
dnf --enablerepo=elrepo install kmod-drbd84 drbd84-utils
```

Enable `drbd.service`:

```bash
systemctl enable drbd.service
```

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
systemctl start drbd.service
```

## Configuring LVM

**Mandatory** on all nodes.

Create a volume group of at least 20 GiB.

If you did not configure an LVM volume group during installation,
prepare the devices or partitions before initializing the Ganeti cluster.
Format the devices you plan to use and add them to the target volume group.

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

If you want to add a device later, you can do so with the *vgextend*
command:

```bash
pvcreate /dev/sdd1
vgextend vmvg /dev/sdd1
```

Optional: configure LVM to skip scanning DRBD
devices for physical volumes. Edit
`/etc/lvm/lvm.conf` and add the
`/dev/drbd[0-9]+` regular expression to the
`filter` variable, like this:

```bash
filter = ["r|/dev/cdrom|", "r|/dev/drbd[0-9]+|" ]
```

## Configuring SELinux

**Mandatory** on all nodes.

Configure SELinux parameters so Ganeti cluster operations work properly.

```bash
setsebool -P nis_enabled on
setsebool -P domain_can_mmap_files on
setsebool -P use_virtualbox on
```

## Installing Ganeti

**Mandatory** on all nodes.

- Install Ganeti:

```bash
dnf --enablerepo=epel,integ-ganeti install ganeti
```

- Optional: Install ganeti-instance-debootstrap:

```bash
dnf --enablerepo=epel,integ-ganeti install ganeti-instance-debootstrap
```

Required ports (default):

Make sure the following network ports are open so nodes can communicate properly.

- ganeti-noded: 1811/tcp
- ganeti-confd: 1814/udp
- ganeti-rapi: 5080/tcp
- ganeti-mond: 1815/tcp
- ganeti-metad: 80/tcp
- DRBD/VNC port for instances: 11000/tcp - 14999/tcp

Enable services:

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
systemctl enable ganeti-metad.service
```

## Initializing the cluster

**Mandatory** on one node per cluster.

Create the `~/.ssh` directory.

```bash
mkdir -p ~/.ssh
chmod 600 ~/.ssh
```

Initialize the cluster.

```bash
gnt-cluster init --vg-name <VOLUMEGROUP> --master-netdev <MASTERINTERFACE> --nic-parameters link=<BRIDGEINTERFACE> <CLUSTERNAME>
```

Example for KVM:

```bash
# gnt-cluster init --vg-name vmvg --master-netdev <MASTERINTERFACE> --enabled-hypervisors kvm --nic-parameters link=<BRIDGEINTERFACE> gcluster
gnt-cluster init --vg-name vmvg --master-netdev eno1 --enabled-hypervisors kvm --nic-parameters link=br0 gcluster
```

Set the default `metavg` parameter for DRBD disks:

```bash
gnt-cluster modify -D drbd:metavg=vmvg
```

Enable `use_bootloader` to use the VM's boot loader:

```bash
gnt-cluster modify --hypervisor-parameters kvm:kernel_path=
```

## Optional cluster configurations

Settings configured with the `gnt-cluster` command are global and apply to every instance. Override specific values per instance with the `gnt-instance` command.

### Enable user shutdown: --user-shutdown

The `--user-shutdown` option enables or disables user shutdown detection at the cluster level. User shutdown detection allows users to initiate instance poweroff from inside the instance, and Ganeti will report the instance status as `USER_down` (as opposed, to `ERROR_down`) and the watcher will not restart these instances, thus preserving their instance status.

```bash
gnt-cluster modify --user-shutdown yes
```

### Optimizing DRBD performance: -D drbd

Use the following examples to tune DRBD performance.

- [Optimizing DRBD performance section in The DRBD User's Guide](https://linbit.com/drbd-user-guide/users-guide-drbd-8-4/#p-performance)
- [DRBD 8.4 sync reaches over 100 MB/s on a 10 Gbit/s network](https://github.com/ganeti/ganeti/issues/1229)

```bash
# For example with 1 Gbps NIC: min: 64 MB/sec, max 96 MB/sec
gnt-cluster modify -D drbd:dynamic-resync=True,c-plan-ahead=20,c-fill-target=20480,c-min-rate=65536,c-max-rate=98304,resync-rate=98304
gnt-cluster modify -D drbd:disk-custom='--al-extents 3833',net-custom='--max-buffers 8192 --max-epoch-size 8192'

# For example with 10 Gbps NIC: min: 300 MB/sec, max 400 MB/sec
gnt-cluster modify -D drbd:dynamic-resync=True,c-plan-ahead=20,c-fill-target=20480,c-min-rate=307200,c-max-rate=409600,resync-rate=409600
gnt-cluster modify -D drbd:disk-custom='--al-extents 3833',net-custom='--max-buffers 8192 --max-epoch-size 8192'
```

### Change the CPU type: cpu_type

This parameter determines the emulated CPU for the instance.

```bash
# For clusters with the same CPU, it is possible to use the 'host' cpu type:
gnt-cluster modify -H kvm:cpu_type=host

# For example on a cluster using IvyBridge-IBRS generation or later CPUs, the following command can be used:
gnt-cluster modify -H kvm:cpu_type='IvyBridge-IBRS\,+pcid\,+ssbd\,+md-clear'

# Show available CPU types:
/usr/libexec/qemu-kvm -cpu help
```

### Change the CPU topology: cpu_sockets

Set the number of emulated CPU sockets.

```bash
gnt-cluster modify -H kvm:cpu_sockets=1
```

### Change the NIC type: nic_type

This parameter determines the way the network cards are presented to the instance.

```bash
# Use paravirtual
gnt-cluster modify -H kvm:nic_type=paravirtual

# Use e1000
gnt-cluster modify -H kvm:nic_type=e1000
```

### Change the VGA type: vga

Sets the emulated VGA mode, passed to the `kvm -vga` option.

```bash
gnt-cluster modify -H kvm:vga="std"
```

### Change the keymap: keymap

Specifies the keyboard mapping to use. It is only needed when using the VNC console.

```
gnt-cluster modify -H kvm:keymap=ja
```

### Extra option for KVM: kvm_extra

Specifies additional options for the KVM hypervisor.

```bash
# For example:
# - Enable KVM: -enable-kvm
# - Add virtio-rng device: -device virtio-rng-pci\,bus=pci.0\,addr=0x1e\,max-bytes=1024\,period=1000
# - Set video memory(MB): -global VGA.vgamem_mb=64
gnt-cluster modify -H kvm:kvm_extra="-enable-kvm -device virtio-rng-pci\,bus=pci.0\,addr=0x1e\,max-bytes=1024\,period=1000 -global VGA.vgamem_mb=64"
```

## Verifying the cluster

**Mandatory** on master node.

```bash
gnt-cluster verify
```

## Joining the nodes to the cluster

**Mandatory** on master node.

After you initialize your cluster, join the other nodes
to it by running the following command on the master
node.

```bash
gnt-node add <NODENAME>

# Example of adding node02
gnt-node add node2

# Example of adding node03
gnt-node add node3

... and more nodes.
```

**Troubleshooting**

- `gnt-node add node2` returns with the error:

```
Node daemon on node2.example.com didn't answer queries within 10.0 seconds
```

Ensure that port 1811 is open (`ss -anpt | grep 1811`).

- `gnt-cluster verify` on master returns an error after `Verifying node status`:

```
ERROR: node node2.example.com: ssh communication with node 'node1.example.com': ssh problem: ssh_exchange_identification: read: Connection reset by peer\'r\n
```

Test manual SSH connections from node2 to node1 and vice versa.

## Manage Ganeti services

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

- Setting up RHEL/AlmaLinux/CentOS/Rocky Linux/others

We recommend using [Ganeti Instance Image](https://github.com/osuosl/ganeti-instance-image) ([yum repository](http://ftp.osuosl.org/pub/osl/ganeti-instance-image/yum/)).

- Setting up Debian (requires ganeti-instance-debootstrap)

Installation succeeds, but the `gnt-instance console` command does not work.

```bash
gnt-instance add -t drbd -n node1:node2 -o debootstrap+default --disk 0:size=8G -B vcpus=2,maxmem=1024,minmem=512 instance1

# With no check, no start, and no install
gnt-instance add -t drbd -n node2:node1 -o debootstrap+default --disk 0:size=8G -B vcpus=2,maxmem=1024,minmem=512 --no-ip-check --no-name-check --no-start --no-install instance3.example.com
```

### Install a custom OS from an ISO file

Enable VNC and check the VNC port of the created instance:

```bash
# gnt-cluster modify -H kvm:vnc_bind_address=0.0.0.0

# gnt-instance info instance3.example.com | grep "console connection"
  console connection: vnc to node2.example.com:11001 (display 5101)
```

Start the instance from an ISO image:

```bash
gnt-instance start -H boot_order=cdrom,cdrom_image_path=/path/to/install.iso instance3.example.com
```

Connect to `node2.example.com:11001` using a VNC client and follow the on-screen instructions to complete the installation.

