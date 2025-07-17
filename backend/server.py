from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel
import httpx
import asyncio
import os
from typing import List, Dict, Optional
from datetime import datetime
import json
from emergentintegrations.llm.chat import LlmChat, UserMessage
import uuid

app = FastAPI(title="AI Binance Signals Bot")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# MongoDB connection
MONGO_URL = os.environ.get('MONGO_URL', 'mongodb://localhost:27017/')
client = AsyncIOMotorClient(MONGO_URL)
db = client.mexc_trading_signals

# API keys from environment
GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')
TELEGRAM_BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')

# MEXC API base URL
MEXC_BASE_URL = "https://api.mexc.com/api/v3"

# Pydantic models
class SignalRequest(BaseModel):
    symbol: str
    interval: str = "1h"

class TradingSignal(BaseModel):
    id: str
    symbol: str
    signal_type: str  # "LONG", "SHORT", "NO_SIGNAL"
    confidence: float
    price: float
    reason: str
    technical_analysis: str
    timestamp: datetime

class MarketData(BaseModel):
    symbol: str
    price: float
    change_24h: float
    volume: float
    timestamp: datetime

# MEXC API functions
async def fetch_mexc_data(endpoint: str, params: dict = None):
    """Fetch data from MEXC public API"""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{MEXC_BASE_URL}/{endpoint}", params=params)
            response.raise_for_status()
            return response.json()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching MEXC data: {str(e)}")

async def get_klines(symbol: str, interval: str = "1h", limit: int = 100):
    """Get candlestick data from MEXC"""
    # Convert standard intervals to MEXC format
    interval_mapping = {
        "1m": "1m",
        "5m": "5m", 
        "15m": "15m",
        "30m": "30m",
        "1h": "60m",  # MEXC uses 60m for 1 hour
        "4h": "4h",
        "1d": "1d"
    }
    
    mexc_interval = interval_mapping.get(interval, interval)
    
    params = {
        "symbol": symbol,
        "interval": mexc_interval,
        "limit": limit
    }
    return await fetch_mexc_data("klines", params)

async def get_ticker_24h(symbol: str):
    """Get 24h ticker data"""
    params = {"symbol": symbol}
    return await fetch_mexc_data("ticker/24hr", params)

async def get_all_tickers():
    """Get all tickers data"""
    return await fetch_mexc_data("ticker/24hr")

async def get_exchange_info():
    """Get trading pairs info"""
    return await fetch_mexc_data("exchangeInfo")

# AI Analysis functions
async def analyze_market_data(symbol: str, klines_data: List, ticker_data: Dict):
    """Analyze market data using Gemini AI"""
    try:
        # Prepare market data for AI analysis
        klines_formatted = []
        for kline in klines_data[-20:]:  # Last 20 candles
            klines_formatted.append({
                "open_time": kline[0],
                "open": float(kline[1]),
                "high": float(kline[2]),
                "low": float(kline[3]),
                "close": float(kline[4]),
                "volume": float(kline[5])
            })
        
        # Calculate technical indicators
        prices = [float(k[4]) for k in klines_data[-20:]]
        
        # Simple moving averages
        sma_5 = sum(prices[-5:]) / 5
        sma_10 = sum(prices[-10:]) / 10
        sma_20 = sum(prices[-20:]) / 20
        
        # RSI calculation (simplified)
        gains = []
        losses = []
        for i in range(1, len(prices)):
            change = prices[i] - prices[i-1]
            if change > 0:
                gains.append(change)
                losses.append(0)
            else:
                gains.append(0)
                losses.append(abs(change))
        
        avg_gain = sum(gains[-14:]) / 14 if len(gains) >= 14 else sum(gains) / len(gains)
        avg_loss = sum(losses[-14:]) / 14 if len(losses) >= 14 else sum(losses) / len(losses)
        
        rsi = 100 - (100 / (1 + (avg_gain / avg_loss if avg_loss != 0 else 1)))
        
        # Prepare AI prompt
        current_price = float(ticker_data["lastPrice"])
        price_change = float(ticker_data["priceChangePercent"])
        volume = float(ticker_data["volume"])
        
        ai_prompt = f"""
        Проанализируй торговые данные для {symbol} и дай рекомендацию:
        
        ТЕХНИЧЕСКИЕ ДАННЫЕ:
        - Текущая цена: {current_price}
        - Изменение за 24ч: {price_change}%
        - Объем: {volume}
        - SMA5: {sma_5:.6f}
        - SMA10: {sma_10:.6f}
        - SMA20: {sma_20:.6f}
        - RSI: {rsi:.2f}
        
        СВЕЧНЫЕ ДАННЫЕ (последние 5 свечей):
        {json.dumps(klines_formatted[-5:], indent=2)}
        
        ЗАДАЧА:
        1. Определи тренд и силу движения
        2. Проанализируй технические индикаторы
        3. Дай рекомендацию: LONG, SHORT или NO_SIGNAL
        4. Укажи уровень уверенности (0-100%)
        5. Объясни причину решения
        
        ОТВЕТ в формате JSON:
        {
            "signal": "LONG/SHORT/NO_SIGNAL",
            "confidence": 85,
            "reason": "Краткое объяснение",
            "technical_analysis": "Подробный технический анализ",
            "entry_price": цена_входа,
            "stop_loss": уровень_стоп_лосса,
            "take_profit": уровень_тейк_профита
        }
        """
        
        # Initialize Gemini chat
        chat = LlmChat(
            api_key=GEMINI_API_KEY,
            session_id=f"trading_analysis_{uuid.uuid4()}",
            system_message="Ты эксперт по техническому анализу криптовалют. Анализируй данные и давай точные торговые сигналы."
        ).with_model("gemini", "gemini-2.0-flash")
        
        # Send message to AI
        user_message = UserMessage(text=ai_prompt)
        response = await chat.send_message(user_message)
        
        # Parse AI response
        try:
            ai_result = json.loads(response.strip())
            return ai_result
        except json.JSONDecodeError:
            # Fallback parsing
            return {
                "signal": "NO_SIGNAL",
                "confidence": 0,
                "reason": "Ошибка парсинга AI ответа",
                "technical_analysis": response,
                "entry_price": current_price,
                "stop_loss": current_price * 0.95,
                "take_profit": current_price * 1.05
            }
            
    except Exception as e:
        return {
            "signal": "NO_SIGNAL",
            "confidence": 0,
            "reason": f"Ошибка AI анализа: {str(e)}",
            "technical_analysis": "Анализ недоступен",
            "entry_price": 0,
            "stop_loss": 0,
            "take_profit": 0
        }

