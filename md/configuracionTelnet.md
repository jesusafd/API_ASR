# activacion telnet
configure terminal
enable password admin
username admin password 0 admin
line vty 0 4
logging synchronous
login local
transport input telnet
end 
wr

# baja telnet
conf t
line vty 0 4
no transport input
transport input ssh
end
wr

