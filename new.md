# Source
# https://www.linode.com/docs/security/securing-your-server

* Update ~/.ssh/config


# Add the user

* adduser chris # Set password, user info interactively
* usermod -a -G sudo chris # Add chris to sudo group
* logout

* ssh chris@put.your.ip.here


# ssh

* ssh-keygen # Where do I run this? Locally or remotely? 
* scp ~/.ssh/id_rsa.pub chris@put.your.ip.here: # Seems local, but I probably have a key already.
* mv id_rsa.pub .ssh/authorized_keys # But .ssh hasn't been generated yet?

# Are these necessary?
chown -R example_user:example_user .ssh
chmod 700 .ssh
chmod 600 .ssh/authorized_keys




