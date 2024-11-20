sudo yum update -y
sudo yum install python3 -y
sudo yum install python3-pip -y
sudo yum install git -y

git checkout -- config/settings.py

sudo systemctl daemon-reload
sudo systemctl start stockkeeper.service
sudo systemctl status stockkeeper.service

pip install gunicorn
pip install whitenoise

gunicorn StockKeeper.config.wsgi:application --bind 0.0.0.0:8000