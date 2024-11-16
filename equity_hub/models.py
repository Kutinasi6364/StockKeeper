from django.db import models

class EquityHub(models.Model):
    stock_No = models.AutoField(primary_key=True) # 自動付与
    symbol = models.CharField(max_length=10, unique=True) # 銘柄コード
    name = models.CharField(max_length=100) # 銘柄名
    dividend_yield = models.FloatField() # 約定利回り
    price = models.FloatField() # 現在値
    shares_owned = models.IntegerField() # 所持個数
    industry = models.CharField(max_length=100, null=True, blank=True) # 銘柄分類
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)

    def __str__(self):
        return self.name