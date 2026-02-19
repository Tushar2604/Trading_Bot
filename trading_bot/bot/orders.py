from typing import Optional, Dict, Any
from .client import BinanceClient
from .validators import validate_symbol, validate_side, validate_order_type, validate_positive_float

def place_trade_order(client: BinanceClient, symbol: str, side: str, order_type: str, quantity: float, price: Optional[float] = None) -> Dict[str, Any]:
    """
    Validates inputs and places an order using the BinanceClient.
    """
    # Validation
    symbol = validate_symbol(symbol)
    side = validate_side(side)
    order_type = validate_order_type(order_type)
    quantity = validate_positive_float(quantity, "Quantity")
    
    if order_type == "LIMIT":
        price = validate_positive_float(price, "Price")

    # Place Order
    return client.place_order(symbol, side, order_type, quantity, price)