# API Routes
@app.get("/")
async def root():
    return {"message": "AI Binance Signals Bot API"}

@app.get("/api/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.now()}

@app.get("/api/trading-pairs")
async def get_trading_pairs():
    """Get available trading pairs"""
    try:
        exchange_info = await get_exchange_info()
        pairs = []
        for symbol in exchange_info["symbols"]:
            if symbol["status"] == "ENABLED" and symbol["quoteAsset"] == "USDT":
                pairs.append({
                    "symbol": symbol["symbol"],
                    "baseAsset": symbol["baseAsset"],
                    "quoteAsset": symbol["quoteAsset"]
                })
        return {"pairs": pairs[:50]}  # Limit to top 50 pairs
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/market-data/{symbol}")
async def get_market_data(symbol: str):
    """Get market data for a symbol"""
    try:
        ticker = await get_ticker_24h(symbol)
        return {
            "symbol": symbol,
            "price": float(ticker["lastPrice"]),
            "change_24h": float(ticker["priceChangePercent"]),
            "volume": float(ticker["volume"]),
            "high_24h": float(ticker["highPrice"]),
            "low_24h": float(ticker["lowPrice"]),
            "timestamp": datetime.now()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/klines/{symbol}/{interval}")
async def get_candlestick_data(symbol: str, interval: str, limit: int = 100):
    """Get candlestick data"""
    try:
        klines = await get_klines(symbol, interval, limit)
        formatted_klines = []
        for kline in klines:
            formatted_klines.append({
                "time": kline[0],
                "open": float(kline[1]),
                "high": float(kline[2]),
                "low": float(kline[3]),
                "close": float(kline[4]),
                "volume": float(kline[5])
            })
        return {"klines": formatted_klines}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/analyze-signal")
async def analyze_trading_signal(request: SignalRequest):
    """Generate AI trading signal"""
    try:
        # Get market data
        klines = await get_klines(request.symbol, request.interval, 100)
        ticker = await get_ticker_24h(request.symbol)
        
        # Analyze with AI
        ai_analysis = await analyze_market_data(request.symbol, klines, ticker)
        
        # Create signal object
        signal = TradingSignal(
            id=str(uuid.uuid4()),
            symbol=request.symbol,
            signal_type=ai_analysis["signal"],
            confidence=ai_analysis["confidence"],
            price=float(ticker["lastPrice"]),
            reason=ai_analysis["reason"],
            technical_analysis=ai_analysis["technical_analysis"],
            timestamp=datetime.now()
        )
        
        # Store in database
        await db.signals.insert_one(signal.dict())
        
        return {
            "signal": signal.dict(),
            "ai_analysis": ai_analysis
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/signals/history")
async def get_signals_history(limit: int = 20):
    """Get trading signals history"""
    try:
        signals = await db.signals.find().sort("timestamp", -1).limit(limit).to_list(length=limit)
        return {"signals": signals}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/top-movers")
async def get_top_movers():
    """Get top price movers"""
    try:
        all_tickers = await get_all_tickers()
        
        # Filter USDT pairs and sort by price change
        usdt_pairs = [
            ticker for ticker in all_tickers 
            if ticker["symbol"].endswith("USDT") and float(ticker["priceChangePercent"]) != 0
        ]
        
        # Sort by price change percentage
        gainers = sorted(usdt_pairs, key=lambda x: float(x["priceChangePercent"]), reverse=True)[:10]
        losers = sorted(usdt_pairs, key=lambda x: float(x["priceChangePercent"]))[:10]
        
        return {
            "gainers": gainers,
            "losers": losers
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)