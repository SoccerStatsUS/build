# Source
# https://www.linode.com/docs/security/securing-your-server


# Add the user

adduser chris
usermod -a -G sudo chris
logout

ssh chris@put.your.ip.here


# ssh

ssh-keygen
scp ~/.ssh/id_rsa.pub chris@123.456.78.90:

mv id_rsa.pub .ssh/authorized_keys

chown -R example_user:example_user .ssh
chmod 700 .ssh
chmod 600 .ssh/authorized_keys




