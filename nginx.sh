# nginx設定 sites-available はデフォルト読み込みディレクトリ
sudo nano /etc/nginx/sites-available/stockkeeper

server {
    listen 80;
    server_name 35.78.74.37;
    return 301 https://$host$request_uri;  # HTTPからHTTPSにリダイレクト

    location = /favicon.ico { access_log off; log_not_found off; }
    location /static/ {
        alias /home/ec2-user/StockKeeper/staticfiles/;
    }
}

server {
    listen 443 ssl;  # HTTPSのポート443をリッスン
    server_name 35.78.74.37;

    ssl_certificate /etc/ssl/certs/nginx-selfsigned.crt;
    ssl_certificate_key /etc/ssl/private/nginx-selfsigned.key;

    location /static/ {
        alias /home/ec2-user/StockKeeper/staticfiles/;
        try_files $uri $uri/ =404;  # ファイルが見つからない場合に404を返す
    }

    location / {
        proxy_pass http://127.0.0.1:8000/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        add_header 'Access-Control-Allow-Origin' '*';
        add_header 'Access-Control-Allow-Methods' 'GET, POST, OPTIONS';
        add_header 'Access-Control-Allow-Headers' 'Authorization, Content-Type';

        if ($request_method = 'OPTIONS') {
            add_header 'Access-Control-Allow-Origin' '*';
            add_header 'Access-Control-Allow-Methods' 'GET, POST, OPTIONS';
            add_header 'Access-Control-Allow-Headers' 'Authorization, Content-Type';
            add_header 'Access-Control-Max-Age' 3600;
            return 204;
        }
    }
}
