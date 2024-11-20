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

# nginx設定 sites-available はデフォルト読み込みディレクトリ
sudo nano /etc/nginx/sites-available/stockkeeper
--------
server {
    listen 80;
    server_name your-ec2-public-ip your-domain.com;

    location = /favicon.ico { access_log off; log_not_found off; }
    location /static/ {
        root /home/ubuntu/your_project_name;
    }

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
--------
# ln: シンベリックリンク -> /etc/nginx/sites-enabled sites-enabled が設定で反映される
sudo ln -s /etc/nginx/sites-available/my_django_app /etc/nginx/sites-enabled
sudo nginx -t  # 設定テスト
sudo systemctl restart nginx


sudo systemctl status stockkeeper.service

