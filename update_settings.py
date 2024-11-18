import requests
import os

# EC2インスタンスメタデータURL
metadata_url = "http://169.254.169.254/latest/meta-data/public-ipv4"

# トークンを取得するURL (IMDSv2用)
token_url = "http://169.254.169.254/latest/api/token"
headers = {'X-aws-ec2-metadata-token-ttl-seconds': '21600'}  # TTL: 6時間

# トークンを取得
response = requests.put(token_url, headers=headers)

if response.status_code == 200:
    # トークンを取得
    token = response.text
    headers = {'X-aws-ec2-metadata-token': token}
    
    # パブリックIPを取得
    ip_response = requests.get(metadata_url, headers=headers)
    
    if ip_response.status_code == 200:
        public_ip = ip_response.text
        print(f"Public IP: {public_ip}")

        # settings.py のパス (Django プロジェクトのパスを指定)
        settings_path = '/home/ec2-user/StockKeeper/config/settings.py'

        # settings.py の読み込み
        with open(settings_path, 'r') as file:
            settings_content = file.read()

        # ALLOWED_HOSTS にパブリックIPを追加
        if "ALLOWED_HOSTS" in settings_content:
            # ALLOWED_HOSTSがすでに存在する場合、パブリックIPを追加
            if f"'{public_ip}'" not in settings_content:
                settings_content = settings_content.replace(
                    'ALLOWED_HOSTS = [',
                    f'ALLOWED_HOSTS = [\'{public_ip}\', '
                )
        else:
            # ALLOWED_HOSTSが存在しない場合、新たに追加
            settings_content += f"\nALLOWED_HOSTS = ['{public_ip}', '127.0.0.1', 'localhost']\n"

        # settings.py の上書き
        with open(settings_path, 'w') as file:
            file.write(settings_content)
        print("ALLOWED_HOSTS updated successfully.")
    else:
        print(f"Failed to retrieve public IP: {ip_response.status_code}")
else:
    print(f"Failed to get token: {response.status_code}")
