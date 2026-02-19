import re

def validate_symbol(symbol: str) -> str:
    """Validates the trading symbol format (e.g., BTCUSDT)."""
    if not symbol:
        raise ValueError("Symbol cannot be empty.")
    # Basic check: usually uppercase alphanumeric
    if not re.match(r'^[A-Z0-9]+$', symbol.upper()):
        raise ValueError(f"Invalid symbol format: {symbol}")
    return symbol.upper()

def validate_side(side: str) -> str:
    """Validates order side (BUY or SELL)."""
    normalized_side = side.upper()
    if normalized_side not in ["BUY", "SELL"]:
        raise ValueError(f"Invalid side: {side}. Must be 'BUY' or 'SELL'.")
    return normalized_side

def validate_positive_float(value: float, name: str) -> float:
    """Validates that a numerical value is positive."""
    try:
        val = float(value)
    except ValueError:
        raise ValueError(f"{name} must be a number.")
    
    if val <= 0:
        raise ValueError(f"{name} must be greater than 0.")
    return val

def validate_order_type(order_type: str) -> str:
    """Validates order type (LIMIT or MARKET)."""
    normalized_type = order_type.upper()
    if normalized_type not in ["LIMIT", "MARKET"]:
        raise ValueError(f"Invalid order type: {order_type}. Must be 'LIMIT' or 'MARKET'.")
    return normalized_type
