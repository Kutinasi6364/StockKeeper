from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.contrib.auth import get_user_model
from equity_hub.models import EquityHub
from unittest.mock import patch

User = get_user_model()

class EquityHubDeleteViewAPITest(APITestCase):
    def setUp(self):
        # テスト用ユーザーを作成
        self.user = User.objects.create_user(username='testuser', password='password')
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.equity_hub_entry = EquityHub.objects.create(
            user=self.user,
            stock_No=1, # 適当なNo.
            symbol="9999",  # 適当な証券コード
            dividend_yield=9999,
            price=9999,
            industry="****",
            shares_owned=0
        )

    def test_delete_equity_hub_success(self):
        # ログイン状態をシミュレート
        self.client.login(username='testuser', password='password')
        url = reverse('delete', kwargs={'pk': self.equity_hub_entry.pk})
        response = self.client.delete(url)

        # ステータスコードが204 (No Content) であることを確認
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # データベースにエントリが削除されていることを確認
        self.assertEqual(EquityHub.objects.count(), 0)

    def test_delete_equity_hub_unauthorized(self):
        # 認証無しでdeleteリクエスト
        url = reverse('delete', kwargs={'pk': self.equity_hub_entry.pk})  # 存在しないIDを指定
        response = self.client.delete(url)

        # ステータスコードが400 (Bad Request) であることを確認
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)

        # データベースにエントリが削除されていないことを確認
        self.assertEqual(EquityHub.objects.count(), 1)


class EquityHubUpdateViewAPITest(APITestCase):
    def setUp(self):
        # テスト用ユーザーを作成
        self.user = User.objects.create_user(username='testuser', password='password')
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.url = reverse('update')  # URLの名前を逆引きで取得
        self.equity_hub_entry = EquityHub.objects.create(
            user=self.user,
            symbol="****",  # 適当な証券コード
            dividend_yield=9999,
            price=9999,
            industry="Technology",
            shares_owned=0
        )

    def test_update_equity_hub_success(self):
        with patch('equity_hub.views.GetEquityHubView.search_stock') as mock_search_stock:
            # ログイン状態をシミュレート
            self.client.login(username='testuser', password='password')
            
            mock_search_stock.return_value = ("****", 1000, 1000, "Technology")

            # PUTリクエストを送信
            response = self.client.put(self.url)

            # ステータスコード204を確認
            self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

            # EquityHubエントリが正しく更新されたか確認
            self.equity_hub_entry.refresh_from_db()
            self.assertEqual(self.equity_hub_entry.dividend_yield, 1000)
            self.assertEqual(self.equity_hub_entry.price, 1000)
            self.assertEqual(self.equity_hub_entry.industry, "Technology")

    def test_update_equity_hub_unauthorized(self):
        # 認証せずにPUTリクエストを送信
        self.client.logout()
        response = self.client.put(self.url)

        # ステータスコード302を確認（認証が必要なため）
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)

# class EquityHubRegisterViewAPITest(APITestCase):
#     # テスト用ユーザーを作成
#     def setUp(self):
#         self.user = User.objects.create_user(username='testuser', password='password')
#         self.client = APIClient()
#         self.client.force_authenticate(user=self.user)
#         self.url = reverse('register')  # URLの名前を逆引きで取得

#     def test_register_equity_hub_success(self):
#         # ログイン状態をシミュレート
#         self.client.login(username='testuser', password='password')

#         # テスト用データを設定
#         data = {
#             'ticker_symbol': '8424'  # 存在するティッカーシンボルを指定
#         }
        
#         # 正常なPOSTリクエストの送信
#         response = self.client.post(self.url, data, format='json')
        
#         # レスポンスの内容を検証
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
        
#         # データベースに登録されているか検証
#         self.assertTrue(EquityHub.objects.filter(symbol='8424', user=self.user).exists())
    
#     def test_register_equity_hub_exception_handling(self):
#         # ログイン状態をシミュレート
#         self.client.login(username='testuser', password='password')
        
#         # データが空の場合や検索結果がない場合をシミュレート
#         response = self.client.post(self.url, {}, format='json')
        
#         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

