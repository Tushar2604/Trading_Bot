import argparse
import os
import sys
from rich.console import Console
from rich.table import Table
from dotenv import load_dotenv

# Add parent directory to path so we can import from bot package
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from bot.client import BinanceClient, MockBinanceClient
from bot.orders import place_trade_order
from bot.logging_config import setup_logging

# Load environment variables
load_dotenv()

console = Console()
logger = setup_logging()

def main():
    parser = argparse.ArgumentParser(description="Binance Futures Testnet Trading Bot")
    
    parser.add_argument("--symbol", type=str, required=True, help="Trading symbol (e.g., BTCUSDT)")
    parser.add_argument("--side", type=str, required=True, choices=["BUY", "SELL"], help="Order side")
    parser.add_argument("--type", type=str, required=True, choices=["LIMIT", "MARKET"], help="Order type")
    parser.add_argument("--quantity", type=float, required=True, help="Order quantity")
    parser.add_argument("--price", type=float, help="Order price (required for LIMIT orders)")
    parser.add_argument("--api-key", type=str, help="Binance API Key (optional if set in env)")
    parser.add_argument("--api-secret", type=str, help="Binance API Secret (optional if set in env)")
    parser.add_argument("--mock", action="store_true", help="Run in mock mode (no API keys required)")

    args = parser.parse_args()

    # Determine Client Type and Keys
    if args.mock:
        console.print("[bold yellow]Running in MOCK mode. No real orders will be placed.[/bold yellow]")
        client = MockBinanceClient()
    else:
        api_key = args.api_key or os.getenv("BINANCE_API_KEY")
        api_secret = args.api_secret or os.getenv("BINANCE_API_SECRET")

        if not api_key or not api_secret:
            console.print("[bold red]Error:[/bold red] API Key and Secret are required. Provide them via arguments, environment variables, or use --mock.")
            sys.exit(1)
        
        client = BinanceClient(api_key, api_secret)

    try:        
        console.print(f"[bold blue]Placing Order:[/bold blue] {args.side} {args.symbol} {args.type} Qty={args.quantity} Price={args.price}")
        
        response = place_trade_order(client, args.symbol, args.side, args.type, args.quantity, args.price)
        
        console.print("[bold green]Order Placed Successfully![/bold green]")
        
        table = Table(title="Order Details")
        table.add_column("Field", style="cyan")
        table.add_column("Value", style="magenta")
        
        table.add_row("Order ID", str(response.get("orderId")))
        table.add_row("Symbol", response.get("symbol"))
        table.add_row("Status", response.get("status"))
        table.add_row("Executed Qty", response.get("executedQty"))
        table.add_row("Avg Price", response.get("avgPrice"))
        
        console.print(table)

    except Exception as e:
        console.print(f"[bold red]Order Failed:[/bold red] {e}")
        logger.error(f"Order failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
