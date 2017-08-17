#!/bin/bash
echo "create iso in bin folder"
cd /root/INSTALL/REPO/Git/Ipxe/ipxe-1e5c5a2/src/
make bin/ipxe.iso  builtin/buildarch=x86_64 EMBED=../../scripts/nic-menu.ipxe
echo "iso creation terminated "
cd bin
mv ipxe.iso /tmp
echo "you can get the iso in  /tmp/ipxe.iso"
ls -lah /tmp | grep ipxe
exit 0
