import pandas as pd
import numpy as np
from qlib.backtest import base

class Strategy:
    """
    Strategy class
    """

    def generate_signals(self, data):
        """
        Generate trading signals based on the provided data.
        Implemented by subclasses to define specific strategies.
        """
        raise NotImplementedError

class DoubleMAStrategy(Strategy): 
    """
    Example strategy: Double Moving Average Strategy
    """

    def __init__(self, short_window=5, long_window=20):
        self.short_window = short_window
        self.long_window = long_window
    
    def generate_signals(self, data):
        """
        Generate trading signals based on the Double Moving Average Strategy.
        """
        signals = pd.DataFrame(index=data.index)
        signals["signal"] = 0.0

        #Calculate MA
        signals["short_ma"] = data["$clise"].rolling(window=self.short_window, min_periods=1).mean()
        signals["long_ma"] = data["$close"].rolling(window=self.long_window, min_periods=1).mean()

        # Create signals
        signals["signal"][self.short_window:] = np.where(
            signals["short_ma"][self.short_window:] > signals["long_ma"][self.short_window:], 1.0, -1.0
        )

        #
        signals["position"] = signals["signal"].diff()
        return signals