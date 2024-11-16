from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from rest_framework.views import APIView
from .models import EquityHub
from .serializers import EquityHubSerializer
from rest_framework.response import Response

from bs4 import BeautifulSoup
import requests
import urllib.robotparser
import time

@login_required(login_url='login')
def react_view(request):
    return render(request, 'react-base.html')


@method_decorator(login_required, name='dispatch')
class EquityHubHomeViewAPI(APIView):
    def get(self, request, *args, **kwargs):
        serializer = EquityHubSerializer(EquityHub.objects.filter(user=self.request.user), many=True)
        return Response(serializer.data)
    
    def put(self, request):
        data  = request.data
        for item in data:
            equity_hub = EquityHub.objects.get(stock_No=item['stock_No'])
            equity_hub.shares_owned += item['quantity']
            equity_hub.save()
        return Response(status=204)


@method_decorator(login_required, name='dispatch')
class EquityHubUpdateViewAPI(APIView):
    def put(self, request):
        get_equity_hub = GetEquityHubView()
        try:
            equity_hub = EquityHub.objects.filter(user=self.request.user)
            for item in equity_hub:
                stock_name, dividend_yield, current_price, industry = get_equity_hub.search_stock(item.symbol)
                if stock_name is not None:
                    item.dividend_yield = dividend_yield
                    item.price = current_price
                    item.industry = industry
                    item.save()
                    time.sleep(1)
            return Response(status=204)
        except Exception as e:
            return Response(status=400)


@method_decorator(login_required, name='dispatch')
class EquityHubDeleteViewAPI(APIView):
    def delete(self, request, *args, **kwargs):
        try:
            EquityHub.objects.filter(stock_No=kwargs['pk'], user=self.request.user).delete()
            return Response(status=204)
        except Exception as e:
            return Response(status=400)
    

@method_decorator(login_required, name='dispatch')
class EquityHubRegisterViewAPI(APIView):
    def post(self, request):
        get_equity_hub = GetEquityHubView()
        try:
            stock_name, dividend_yield, current_price, industry = get_equity_hub.search_stock(request.data.get('ticker_symbol'))
            
            if stock_name is not None:
                equity = EquityHub(
                    symbol = request.data.get('ticker_symbol'),
                    name = stock_name,
                    dividend_yield = dividend_yield,
                    price = current_price,
                    shares_owned = 0, # 初期は0固定
                    industry = industry,
                    user = request.user,
                )
                equity.save()
                return Response(status=200)
        except Exception as e:
            return Response(status=400)
        

class GetEquityHubView():
    def __init__(self):
        # 各URLの設定
        self.robot_url = "https://minkabu.jp/robots.txt"
        self.basic_url = "https://minkabu.jp/stock/"
    
    # 全ての証券番号の情報を抜き出す
    def search_stock(self, ticker_symbol):
        # 指定した証券番号のURLを作成
        url = self.basic_url + ticker_symbol
        if self.check_crawling(url):
            # 株価、配当金を返す
            return self.scraping(url) # stock_name, dividend_yield, current_price, industry_a


    # クローリング可能かチェック
    def check_crawling(self, url):
        ur = urllib.robotparser.RobotFileParser()
        ur.set_url(self.robot_url)
        ur.read()
        result = ur.can_fetch("*", url)
        return result

    # スクレイピングの実行
    def scraping(self, url):
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")

        stock_name = soup.find('span', class_='md_stockBoard_stockName').text # 証券名

        # 配当金抽出
        dividend_yield = soup.find_all(
            "td", attrs={"class": "ly_vamd_inner ly_colsize_9_fix fwb tar wsnw"}
        )
        # 株価抽出
        current_price = soup.find("div", attrs={"class": "stock_price"}).text

        # 抽出した文字の整形
        current_price = current_price.replace(",", "")
        current_price = current_price.replace("\n", "")
        current_price = current_price.replace(" ", "")
        current_price = current_price.replace("円", "")

        # 株価と配当金をリストに追加
        if current_price == "---":
            current_price = 0
        else:
            current_price = float(current_price)
        
        if dividend_yield[4].string == "---": # 沖縄セルラーの値が取れなかったため対応
            dividend_yield = 0.01
        else:
            dividend_yield = dividend_yield[4].string.replace("%", "")

        # 業種を取得
        industry = soup.find('div', class_='ly_content_wrapper size_ss')
        if industry:
            industry_a = industry.find('a').get_text()
            
        return stock_name, dividend_yield, current_price, industry_a

    