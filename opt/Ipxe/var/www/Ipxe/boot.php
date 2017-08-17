#!ipxe
# Variables are specified in boot.ipxe.cfg Some menu defaults
set server_name CRIFNET_BOOT_SERVER
set menu-timeout 100000 
set server_protocol_insecure http://
set server_protocol https://
#set server_ip 10.0.18.178
set server_ip poclinuxmaster.crifnet.com
set submenu-timeout ${menu-timeout} 
set client_hostname <?php echo $_GET['hostname']; echo "\n" ?>
set client_domain_name <?php echo $_GET['domain_name']; echo "\n" ?>
set client_ip <?php echo $_GET['client_ip']; echo "\n" ?>
set client_netmask <?php echo $_GET['client_netmask']; echo "\n" ?>
set client_gateway <?php echo $_GET['client_gateway']; echo "\n" ?>
set client_dns <?php echo $_GET['client_dns']; echo "\n" ?>
set client_network_mac <?php echo $_GET['client_network_mac']; echo "\n" ?>

isset ${menu-default} || set menu-default exit

###################### MAIN MENU ####################################
:start
menu iPXE boot menu: ${server_name} 
item --gap -- ------------------------- Operating systems ------------------------------ 
item --key e redhat_menu R(e)d Hat  Enterprise Linux install 
item --key o oracle_menu (O)racle Linux install
item --key t centos_menu Cen(t)OS Linux install
item --key s settings Configure RedHat installation (S)ettings 
item --gap -- ------------------------- Advanced options ------------------------------- 
item --key c config (C)onfigure iPXE settings 
item --key h shell Drop to iPXE s(h)ell 
item --key r reboot (R)eboot computer 
item --gap
item --key x exit E(x)it iPXE and continue BIOS boot 
item --gap
item --gap -- ------------------------- Client status ----------------------------------
item --gap hostname:    ${client_hostname}
item --gap domain:      ${client_domain_name}
item --gap ip address:  ${client_ip}
item --gap netmask:     ${client_netmask}
item --gap gateway:     ${client_gateway}
item --gap dns address: ${client_dns}
item --gap mac address: ${client_network_mac}
item --gap -- -------------------------------------------------------------------------- 
choose --timeout ${menu-timeout} --default ${menu-default} selected || goto cancel 
set menu-timeout 0
goto ${selected}

:back
set submenu-timeout 0 
clear submenu-default 
goto start

:redhat_menu
set os RedHat
menu iPXE boot menu: ${server_name}
item --gap -- ------------------------ Red Hat Enterprise Linux --------------------------
item --key 1 redhat_67 1) Red Hat Enterprise Linux v. 6.7
item --key 2 redhat_68 2) Red Hat Enterprise Linux v. 6.8
item --key 3 redhat_69 3) Red Hat Enterprise Linux v. 6.9
item --key 4 redhat_70 4) Red Hat Enterprise Linux v. 7.0
item --key 5 redhat_71 5) Red Hat Enterprise Linux v. 7.1
item --key 6 redhat_72 6) Red Hat Enterprise Linux v. 7.2
item --key 7 redhat_73 7) Red Hat Enterprise Linux v. 7.3
item --gap -- ----------------------------------------------------------------------------
item --key b back (B)ack to main menu
item --gap
choose --timeout ${menu-timeout} --default ${menu-default} selected || goto cancel
set menu-timeout 0
goto ${selected}

:redhat_67
set version 6.7
goto redhat_install

:redhat_68
set version 6.8
goto redhat_install

:redhat_69
set version 6.9
goto redhat_install

:redhat_70
set version 7.0
goto redhat_install

:redhat_71
set version 7.1
goto redhat_install

:redhat_72
set version 7.2
goto redhat_install

:redhat_73
set version 7.3
goto redhat_install

:oracle_menu
set os Oracle
menu iPXE boot menu: ${server_name}
item --gap -- --------------------------- Oracle Linux --------------------------------
item --key 1 oracle_67 1) Oracle Linux v. 6.7
item --key 2 oracle_68 2) Oracle Linux v. 6.8
item --key 3 oracle_69 3) Oracle Linux v. 6.9
item --key 4 oracle_70 4) Oracle Linux v. 7.0
item --key 5 oracle_71 5) Oracle Linux v. 7.1
item --key 6 oracle_72 6) Oracle Linux v. 7.2
item --key 7 oracle_73 7) Oracle Linux v. 7.3

item --gap -- -------------------------------------------------------------------------
item --key b back (B)ack to main menu
item --gap
choose --timeout ${menu-timeout} --default ${menu-default} selected || goto cancel
set menu-timeout 0
goto ${selected}

:oracle_67
set version 6.7
goto oracle_install

:oracle_68
set version 6.8
goto oracle_install

:oracle_69
set version 6.9
goto oracle_install

:oracle_70
set version 7.0
goto oracle_install

:oracle_71
set version 7.1
goto oracle_install

:oracle_72
set version 7.2
goto oracle_install

:oracle_73
set version 7.3
goto oracle_install


