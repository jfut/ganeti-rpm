Ganeti installation tutorial for RHEL/CentOS/Scientific Linux
=============================================================

This documentation is the short version for RHEL/CentOS/Scientific Linux.

Official full version:

* `Ganeti's documentation <http://docs.ganeti.org/ganeti/current/html/>`_ >> `Ganeti installation tutorial <http://docs.ganeti.org/ganeti/current/html/install.html>`_


Installing the base system
++++++++++++++++++++++++++

**Mandatory** on all nodes.

Note that Ganeti requires the hostnames of the systems.

ex) ``/etc/hosts``::

  127.0.0.1       localhost
  # cluster name
  192.168.1.1     gcluster
  # node names
  192.168.1.11    node1.example.com node1
  192.168.1.12    node2.example.com node2
  # instance names
  192.168.1.101   instance1.example.com instance1
  192.168.1.102   instance2.example.com instance2

Installing The Hypervisor
+++++++++++++++++++++++++

**Mandatory** on all nodes.

- KVM on RHEL/CentOS/Scientific Linux

::

  yum install kvm kvm-qemu-img python-virtinst

- Xen on RHEL/CentOS/Scientific Linux

::

  yum install xen

KVM settings
~~~~~~~~~~~~

- KVM on RHEL/CentOS/Scientific Linux

**Mandatory** on all nodes.

Service configuration::

  chkconfig messagebus on
  chkconfig libvirtd on
  chkconfig libvirt-guests off

Create bridge interface

- ex) br0 (eth0)

Edit ``/etc/sysconfig/network-scripts/ifcfg-eth0``::

  DEVICE="eth0"
  BOOTPROTO="static"
  HWADDR="??:??:??:??:??:??"
  ONBOOT="yes"
  BRIDGE="br0"

Edit ``/etc/sysconfig/network-scripts/ifcfg-br0``::

  DEVICE="br0"
  TYPE=Bridge
  BOOTPROTO="static"
  IPADDR="192.168.1.11"
  NETMASK="255.255.255.0"
  ONBOOT="yes"

Apply network configurations.::

   /etc/init.d/network restart

Allow to bridge interface access.

Edit ``/etc/sysconfig/iptables``::

  *filter
  ...
  -A INPUT -j REJECT --reject-with icmp-host-prohibited
  ## FORWARD
  -A FORWARD -m physdev --physdev-is-bridged -j ACCEPT
  COMMIT

Apply firewall rules.::

  iptables-restore < /etc/sysconfig/iptables

Xen settings
~~~~~~~~~~~~

- Xen on RHEL/CentOS/Scientific Linux

**Mandatory** on all nodes.

Service configuration::

  chkconfig xend on
  chkconfig xendomains on
  chkconfig libvirtd off

Edit ``/etc/xen/xend-config.sxp``::

  (dom0-min-mem 0)
  (xend-relocation-server yes)
  (xend-relocation-port 8002)
  (xend-relocation-hosts-allow '')

Add dom0_mem to ``/etc/grub.conf``::

  title CentOS (2.6.18-xxx.xx.x.el5xen)
        root (hd0,0)
        kernel /xen.gz-2.6.18-xxx.xx.x.el5 dom0_mem=512M
        module /vmlinuz-2.6.18-xxx.xx.x.el5xen ro root=/dev/VolGroup00/HostRoot
        module /initrd-2.6.18-xxx.xx.x.el5xen.img

You need to restart the Xen daemon for these settings to take effect::

  /etc/init.d/xend restart

After installing either hypervisor, you need to reboot into your new 
system. On some distributions this might involve configuring GRUB 
appropriately, whereas others will configure it automatically when you 
install the respective kernels.::

  reboot

Setup a kernel for an instance::

  cd /boot
  ln -s vmlinuz-`uname -r` vmlinuz-2.6-xenU

Installing DRBD
+++++++++++++++

**Mandatory** on all nodes.

- RHEL/CentOS/Scientific Linux

Install ELRepo repository to install the drbd package.

