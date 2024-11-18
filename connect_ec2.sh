aws ec2 describe-instances --filters "Name=instance-state-name,Values=running" --query "Reservations[*].Instances[*].[InstanceId,PublicIpAddress]" --output table

# SSH で接続
ssh -i "C:\Users\kutin\Desktop\AWS\Security\UniversalSecurityKey.pem" ec2-user@$PUBLIC_IP


# 自動起動させるためにsystemd を使う
sudo nano /etc/systemd/system/[Webアプリ名].service
[Unit]
Description=[Webアプリ名]
After=syslog.target

[Service]
User=ec2-user
ExecStart=/usr/bin/java -jar /home/ec2-user/app/[Webアプリ名]-0.0.1-SNAPSHOT.jar
SuccessExitStatus=143

[Install]
WantedBy=multi-user.target
