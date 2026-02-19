# Simplified Trading Bot

A Python-based CLI application to place **MARKET** and **LIMIT** orders on the **Binance Futures Testnet (USDT-M)**.

## Features
- **Place Orders**: Supports MARKET and LIMIT orders for both BUY and SELL sides.
- **Validation**: Ensures valid symbols, positive quantities/prices, and correct order types.
- **Enhanced CLI**: Uses `rich` for colorful and structured output.
- **Logging**: detailed logs are saved to `trading_bot.log`.
- **Modular Design**: Separated API client, order logic, and CLI interface.

## Prerequisites
- Python 3.x
- A [Binance Futures Testnet](https://testnet.binancefuture.com) account.
- API Key and Secret from the Testnet.

## Setup

1. **Clone/Download** the repository.
2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
3. **Environment Variables** (Optional but recommended):
   Create a `.env` file or set them in your shell:
   ```bash
   export BINANCE_API_KEY="your_api_key"
   export BINANCE_API_SECRET="your_api_secret"
   ```

## Usage

Run the bot from the command line using `python trading_bot/cli.py`.

### Arguments

| Argument | Type | Description | Required | Options |
| :--- | :--- | :--- | :--- | :--- |
| `--symbol` | str | Trading Pair | Yes | e.g. `BTCUSDT` |
| `--side` | str | Order Side | Yes | `BUY`, `SELL` |
| `--type` | str | Order Type | Yes | `MARKET`, `LIMIT` |
| `--quantity` | float | Amount to trade | Yes | > 0 |
| `--price` | float | Limit Price | No* | > 0 (*Req for LIMIT) |
| `--api-key` | str | API Key | No* | (*If not in env) |
| `--api-secret`| str | API Secret | No* | (*If not in env) |

### Examples

**1. Place a MARKET BUY Order:**
```bash
python trading_bot/cli.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.001
```

**2. Place a LIMIT SELL Order:**
```bash
python trading_bot/cli.py --symbol BTCUSDT --side SELL --type LIMIT --quantity 0.001 --price 50000
```

**3. Providing Keys Inline:**
```bash
python trading_bot/cli.py --symbol ETHUSDT --side BUY --type MARKET --quantity 0.01 --api-key "YOUR_KEY" --api-secret "YOUR_SECRET"
```

### Mock Mode (No Keys Required)
You can run the bot in "Mock Mode" to test the CLI and logic without needing API keys or placing real orders.

```bash
python trading_bot/cli.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.001 --mock
```

## Project Structure
```
trading_bot/
  bot/
    __init__.py
    client.py        # Binance Client Wrapper
    orders.py        # Order Logic & Validation
    validators.py    # Input Validators
    logging_config.py# Logging Setup
  cli.py             # CLI Entry Point
requirements.txt
README.md
```

## Logs
All activities are logged to `trading_bot.log` in the root directory.
