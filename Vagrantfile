# -*- mode: ruby -*-
# vi: set ft=ruby :


GRANTFILE_API_VERSION = "2"
INIT_SCRIPT = "bootstrap.sh"

Vagrant.configure(GRANTFILE_API_VERSION) do |config|
  config.vm.box = "ubuntu/trusty64"

  config.vm.provision :shell, path: INIT_SCRIPT

  # config.vm.network :forwarded_port, guest: 80, host: 8888
end
