<?php
list($empty,$os,$version,$host_name,$domain_name,$ks_filename) = 
    explode("/",$_SERVER['PATH_INFO']);
header("Content-Type: text/plain"); # important, otherwise kickstart fails
?>
# Kickstart_test file automatically generated by my script.
#parameter1=<?php echo $empty;?>
#
#parameter2-os=<?php echo $os;?>

#parameter3-version=<?php echo $version;?>

#parameter4-hostname=<?php echo $host_name;?>

#parameter5-domain_name=<?php echo $domain_name;?>

#parameter6-ks_filename=<?php echo $ks_filename;?>

#version=<?php echo $version;?>

install
#url --url=http://yumsrv01.dprod.net/repo/rhel/7/x86_64/u2/
url --url=http://212.7.73.139/repo/rhel/7/x86_64/u2/
#lang en_US.UTF-8
#keyboard us
#network --device eth0 --bootproto dhcp --hostname <?php echo $hostname;?>
# ... rest of kickstart parameters


#da testare
#interactive

# autostep (optional)    Similar to interactive except it goes to the next screen for you. It is used mostly for debugging.
#--autoscreenshot � Take a screenshot at every step during installation and copy the images over to /root/anaconda-screenshots after installation is complete. This is most useful for documentation. 
autostep --autoscreenshot 


lang en_US
keyboard it
timezone Europe/Rome --isUtc
rootpw $1$YgOl7zsS$4Q5cKi6zWaY.o81tyGEk.. --iscrypted
#platform x86, AMD64, or Intel EM64T
reboot
#cdrom
bootloader --location=mbr --append="rhgb quiet ipv6.disable=1 crashkernel=auto" --boot-drive=sda
#zerombr
autopart --type=lvm
clearpart --all --drives=sda --initlabel
#volgroup lv_ol_<?php echo $host_name;?> --pesize=4096 pv.0 
#part pv.0 --fstype=lvmpv --ondisk=sda --size=571693
#part /boot --fstype=ext4 --size=300 --asprimary
#part /boot/efi --fstype=ext4 --size=300
#logvol swap --vgname=lv_<?php echo $host_name;?> --name=lv_swap --fstype=swap --size=16384
#logvol /var --vgname=lv_<?php echo $host_name;?> --name=lv_var --fstype=ext4 --size=10240
#logvol /tmp --vgname=lv_<?php echo $host_name;?> --name=lv_tmp --fstype=ext4 --size=10240
#logvol /var/log --vgname=lv_<?php echo $host_name;?> --name=lv_varlog --fstype=ext4 --size=10240
#logvol /var/log/audit --vgname=lv_<?php echo $host_name;?> --name=lv_varlogaudit --fstype=ext4 --size=5120
#logvol /u01 --vgname=lv_<?php echo $host_name;?> --name=lv_u01 --fstype=ext4 --size=213647
#logvol /u02 --vgname=lv_<?php echo $host_name;?> --name=lv_u02 --fstype=ext4 --size=213647
#auth --passalgo=sha512
#selinux --disabled
#firewall --disabled
#firstboot --disable

%pre
#here there is the pre installation script
%end

%post --nochroot
#here there is the post installation script
%end

%packages
@debugging
@perl-runtime
@java-platform
@hardware-monitoring
@performance
@console-internet
@large-systems
@base
@system-admin-tools
@gnome-desktop
@fonts
@desktop-debugging
@x11
%end
