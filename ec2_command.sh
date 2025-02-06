sudo yum update -y
sudo yum install python3 -y
sudo yum install python3-pip -y
sudo yum install git -y
sudo yum install nginx

git checkout -- config/settings.py

sudo systemctl daemon-reload
sudo systemctl start stockkeeper.service
sudo systemctl status stockkeeper.service

pip install gunicorn
pip install whitenoise

gunicorn StockKeeper.config.wsgi:application --bind 0.0.0.0:8000

# ln: シンボリックリンク -> /etc/nginx/sites-enabled sites-enabled が設定で反映される
sudo ln -s /etc/nginx/sites-available/stockkeeper /etc/nginx/sites-enabled
sudo nginx -t  # 設定テスト
sudo systemctl restart nginx


sudo systemctl status stockkeeper.service