::

  rpm --import http://elrepo.org/RPM-GPG-KEY-elrepo.org
  rpm -Uvh http://elrepo.org/elrepo-release-6-3.el6.elrepo.noarch.rpm
  sed -i "s/enabled = 1/enabled = 0/g" /etc/yum.repos.d/elrepo.repo

Install DRBD package::

  yum --enablerepo=elrepo install drbd83-utils kmod-drbd83

- DRBD 8.3.0 or later

Create ``/etc/default/drbd``::

  ADD_MOD_PARAM="usermode_helper=/bin/true"

Installing other required software
++++++++++++++++++++++++++++++++++

Install EPEL Rrepository.

ex) Scientific Linux::

  yum install yum-conf-epel
  sed -i "s/enabled = 1/enabled = 0/g" /etc/yum.repos.d/epel.repo

Install other required software::

 yum --enablerepo=epel install pyOpenSSL python-simplejson pyparsing python-inotify python-ctypes python-pycurl python-paramiko debootstrap

Install other required software for KVM::

  yum --enablerepo=epel socat

Optional: Install to support htools. See: `HTOOLS(1) Ganeti <http://docs.ganeti.org/ganeti/2.6/man/htools.html>`_.

- **RHEL/CentOS/Scientific Linux 6.x or later only**

::

  yum --enablerepo=epel ghc ghc-curl ghc-json ghc-network ghc-parallel
  wget http://jfut.integ.jp/linux/ganeti/x86_64/ghc-curl-1.3.8-1.el6.x86_64.rpm
  rpm -ivh ghc-curl-1.3.8-1.el6.x86_64.rpm

Optional: Install to support CPU Pinning for KVM. See: `Ganeti CPU Pinning <http://docs.ganeti.org/ganeti/2.6/html/design-cpu-pinning.html>`_.

- KVM on RHEL/CentOS/Scientific Linux 6.x

::

  wget http://jfut.integ.jp/linux/ganeti/x86_64/python-affinity-0.1.0-1.el6.x86_64.rpm
  rpm -ivh python-affinity-0.1.0-1.el6.x86_64.rpm

- KVM on RHEL/CentOS/Scientific Linux 5.x

::

  wget http://jfut.integ.jp/linux/ganeti/x86_64/python-affinity-0.1.0-1.el5.x86_64.rpm
  rpm -ivh python-affinity-0.1.0-1.el5.x86_64.rpm

Configuring LVM
+++++++++++++++

**Mandatory** on all nodes.

The volume group is required to be at least 20GiB.

If you haven't configured your LVM volume group at install time you
need to do it before trying to initialize the Ganeti cluster. This is
done by formatting the devices/partitions you want to use for it and
then adding them to the relevant volume group::

  pvcreate /dev/sda3
  vgcreate vmvg /dev/sda3

or::

  pvcreate /dev/sdb1
  pvcreate /dev/sdc1
  vgcreate vmvg /dev/sdb1 /dev/sdc1

If you want to add a device later you can do so with the *vgextend*
command::

  pvcreate /dev/sdd1
  vgextend vmvg /dev/sdd1

Optional: it is recommended to configure LVM not to scan the DRBD
devices for physical volumes. This can be accomplished by editing
``/etc/lvm/lvm.conf`` and adding the
``/dev/drbd[0-9]+`` regular expression to the
``filter`` variable, like this::

  filter = ["r|/dev/cdrom|", "r|/dev/drbd[0-9]+|" ]

Installing Ganeti
+++++++++++++++++

**Mandatory** on all nodes.

- RHEL/CentOS/Scientific Linux 6.x

::

  wget http://jfut.integ.jp/linux/ganeti/x86_64/ganeti-2.6.2-2.el6.x86_64.rpm
  wget http://jfut.integ.jp/linux/ganeti/noarch/ganeti-instance-debootstrap-0.12-1.el6.noarch.rpm
  rpm -ivh ganeti-2.6.2-2.el6.x86_64.rpm ganeti-instance-debootstrap-0.12-1.el6.noarch.rpm

