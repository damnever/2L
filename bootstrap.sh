#!/bin/bash
#
# Reference: https://github.com/Damnever/setup
#

redis="http://download.redis.io/redis-stable.tar.gz"

sudo apt-get update
sudo apt-get -y install make build-essential wget curl git python-pip \
    libssl-dev zlib1g-dev libbz2-dev libreadline-dev libsqlite3-dev \
    llvm libncurses5-dev nginx

# mysql
sudo debconf-set-selections <<< 'mysql-server mysql-server/root_password password DXC'
sudo debconf-set-selections <<< 'mysql-server mysql-server/root_password_again password DXC'
sudo apt-get -y install mysql-server libmysqlclient-dev

# redis
wget ${redis} -O redis-stable.tar.gz
tar -xvzf redis-stable.tar.gz
cd redis-stable
make
sudo cp src/redis-server /usr/local/bin/
sudo cp src/redis-cli /usr/local/bin/
sudo mkdir /etc/redis
sudo mkdir /var/redis
sudo cp utils/redis_init_script /etc/init.d/redis_6379
sudo sed -i '/REDISPORT=/c\REDISPORT=6379' /etc/init.d/redis_6379
sudo cp redis.conf /etc/redis/6379.conf
sudo mkdir /var/redis/6379
sudo sed -i '/^daemonize*/c\daemonize yes' /etc/redis/6379.conf
sudo sed -i '/^pidfile*/c\pidfile \/var\/run\/redis_6379\.pid' /etc/redis/6379.conf
sudo sed -i '/^port*/c\port 6379' /etc/redis/6379.conf
sudo sed -i '/^loglevel*/c\loglevel debug' /etc/redis/6379.conf
sudo sed -i '/^logfile*/c\logfile \/var\/log\/redis_6379\.log' /etc/redis/6379.conf
sudo sed -i '/^dir*/c\dir \/var\/redis\/6379' /etc/redis/6379.conf
sudo update-rc.d redis_6379 defaults
sudo /etc/init.d/redis_6379 start
rm -r redis-stable

# pyenv
git clone https://github.com/yyuu/pyenv.git ~/.pyenv
echo '\n# Setup pyenv' >> $HOME/.bashrc
echo 'export PATH=/usr/local/p/versions/python:$PATH' >> $HOME/.bashrc
echo 'export PYENV_ROOT="$HOME/.pyenv"' >> $HOME/.bashrc
echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> $HOME/.bashrc
echo 'eval "$(pyenv init -)"' >> $HOME/.bashrc
exec $SHELL

git clone https://github.com/yyuu/pyenv-virtualenvwrapper.git ~/.pyenv/plugins/pyenv-virtualenvwrapper
pyenv virtualenvwrapper
echo 'export PYENV_VIRTUALENVWRAPPER_PREFER_PYVENV="true"' >> $HOME/.bashrc

pyenv install 2.7.11
pyenv global 2.7.11

pip install --upgrade pip

ln -s $(pwd)/tpl_settings.py $(pwd)/app/settings.py

pip install -e .


# supervisor
pip install supervisor
sudo mkdir /var/log/supervisor/
sudo supervisord -c $(pwd)/supervisord.conf

# nginx
sudo nginx -c $(pwd)/nginx.conf
