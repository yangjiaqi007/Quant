from qlib.data import D
from qlib.utils import init_instance_by_config

class DataFeed:
    """
    A class to handle data loading for financial markets.
    """
    def __init__(self, market="csi300", start_time="2020-01-01", end_time="2024-12--31"):
        self.market = market
        self.start_time = start_time
        self.end_time = end_time
    
    def load_data(self):
        """
        Load data for the specified market and time range.

        """
        instruments = D.instruments(self.market)
        df_data = D.features(
            instruments,
            features=[
                "$open", "$high", "$low", "$close", "$volume",
                "Ref($close, -1)/$close-1",
                "Mean($close,5)/$close",
                "Mean($close, 20)/$close",
            ],
            start_time=self.start_time,
            end_time=self.end_time,
        )
        return df_data

#Example:
# data_feed = DataFeed(market="csi300", start_time="2020-01-01", end_time="2024-12-31")
# data = data_feed.load_data()