#!/bin/bash
echo "create iso in bin folder"
cd /opt/Ipxe/ipxe-1e5c5a2/src/
make bin/ipxe.iso  builtin/buildarch=x86_64 TRUST=../../scripts/certs/localhost.crt EMBED=../../scripts/nic-menu_test.ipxe
echo "iso creation terminated "
cd bin
mv ipxe.iso /tmp/ipxe_test.iso
echo "you can get the iso in  /tmp/ipxe_test.iso"
ls -lah /tmp | grep ipxe_test
exit 0
