from typing import List, Tuple
import pandas as pd
from statsmodels.tsa.arima.model import ARIMA
import numpy as np

class DataPreprocessor:
    def preprocess_data(self, data: List[List]) -> pd.DataFrame:
        columns = ['timestamp', 'open', 'high', 'low', 'close', 'volume', 'close_time',
                   'quote_asset_volume', 'number_of_trades', 'taker_buy_base_asset_volume',
                   'taker_buy_quote_asset_volume', 'ignore']
        df = pd.DataFrame(data, columns=columns)
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms').dt.tz_localize('UTC')
        df.set_index('timestamp', inplace=True)
        return df


class ArimaModelFinder:
    def find_best_arima_order(self, series: pd.Series) -> Tuple[int, int, int]:
        best_aic = float("inf")
        best_order = None

        p = d = q = range(0, 3)
        pdq = [(p_, d_, q_) for p_ in p for d_ in d for q_ in q]

        for order in pdq:
            try:
                model = ARIMA(series, order=order)
                model_fit = model.fit()
                if model_fit.aic < best_aic:
                    best_aic = model_fit.aic
                    best_order = order
            except:
                continue

        if best_order is None:
            raise ValueError("No suitable ARIMA model found.")
        return best_order

    def make_forecast(self, series: pd.Series, order: Tuple[int, int, int], start_point: int, end_point: int) -> pd.Series:
        model = ARIMA(series, order=order)
        model_fit = model.fit()
        forecast = model_fit.predict(start=start_point, end=end_point)
        return forecast


class FutureTimeStampsGenerator:
    __interval_map = {
        '1m': ('minutes', 1),
        '5m': ('minutes', 5),
        '15m': ('minutes', 15),
        '1h': ('hours', 1),
        '1d': ('days', 1),
    }

    def generate(self, start_timestamp: pd.Timestamp, interval: str, num_points: int) -> List[pd.Timestamp]:
        interval_pair = FutureTimeStampsGenerator.__interval_map[interval]
        timestamp_name = interval_pair[0]
        timestamp_value = interval_pair[1]
        future_timestamps = [start_timestamp + pd.Timedelta(**{timestamp_name: i * timestamp_value}) for i in
                             range(num_points)]
        return future_timestamps


class ArimaForecastGenerator:
    def __init__(self):
        self.preprocessor = DataPreprocessor()
        self.arima_model = ArimaModelFinder()
        self.forecast_generator = FutureTimeStampsGenerator()

    def generate(self, data: List[List], interval: str, steps: int = 10) -> pd.DataFrame:
        df = self.preprocessor.preprocess_data(data)
        close_prices = df['close'].astype(float)

        best_order = self.arima_model.find_best_arima_order(close_prices)

        start_point = int(len(close_prices) * 0.1)
        forecast_end = start_point + len(close_prices) - 1

        forecast_close = self.arima_model.make_forecast(close_prices, best_order, start_point, forecast_end)
        forecast_open = self.arima_model.make_forecast(df['open'].astype(float), best_order, start_point, forecast_end)

        final_forecast = np.median([forecast_close.values, forecast_open.values], axis=0)

        start_timestamp = df.index[start_point]
        future_timestamps = self.forecast_generator.generate(start_timestamp, interval, len(close_prices))

        forecast_df = pd.DataFrame({'timestamp': future_timestamps, 'forecast': final_forecast})

        return forecast_df[['timestamp', 'forecast']]
