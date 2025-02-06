sudo yum update -y
sudo yum install python3 -y
sudo yum install python3-pip -y
sudo yum install git -y
sudo yum install nginx -y

pip install gunicorn

git clone https://github.com/Kutinasi6364/StockKeeper.git

pip install -r requirements.txt

# settings.py ALLOWED_HOSTS = []

gunicorn StockKeeper.config.wsgi:application --bind 0.0.0.0:8000

sudo nano /etc/nginx/nginx.conf

-- nginx.config --
include /etc/nginx/sites-available/stockkeeper

sudo nano /etc/nginx/sites-available/stockkeeper

sudo mkdir /etc/ssl/private

sudo openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
    -keyout /etc/ssl/private/nginx-selfsigned.key \
    -out /etc/ssl/certs/nginx-selfsigned.crt

sudo ln -s /etc/nginx/sites-available/stockkeeper /etc/nginx/sites-enabled
sudo nginx -t  # 設定テスト
sudo systemctl restart nginx


# ポート開放 8000, 443

sudo chmod -R 755 /home