:centos_menu
set os Centos
menu iPXE boot menu: ${server_name}
item --gap -- --------------------------- CentOS Linux ---------------------------------
item --key 1 centos_67 1) CentOS Linux v. 6.7
item --key 2 centos_68 2) CentOS Linux v. 6.8
item --key 3 centos_69 3) CentOS Linux v. 6.9
item --key 4 centos_70 4) CentOS Linux v. 7.0
item --key 5 centos_71 5) CentOS Linux v. 7.1
item --key 6 centos_72 6) CentOS Linux v. 7.2
item --key 7 centos_73 7) CentOS Linux v. 7.3
item --gap -- --------------------------------------------------------------------------
item --key b back (B)ack to main menu
item --gap
choose --timeout ${menu-timeout} --default ${menu-default} selected || goto cancel
set menu-timeout 0
goto ${selected}

:centos_67
set version 6.7
goto centos_install

:centos_68
set version 6.8
goto centos_install

:centos_69
set version 6.9
goto centos_install

:centos_70
set version 7.0
goto centos_install

:centos_71
set version 7.1
goto centos_install

:centos_72
set version 7.2
goto centos_install

:centos_73
set version 7.3
goto centos_install

:cancel
echo You cancelled the menu, dropping you to a shell

:shell
shell

:failed
echo Booting failed, dropping to shell 
goto shell

:reboot
reboot

:exit
exit

:config
config 
goto start


:redhat_install
#insert specific Red Hat Configuration
goto install
goto back

:oracle_install
goto install
goto back

:centos_install
goto install
goto back

:install
set kickstart_filename ${server_protocol}${server_ip}/kickstart/${os}/${version}/${client_hostname}/${client_domain_name}/ks.cfg

#for testing 
echo ${kickstart_filename}
#echo ${server_protocol}${server_ip}/Ipxe/boot/${os}/${version}/images/pxeboot/vmlinuz
#echo ${server_protocol}${server_ip}/Ipxe/boot/${os}/${version}/images/pxeboot/initrd.img ip=${client_ip} inst.repo=http://212.7.73.139/repo/rhel/7/x86_64/u2/ ks=${kicktart_filename}
prompt
#end testing block


#ifname=
#    Assigns a given interface name to a network device with a given MAC address. Can be used multiple times. The syntax is ifname=interface:MAC. For example:

#    ifname=eth0:01:23:45:67:89:ab
#ip=ip::gateway:netmask:hostname:interface:none
 
#kernel ${server_protocol}${server_ip}/Ipxe/boot/${os}/${version}/images/pxeboot/vmlinuz initrd=initrd
#initrd ${server_protocol}${server_ip}/kickstart/${os}/${version}/images/pxeboot/initrd.img \
       ks=${server_protocol}${server_ip}/kickstart/${os}/${version}/${client_hostname}.${client_domain_name}/ks.cfg
#initrd ${server_protocol}${server_ip}/Ipxe/boot/${os}/${version}/images/pxeboot/initrd.img ksdevice=eth0 ip=${client_ip} inst.repo=http://212.7.73.139/repo/rhel/7/x86_64/u2/ ks=${kicktart_filename}
#kernel ${server_protocol}${server_ip}/Ipxe/boot/${os}/${version}/images/pxeboot/vmlinuz initrd=initrd inst.repo=${server_protocol}${server_ip}/Ipxe/boot/${os}/${version}/rhel-server-7.2-x86_64-dvd.iso

initrd ${server_protocol}${server_ip}/Ipxe/boot/${os}/${version}/images/pxeboot/initrd.img  
#kernel ${server_protocol}${server_ip}/Ipxe/boot/${os}/${version}/images/pxeboot/vmlinuz initrd=initrd ifname=eth0:${client_network_mac} ip=${client_ip}::${client_gateway}:${client_netmask}:${client_hostname}:eth0:none inst.repo=http://212.7.73.139/repo/rhel/7/x86_64/u2/ inst.ks==${kicktart_filename}

#kernel ${server_protocol}${server_ip}/Ipxe/boot/${os}/${version}/images/pxeboot/vmlinuz initrd=initrd ifname=eth0:${client_network_mac} ip=${client_ip}::${client_gateway}:${client_netmask}:${client_hostname}:eth0:none inst.ks.sendmac inst.ks=${server_protocol}${server_ip}/Ipxe/boot/${os}/${version}/ks.cfg
#local repo
#kernel ${server_protocol}${server_ip}/Ipxe/boot/${os}/${version}/images/pxeboot/vmlinuz initrd=initrd ifname=eth99:${client_network_mac} ip=${client_ip}::${client_gateway}:${client_netmask}:${client_hostname}:eth99:none inst.repo=${server_protocol}${server_ip}/Ipxe/boot/${os}/${version} inst.ks.sendmac inst.ks=${kicktart_filename} 

kernel ${server_protocol}${server_ip}/Ipxe/boot/${os}/${version}/images/pxeboot/vmlinuz initrd=initrd ifname=eth99:${client_network_mac} ip=${client_ip}::${client_gateway}:${client_netmask}:${client_hostname}:eth99:none inst.ks.sendmac inst.ks=${server_protocol}${server_ip}/kickstart/${os}/${version}/${client_hostname}/${client_domain_name}/ks.cfg 
boot
goto back
