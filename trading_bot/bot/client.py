import hashlib
import hmac
import time
import requests
import logging
from typing import Dict, Any, Optional

logger = logging.getLogger("trading_bot")

class BinanceClient:
    BASE_URL = "https://testnet.binancefuture.com"

    def __init__(self, api_key: str, api_secret: str):
        self.api_key = api_key
        self.api_secret = api_secret
        self.session = requests.Session()
        self.session.headers.update({
            "X-MBX-APIKEY": self.api_key,
            "Content-Type": "application/json"
        })

    def _get_timestamp(self) -> int:
        return int(time.time() * 1000)

    def _sign_request(self, params: Dict[str, Any]) -> Dict[str, Any]:
        query_string = '&'.join([f"{k}={v}" for k, v in params.items()])
        signature = hmac.new(
            self.api_secret.encode('utf-8'),
            query_string.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()
        params["signature"] = signature
        return params

    def _send_request(self, method: str, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        url = f"{self.BASE_URL}{endpoint}"
        params = params or {}
        
        # Add timestamp and signature
        params["timestamp"] = self._get_timestamp()
        
        # Only sign if we have credentials
        if self.api_key and self.api_secret:
             params = self._sign_request(params)
        
        logger.info(f"Sending {method} request to {url} with params: {params}")

        try:
            response = self.session.request(method, url, params=params)
            response.raise_for_status()
            logger.info(f"Response: {response.json()}")
            return response.json()
        except requests.exceptions.HTTPError as e:
            logger.error(f"HTTP Error: {e.response.text}")
            raise
        except Exception as e:
            logger.error(f"Request failed: {e}")
            raise

    def place_order(self, symbol: str, side: str, order_type: str, quantity: float, price: Optional[float] = None, 
                   time_in_force: str = "GTC") -> Dict[str, Any]:
        """
        Places an order on Binance Futures Testnet.
        """
        params = {
            "symbol": symbol,
            "side": side,
            "type": order_type,
            "quantity": quantity,
        }

        if order_type == "LIMIT":
            if price is None:
                raise ValueError("Price is required for LIMIT orders")
            params["price"] = price
            params["timeInForce"] = time_in_force
        
        return self._send_request("POST", "/fapi/v1/order", params)

    def get_account_info(self) -> Dict[str, Any]:
        """Fetch account information (balances, etc.)"""
        return self._send_request("GET", "/fapi/v2/account")

class MockBinanceClient(BinanceClient):
    """
    Mock Client for testing without API keys.
    """
    def __init__(self, api_key: str = "mock_key", api_secret: str = "mock_secret"):
        super().__init__(api_key, api_secret)
        logger.info("Initialized MockBinanceClient")

    def _send_request(self, method: str, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        logger.info(f"[MOCK] Sending {method} request to {endpoint} with params: {params}")
        
        # Simulate successful order response
        if "order" in endpoint:
            return {
                "orderId": 123456789,
                "symbol": params.get("symbol", "UNKNOWN"),
                "status": "NEW",
                "clientOrderId": "mock_order_id",
                "price": params.get("price", "0"),
                "avgPrice": "0.00000",
                "origQty": params.get("quantity", "0"),
                "executedQty": "0",
                "cumQty": "0",
                "cumQuote": "0",
                "timeInForce": "GTC",
                "type": params.get("type", "MARKET"),
                "reduceOnly": False,
                "closePosition": False,
                "side": params.get("side", "BUY"),
                "positionSide": "BOTH",
                "stopPrice": "0",
                "workingType": "CONTRACT_PRICE",
                "priceProtect": False,
                "origType": params.get("type", "MARKET"),
                "updateTime": int(time.time() * 1000)
            }
        return {"msg": "Mock response"}
