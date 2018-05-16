### You should add these settings on both sides: sshd & ssh client

For server machine
sshd:

ClientAliveInterval 20 . 
ClientAliveCountMax 5 . 

sysctl.conf:

net.ipv4.conf.all.proxy_arp=1 . 
net.ipv4.conf.all.forwarding=1 . 

For client machine:

~/.ssh/config:

Host * . 
ServerAliveInterval 30 . 
ServerAliveCountMax 5

