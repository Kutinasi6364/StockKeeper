aws ec2 describe-instances --filters "Name=instance-state-name,Values=running" --query "Reservations[*].Instances[*].[InstanceId,PublicIpAddress]" --output table

# SSH で接続
ssh -i "C:\Users\kutin\Desktop\AWS\Security\UniversalSecurityKey.pem" ec2-user@$PUBLIC_IP