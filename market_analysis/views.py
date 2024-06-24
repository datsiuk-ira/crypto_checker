# views.py
import json

import requests
from django.shortcuts import render

from market_analysis.arima_model import ArimaForecastGenerator


def get_historical_data(symbol, interval, limit):
    binance_url = f'https://api.binance.com/api/v3/klines?symbol={symbol}&interval={interval}&startTime=1719232200000&endTime=1719238200000'
    response = requests.get(binance_url)

    if response.status_code == 200:
        return response.json()
    else:
        raise Exception('Виникла помилка при отриманні даних про криптопару. Перевірте назву криптопари!')


def crypto_price_checker(request):
    arima_forecast_generator = ArimaForecastGenerator()
    symbol = request.GET.get('symbol', 'BTCUSDT')
    interval = request.GET.get('interval', '1m')
    limit = int(request.GET.get('limit', 100))

    try:
        historical_data = get_historical_data(symbol, interval, limit)
        arima_data = arima_forecast_generator.generate(historical_data, interval, steps=int(limit / 10))
        context = {
            'historical_data': json.dumps(historical_data),
            'arima_data': arima_data.to_json(orient='records', date_format='iso'),
            'timestamps': json.dumps([entry[0] for entry in historical_data]),
        }
    except Exception as e:
        context = {'error': f"Error: {e}"}

    return render(request, 'market_analysis/crypto_chart.html', context)
