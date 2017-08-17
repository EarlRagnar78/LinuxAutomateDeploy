#!/bin/bash
echo "create iso in bin folder"
cd /opt/Ipxe/ipxe-src/src/
make bin/ipxe.iso  builtin/buildarch=x86_64 DEBUG=tls,x509,certstore,privkey CERT=/var/www/ca/ca.pem,/opt/Ipxe/scripts/Certificate/full-chain.pem,/opt/Ipxe/scripts/Certificate/client/client.pem,/opt/Ipxe/scripts/Certificate/ca/ca.pem,/opt/Ipxe/scripts/Certificate/ca/ca-root-crif.pem  PRIVKEY=/opt/Ipxe/scripts/Certificate/client/client.key TRUST=/opt/Ipxe/scripts/Certificate/ca/ca-root-crif.pem  EMBED=../../scripts/nic-menu_test.ipxe
#make bin/ipxe.iso  builtin/buildarch=x86_64 DEBUG=tls,x509,certstore,privkey EMBED=../../scripts/nic-menu_test.ipxe PRIVKEY=client.key TRUST=ca.crt CERT=server.crt 
 
#make bin/ipxe.iso  builtin/buildarch=x86_64 DEBUG=tls,x509,certstore,privkey CERT=/var/www/ca/ca.pem,/opt/Ipxe/scripts/Certificate/full-chain.pem,/opt/Ipxe/scripts/Certificate/client/client.pem,/opt/Ipxe/scripts/Certificate/ca/ca.pem,/opt/Ipxe/scripts/Certificate/ca/ca-root-crif.pem  PRIVKEY=/opt/Ipxe/scripts/Certificate/client/client.key TRUST=/opt/Ipxe/scripts/Certificate/ca/ca-root-crif.pem  EMBED=../../scripts/nic-menu.ipxe
echo "iso creation terminated "
cd bin
mv ipxe.iso /tmp/ipxe_debug.iso
echo "you can get the iso in  /tmp/ipxe_debug.iso"
ls -lah /tmp | grep ipxe
exit 0
