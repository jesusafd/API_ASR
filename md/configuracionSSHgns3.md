# COnfiguracion ssh para los routers
configure terminal
ip domain-name a.escom.ipn.mx
ip ssh rsa keypair-name sshkey
crypto key generate rsa usage-keys label sshkey modulus 1024
ip ssh v 2
ip ssh time-out 30
ip ssh authentication-retries 3
line vty 0 15
password admin
login local
transport input ssh
exit
username admin privilege 15 password admin
end
wr

# Baja ssh
conf t
line vty 0 15
no transport input
transport input telnet
end
wr