Optional: Install to support htools.

::

  wget http://jfut.integ.jp/linux/ganeti/x86_64/ganeti-htools-2.6.2-2.el6.x86_64.rpm
  rpm -ivh ganeti-htools-2.6.2-2.el6.x86_64.rpm

- RHEL/CentOS/Scientific Linux 5.x

::

  wget http://jfut.integ.jp/linux/ganeti/x86_64/ganeti-2.6.2-2.el5.x86_64.rpm
  wget http://jfut.integ.jp/linux/ganeti/noarch/ganeti-instance-debootstrap-0.12-1.el5.noarch.rpm
  rpm -ivh ganeti-2.6.2-2.el5.x86_64.rpm ganeti-instance-debootstrap-0.12-1.el5.noarch.rpm

Upgrade notes
+++++++++++++

**Mandatory** on all nodes.

Stop ganeti service and backup the configuration file.

::

  /etc/init.d/ganeti stop
  tar czf /var/lib/ganeti-$(date +%FT%T).tar.gz -C /var/lib ganeti

Install new Ganeti version on all nodes.

**Mandatory** on master node.

Update the configuration file.

::

  /usr/lib/ganeti/tools/cfgupgrade --verbose --dry-run
  /usr/lib/ganeti/tools/cfgupgrade --verbose
      This script upgrade the configuration files(/var/lib/ganeti).
  /etc/init.d/ganeti start
  gnt-cluster redist-conf
  /etc/init.d/ganeti restart
  gnt-cluster verify

- Update from Ganeti 2.5 to 2.6

Set default metavg parameter for DRBD disk::

  gnt-cluster modify -D drbd:metavg=vmvg

Initializing the cluster
++++++++++++++++++++++++

**Mandatory** on one node per cluster.

Initialize a cluster.

Example::

  gnt-cluster init --vg-name <VOLUMEGROUP> --master-netdev <MASTERINTERFACE> --nic-parameters link=<BRIDGEINTERFACE> <CLUSTERNAME>

- KVM

Example for KVM::

  gnt-cluster init --vg-name vmvg --master-netdev <MASTERINTERFACE> --enabled-hypervisors kvm --nic-parameters link=<BRIDGEINTERFACE> gcluster
  ex) gnt-cluster init --vg-name vmvg --master-netdev eth0 --enabled-hypervisors kvm --nic-parameters link=br0 gcluster

- Xen

Example for Xen::

  gnt-cluster init --vg-name vmvg --master-netdev <MASTERINTERFACE> --nic-parameters link=<BRIDGEINTERFACE> gcluster
  ex) gnt-cluster init --vg-name vmvg --master-netdev eth0 --nic-parameters link=xenbr0 gcluster

Set default metavg parameter for DRBD disk

::

  gnt-cluster modify -D drbd:metavg=vmvg

Enable use_bootloader for using VM's boot loader.

- KVM

::

  gnt-cluster modify --hypervisor-parameters kvm:kernel_path=

- Xen

::

  gnt-cluster modify --hypervisor-parameters xen-pvm:use_bootloader=True


Joining the nodes to the cluster
++++++++++++++++++++++++++++++++

**Mandatory** for all the other nodes.

After you have initialized your cluster you need to join the other nodes
to it. You can do so by executing the following command on the master
node::

  gnt-node add <NODENAME>
  gnt-node add node2

Setting up and managing virtual instances
+++++++++++++++++++++++++++++++++++++++++

**Mandatory** on master node.

Setting up virtual instances
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- Setting up RHEL/CentOS/Scientific Linux

I recommend to use Ganeti Instance Image.

- `Ganeti Instance Image <http://code.osuosl.org/projects/ganeti-image/>`_

- Setting up Debian

Installation will be successful, but gnt-instance console doesn't work.

::

  gnt-instance add -t drbd -n node1:node2 -o debootstrap+default --disk 0:size=8G -B vcpus=2,maxmem=1024,minmem=512 instance1

