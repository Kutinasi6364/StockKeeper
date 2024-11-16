import axios from 'axios';
import { getCookie } from './home/fetchCookie';

// 初期データを取得する関数
export const fetchEquityHubs = async (setEquityHubs: React.Dispatch<React.SetStateAction<any[]>>) => {
  try {
      const response = await axios.get('/home/api/'); // APIエンドポイントを指定
      setEquityHubs(response.data);
  } catch (error) {
      console.error('Error fetching data:', error);
  }
};

// 株式情報更新
export const updateStockData = async (fetchEquityHubs: () => void) => {
  try{
    await axios.put('/home/api/update/', {}, {
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': getCookie('csrftoken') ?? '', // CSRFトークンを取得
      },
    }); // APIエンドポイントを指定
    fetchEquityHubs(); // 再取得してリストを更新
    alert('最新株価情報を更新しました。');
  } catch (error: any) {
    alert(`Error updating data: ${error.response.data.error}`);
  }
};

// 株式購入数登録
export const handleBuy = async (shares: { [key: number]: number }, setShares: React.Dispatch<React.SetStateAction<any>>, fetchEquityHubs: () => void) => {
  try {
    const payload = Object.entries(shares).map(([stock_No, quantity]) => ({
    stock_No: stock_No,
    quantity: quantity,
    }))
    await axios.put(`/home/api/`, payload, {
      headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': getCookie('csrftoken') ?? '', // CSRFトークンを取得
      },
    });
    fetchEquityHubs(); // 再取得してリストを更新
    setShares({}); // 購入数をリセット
    alert('株式購入数を更新しました。');
  } catch (error: any) {
    alert(`Error updating data: ${error.response.data.error}`);
  }
};

// 株式登録
export const registerEquity = async (tickerSymbol: string, fetchEquityHubs: () => void) => {
  try {
    await axios.post('/home/api/register/', {
      ticker_symbol: tickerSymbol,
    }, {
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': getCookie('csrftoken') ?? '', // CSRFトークンを取得
      },
    });
    alert('株式を登録しました。');
  } catch (error: any) {
    alert(`Error registering data: ${error.response.data.error}`);
  }
  fetchEquityHubs(); // 再取得してリストを更新
};

// 株式登録削除
export const handleDelete = async (stock_No: number, fetchEquityHubs: () => void) => {
  try {
    await axios.delete(`/home/api/delete/${stock_No}/`, {
        headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': getCookie('csrftoken') ?? '', // CSRFトークンを取得
        },
    });
    alert('株式を削除しました。');
  } catch (error: any) {
    alert(`Error deleting data: ${error.response.data.error}`);
  }
  fetchEquityHubs(); // 再取得してリストを更新
};