import sys
import os
import json
from unittest.mock import MagicMock, patch
import requests

# Add parent to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from trading_bot.bot.client import BinanceClient
from trading_bot.bot.orders import place_trade_order
from trading_bot.bot.logging_config import setup_logging

# Setup logging
setup_logging()

def test_place_order_with_logs():
    print("Setting up Real Client with Mocked Session...")
    client = BinanceClient("test_key", "test_secret")
    
    # Mock the session.request method
    mock_response = MagicMock()
    mock_response.json.return_value = {
        "orderId": 123456,
        "symbol": "BTCUSDT",
        "status": "NEW",
        "executedQty": "0.0",
        "avgPrice": "0.0"
    }
    mock_response.raise_for_status.return_value = None
    
    client.session.request = MagicMock(return_value=mock_response)

    print("Running Test: Place Valid Market Order (Logs Expected)")
    try:
        response = place_trade_order(client, "BTCUSDT", "BUY", "MARKET", 0.001)
        print("Success:", response)
    except Exception as e:
        print("Failed:", e)
        sys.exit(1)

    print("\nRunning Test: Place Valid Limit Order (Logs Expected)")
    try:
        response = place_trade_order(client, "BTCUSDT", "SELL", "LIMIT", 0.001, 50000.0)
        print("Success:", response)
    except Exception as e:
        print("Failed:", e)
        sys.exit(1)

if __name__ == "__main__":
    test_place_order_with_logs()
