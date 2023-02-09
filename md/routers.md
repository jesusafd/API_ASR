# R1
configure t
int f0/0
ip add 10.0.1.1 255.255.255.0
no sh
exit
int f1/0
ip add 10.0.2.2 255.255.255.0
no sh
exit
int f2/0
ip add 10.0.3.2 255.255.255.0
no sh
exit
int f3/0
ip add 10.0.4.2 255.255.255.0
no sh
end
wr

# R2
configure t
int f1/0
ip add 10.0.2.1 255.255.255.0
no sh
exit
int f0/0
ip add 10.0.5.1 255.255.255.0
no sh
end
wr

# R3
configure t
int f2/0
ip add 10.0.3.1 255.255.255.0
no sh
exit
int f0/0
ip add 10.0.6.1 255.255.255.0
no sh
end
wr

# R4
configure t
int f3/0
ip add 10.0.4.1 255.255.255.0
no sh
exit
int f0/0
ip add 10.0.7.1 255.255.255.0
no sh
end
wr

# PC1
ip 10.0.5.2 255.255.255.0 10.0.5.1
save

# PC2
ip 10.0.6.2 255.255.255.0 10.0.6.1
save

# PC3
ip 10.0.7.2 255.255.255.0 10.0.7.1
save
