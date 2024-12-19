class VolumeOscillator:
    def __init__(self, short_period=5, long_period=14):
        self.short_period = short_period
        self.long_period = long_period
        self.volumes = []

    def determine_next_trade(self, candles, short_period=5, long_period=14):
        volumes = [candle[5] for candle in candles]  # Extract volume field
        oscillator_value = self.calculate_volume_oscillator(volumes, short_period, long_period)
        trade_direction = self.analyze_trade_direction(oscillator_value)
        return trade_direction, oscillator_value
        
    def analyze_trade_direction(self, oscillator_value):
        if oscillator_value > 0:
            return "call"  # Buy signal
        elif oscillator_value < 0:
            return "put"  # Sell signal
        else:
            return "hold"  # Neutral
        
    def calculate_volume_oscillator(self, volumes, short_period, long_period):
        if len(volumes) < long_period:
            raise ValueError("Not enough data to calculate the long-period SMA.")

        short_sma = self.calculate_sma(volumes, short_period)
        long_sma = self.calculate_sma(volumes, long_period)

        if long_sma == 0:  # Prevent division by zero
            return 0

        oscillator = ((short_sma - long_sma) / long_sma) * 100
        return round(oscillator, 2)
    
    def calculate_sma(self, data, period):
        if len(data) < period:
            return None  # Not enough data for the period
        return sum(data[-period:]) / period