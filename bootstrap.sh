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
# http://stackoverflow.com/questions/3513773/change-mysql-default-character-set-to-utf-8-in-my-cnf
sudo echo "[client]" >> /etc/mysql/my.cnf
sudo echo "default-character-set=utf8" >> /etc/mysql/my.cnf
sudo echo "" >> /etc/mysql/my.cnf
sudo echo "[mysql]" >> /etc/mysql/my.cnf
sudo echo "default-character-set=utf8" >> /etc/mysql/my.cnf
sudo echo "" >> /etc/mysql/my.cnf
sudo echo "[mysqld]" >> /etc/mysql/my.cnf
sudo echo "collation-server = utf8_unicode_ci" >> /etc/mysql/my.cnf
sudo echo "init-connect='SET NAMES utf8'" >> /etc/mysql/my.cnf
sudo echo "character-set-server = utf8" >> /etc/mysql/my.cnf
sudo /etc/init.d/mysql restart

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
cd -
rm ${redis}
rm -r redis-stable

sudo pip install virtualenvwrapper
source /usr/local/bin/virtualenvwrapper.sh
mkvirtualenv 2L
pip install --upgrade pip
pip install -r requirements.txt
ln -s $(pwd)/tpl_settings.py $(pwd)/app/settings.py
pip install -e .

2L initdb


# supervisor
pip install supervisor
sudo mkdir /var/log/supervisor/
sudo supervisord -c $(pwd)/supervisord.conf

# nginx
sudo nginx -c $(pwd)/nginx.conf
