### You should add these settings on both sides: sshd & ssh client

For sshd:

ClientAliveInterval 20
ClientAliveCountMax 5

For ssh client:

Host *
  ServerAliveInterval 30
  ServerAliveCountMax 5