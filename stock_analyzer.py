import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
import logging

logger = logging.getLogger("stock-analyzer")


class StockAnalyzer:
    """Analyzes stocks for technical patterns like MA crossovers."""

    def __init__(self):
        self.stocks_cache = {}

        # Taiwan stock tickers (台股代碼範例)
        self.tw_stocks = [
            "2330.TW",  # TSMC
            "2317.TW",  # Acer
            "2454.TW",  # MediaTek
            "3008.TW",  # Largan Precision
            "2412.TW",  # Mediatek
            "1303.TW",  # Nanya Technology
            "2882.TW",  # Cathay Pacific
            "1101.TW",  # Taiwan Cement
            "1102.TW",  # Asia Cement
            "1216.TW",  # Uni-President
            "2105.TW",  # Chailease
            "1907.TW",  # Taiwan Fertilizer
            "2887.TW",  # Taiwan Semiconductor
            "9910.TW",  # Honsen
            "5871.TW",  # Chinatrust
        ]

        # Top US stocks (美股代碼範例)
        self.us_stocks = [
            "AAPL",  # Apple
            "MSFT",  # Microsoft
            "GOOGL",  # Google
            "AMZN",  # Amazon
            "NVDA",  # NVIDIA
            "TSLA",  # Tesla
            "META",  # Meta
            "NFLX",  # Netflix
            "SPOT",  # Spotify
            "SQ",    # Block
            "PLTR",  # Palantir
            "CRM",   # Salesforce
            "ADBE",  # Adobe
            "INTC",  # Intel
            "AMD",   # AMD
        ]

    def get_ma_crossover_stocks(self, market: str = "tw", days: int = 5) -> dict:
        """Find stocks with MA pullback (moving average pullback).

        Args:
            market: "tw" for Taiwan stocks, "us" for US stocks
            days: Number of days for pullback detection (default: 5)

        Returns:
            Dictionary with list of stocks and analysis details
        """
        stocks = self.tw_stocks if market == "tw" else self.us_stocks
        market_name = "台股" if market == "tw" else "美股"

        results = {
            "market": market_name,
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "stocks": [],
            "total_analyzed": 0,
            "total_found": 0
        }

        logger.info(f"Scanning {market_name} for MA pullback opportunities...")

        for ticker in stocks:
            try:
                results["total_analyzed"] += 1

                # Download historical data (last 30 days)
                data = yf.download(ticker, period="30d", progress=False)

                if len(data) < 10:
                    continue

                # Calculate moving averages
                data['MA5'] = data['Close'].rolling(window=5).mean()
                data['MA10'] = data['Close'].rolling(window=10).mean()
                data['MA20'] = data['Close'].rolling(window=20).mean()

                # Get current and recent prices
                current_price = data['Close'].iloc[-1]
                ma5 = data['MA5'].iloc[-1]
                ma10 = data['MA10'].iloc[-1]
                ma20 = data['MA20'].iloc[-1]

                # Check for MA pullback (price below MA but recovering)
                recent_prices = data['Close'].iloc[-days:].values
                recent_ma = data['MA5'].iloc[-days:].values

                # Detect pullback: price dipped below MA but is recovering
                if self._is_ma_pullback(recent_prices, recent_ma, days):
                    # Calculate metrics
                    high_recent = data['Close'].iloc[-days:].max()
                    low_recent = data['Close'].iloc[-days:].min()
                    support = low_recent
                    resistance = high_recent

                    stock_info = {
                        "ticker": ticker,
                        "current_price": round(current_price, 2),
                        "ma5": round(ma5, 2),
                        "ma10": round(ma10, 2),
                        "ma20": round(ma20, 2),
                        "support": round(support, 2),
                        "resistance": round(resistance, 2),
                        "trend": "BULLISH" if current_price > ma20 else "BEARISH",
                    }

                    results["stocks"].append(stock_info)
                    results["total_found"] += 1

            except Exception as e:
                logger.error(f"Error analyzing {ticker}: {e}")
                continue

        return results

    @staticmethod
    def _is_ma_pullback(prices: list, ma_values: list, days: int) -> bool:
        """Check if there's a MA pullback pattern.

        Pullback = price dipped below MA then recovered
        """
        if len(prices) < days:
            return False

        # Check if lowest point was below MA
        min_price = min(prices)
        avg_ma = sum(ma_values) / len(ma_values)

        # Check if current price is above MA (recovery)
        current_above_ma = prices[-1] > ma_values[-1]

        # Check if there was a recent dip below MA
        recent_below = any(p < ma for p, ma in zip(prices[-days:], ma_values[-days:]))

        return current_above_ma and recent_below

    def format_results(self, results: dict) -> str:
        """Format results for Telegram display."""
        market = results["market"]
        total = results["total_analyzed"]
        found = results["total_found"]

        message = f"📊 {market} MA 回撤五日掃描結果\n"
        message += f"⏰ 時間：{results['date']}\n"
        message += f"━━━━━━━━━━━━━━━━━━━━━━\n"
        message += f"掃描股票數：{total} 只\n"
        message += f"符合條件：{found} 只 ✅\n\n"

        if found == 0:
            message += "暫無符合條件的股票"
            return message

        for stock in results["stocks"][:10]:  # Show top 10
            message += f"🔹 {stock['ticker']}\n"
            message += f"   現價：${stock['current_price']}\n"
            message += f"   MA5：${stock['ma5']} | MA10：${stock['ma10']}\n"
            message += f"   MA20：${stock['ma20']}\n"
            message += f"   支撐：${stock['support']} | 壓力：${stock['resistance']}\n"
            message += f"   趨勢：{stock['trend']}\n\n"

        if found > 10:
            message += f"📌 ...還有 {found - 10} 只股票\n"

        return message

    def get_weekly_ma_analysis(self, ticker: str) -> dict:
        """Get weekly MA analysis for a stock."""
        try:
            data = yf.download(ticker, period="60d", progress=False)

            if len(data) < 20:
                return {"error": f"Not enough data for {ticker}"}

            # Calculate weekly data
            weekly_data = data.resample("W").agg({
                "Open": "first",
                "High": "max",
                "Low": "min",
                "Close": "last",
                "Volume": "sum"
            })

            # Calculate MAs
            weekly_data["MA5W"] = weekly_data["Close"].rolling(window=5).mean()
            weekly_data["MA10W"] = weekly_data["Close"].rolling(window=10).mean()

            current_price = data["Close"].iloc[-1]
            weekly_close = weekly_data["Close"].iloc[-1]
            ma5w = weekly_data["MA5W"].iloc[-1]
            ma10w = weekly_data["MA10W"].iloc[-1]

            return {
                "ticker": ticker,
                "current_price": round(current_price, 2),
                "weekly_close": round(weekly_close, 2),
                "ma5w": round(ma5w, 2),
                "ma10w": round(ma10w, 2),
                "weeks_analyzed": len(weekly_data),
                "trend": "BULLISH" if current_price > ma10w else "BEARISH"
            }
        except Exception as e:
            logger.error(f"Error analyzing {ticker}: {e}")
            return {"error": str(e)}

    def get_historical_data(self, ticker: str, days: int = 7) -> dict:
        """Get historical daily data for a stock."""
        try:
            data = yf.download(ticker, period=f"{days}d", progress=False)

            if len(data) == 0:
                return {"error": f"No data for {ticker}"}

            prices = []
            for date, row in data.iterrows():
                prices.append({
                    "date": date.strftime("%Y-%m-%d"),
                    "open": round(row["Open"], 2),
                    "close": round(row["Close"], 2),
                    "high": round(row["High"], 2),
                    "low": round(row["Low"], 2),
                    "volume": int(row["Volume"])
                })

            return {
                "ticker": ticker,
                "days": len(prices),
                "prices": prices,
                "current_price": prices[-1]["close"] if prices else None
            }
        except Exception as e:
            logger.error(f"Error getting historical data for {ticker}: {e}")
            return {"error": str(e)}

    def format_weekly_analysis(self, result: dict) -> str:
        """Format weekly analysis for display."""
        if "error" in result:
            return f"❌ 錯誤：{result['error']}"

        msg = f"📊 週線分析 - {result['ticker']}\n"
        msg += f"━━━━━━━━━━━━━━━━━━\n"
        msg += f"📈 現價：${result['current_price']}\n"
        msg += f"📅 週收：${result['weekly_close']}\n"
        msg += f"📊 週MA5：${result['ma5w']}\n"
        msg += f"📊 週MA10：${result['ma10w']}\n"
        msg += f"💡 趨勢：{result['trend']}\n"
        msg += f"⏱️ 分析週數：{result['weeks_analyzed']}\n\n"

        return msg

    def format_historical_data(self, result: dict) -> str:
        """Format historical data for display."""
        if "error" in result:
            return f"❌ 錯誤：{result['error']}"

        msg = f"📋 {result['ticker']} 過去 {result['days']} 天股價記錄\n"
        msg += f"━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"

        for price in result["prices"][-7:]:  # Show last 7
            msg += f"📅 日期：{price['date']}\n"
            msg += f"   開盤：${price['open']} | 收盤：${price['close']}\n"
            msg += f"   最高：${price['high']} | 最低：${price['low']}\n"
            msg += f"   成交量：{price['volume']:,}\n\n"

        return msg


# Global instance
_analyzer = None


def get_stock_analyzer() -> StockAnalyzer:
    """Get or create the global stock analyzer instance."""
    global _analyzer
    if _analyzer is None:
        _analyzer = StockAnalyzer()
    return _analyzer
