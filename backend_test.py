#!/usr/bin/env python3
"""
Backend API Testing for AI Trading Bot
Tests all backend endpoints and functionality
"""

import requests
import json
import time
from datetime import datetime
import os

# Get backend URL from frontend .env
def get_backend_url():
    try:
        with open('/app/frontend/.env', 'r') as f:
            for line in f:
                if line.startswith('REACT_APP_BACKEND_URL='):
                    return line.split('=', 1)[1].strip()
    except Exception as e:
        print(f"Error reading frontend .env: {e}")
        return None

BACKEND_URL = get_backend_url()
if not BACKEND_URL:
    print("ERROR: Could not get REACT_APP_BACKEND_URL from frontend/.env")
    exit(1)

print(f"Testing backend at: {BACKEND_URL}")

class BackendTester:
    def __init__(self, base_url):
        self.base_url = base_url
        self.session = requests.Session()
        self.test_results = []
        
    def log_test(self, test_name, success, details="", response_data=None):
        """Log test results"""
        result = {
            "test": test_name,
            "success": success,
            "details": details,
            "timestamp": datetime.now().isoformat(),
            "response_data": response_data
        }
        self.test_results.append(result)
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} {test_name}: {details}")
        
    def test_health_endpoint(self):
        """Test GET /api/health"""
        try:
            response = self.session.get(f"{self.base_url}/api/health", timeout=10)
            if response.status_code == 200:
                data = response.json()
                if "status" in data and data["status"] == "healthy":
                    self.log_test("Health Check", True, "Service is healthy", data)
                    return True
                else:
                    self.log_test("Health Check", False, f"Invalid health response: {data}")
            else:
                self.log_test("Health Check", False, f"HTTP {response.status_code}: {response.text}")
        except Exception as e:
            self.log_test("Health Check", False, f"Request failed: {str(e)}")
        return False
        
    def test_trading_pairs(self):
        """Test GET /api/trading-pairs"""
        try:
            response = self.session.get(f"{self.base_url}/api/trading-pairs", timeout=15)
            if response.status_code == 200:
                data = response.json()
                if "pairs" in data and isinstance(data["pairs"], list) and len(data["pairs"]) > 0:
                    sample_pair = data["pairs"][0]
                    if "symbol" in sample_pair and "baseAsset" in sample_pair:
                        self.log_test("Trading Pairs", True, f"Retrieved {len(data['pairs'])} trading pairs", 
                                    {"sample_pair": sample_pair, "total_pairs": len(data["pairs"])})
                        return True
                    else:
                        self.log_test("Trading Pairs", False, f"Invalid pair structure: {sample_pair}")
                else:
                    self.log_test("Trading Pairs", False, f"No pairs in response: {data}")
            else:
                self.log_test("Trading Pairs", False, f"HTTP {response.status_code}: {response.text}")
        except Exception as e:
            self.log_test("Trading Pairs", False, f"Request failed: {str(e)}")
        return False
        
    def test_market_data(self, symbol="BTCUSDT"):
        """Test GET /api/market-data/{symbol}"""
        try:
            response = self.session.get(f"{self.base_url}/api/market-data/{symbol}", timeout=15)
            if response.status_code == 200:
                data = response.json()
                required_fields = ["symbol", "price", "change_24h", "volume"]
                if all(field in data for field in required_fields):
                    price = data["price"]
                    if isinstance(price, (int, float)) and price > 0:
                        self.log_test("Market Data", True, f"Retrieved {symbol} data: ${price:,.2f}", 
                                    {"symbol": symbol, "price": price, "change_24h": data["change_24h"]})
                        return True
                    else:
                        self.log_test("Market Data", False, f"Invalid price data: {price}")
                else:
                    missing = [f for f in required_fields if f not in data]
                    self.log_test("Market Data", False, f"Missing fields: {missing}")
            else:
                self.log_test("Market Data", False, f"HTTP {response.status_code}: {response.text}")
        except Exception as e:
            self.log_test("Market Data", False, f"Request failed: {str(e)}")
        return False
        
    def test_klines_data(self, symbol="BTCUSDT", interval="1h"):
        """Test GET /api/klines/{symbol}/{interval}"""
        try:
            response = self.session.get(f"{self.base_url}/api/klines/{symbol}/{interval}", timeout=15)
            if response.status_code == 200:
                data = response.json()
                if "klines" in data and isinstance(data["klines"], list) and len(data["klines"]) > 0:
                    sample_kline = data["klines"][0]
                    required_fields = ["time", "open", "high", "low", "close", "volume"]
                    if all(field in sample_kline for field in required_fields):
                        self.log_test("Klines Data", True, f"Retrieved {len(data['klines'])} candles for {symbol}", 
                                    {"symbol": symbol, "interval": interval, "candles_count": len(data["klines"]),
                                     "latest_close": data["klines"][-1]["close"]})
                        return True
                    else:
                        missing = [f for f in required_fields if f not in sample_kline]
                        self.log_test("Klines Data", False, f"Missing kline fields: {missing}")
                else:
                    self.log_test("Klines Data", False, f"No klines in response: {data}")
            else:
                self.log_test("Klines Data", False, f"HTTP {response.status_code}: {response.text}")
        except Exception as e:
            self.log_test("Klines Data", False, f"Request failed: {str(e)}")
        return False
        
    def test_ai_signal_analysis(self, symbol="BTCUSDT", interval="1h"):
        """Test POST /api/analyze-signal"""
        try:
            payload = {"symbol": symbol, "interval": interval}
            response = self.session.post(f"{self.base_url}/api/analyze-signal", 
                                       json=payload, timeout=30)
            if response.status_code == 200:
                data = response.json()
                if "signal" in data and "ai_analysis" in data:
                    signal = data["signal"]
                    ai_analysis = data["ai_analysis"]
                    
                    # Check signal structure
                    signal_fields = ["id", "symbol", "signal_type", "confidence", "price", "reason"]
                    if all(field in signal for field in signal_fields):
                        signal_type = signal["signal_type"]
                        confidence = signal["confidence"]
                        
                        if signal_type in ["LONG", "SHORT", "NO_SIGNAL"]:
                            self.log_test("AI Signal Analysis", True, 
                                        f"Generated {signal_type} signal with {confidence}% confidence", 
                                        {"signal_type": signal_type, "confidence": confidence, 
                                         "reason": signal["reason"][:100]})
                            return True
                        else:
                            self.log_test("AI Signal Analysis", False, f"Invalid signal type: {signal_type}")
                    else:
                        missing = [f for f in signal_fields if f not in signal]
                        self.log_test("AI Signal Analysis", False, f"Missing signal fields: {missing}")
                else:
                    self.log_test("AI Signal Analysis", False, f"Missing signal or ai_analysis in response")
            else:
                self.log_test("AI Signal Analysis", False, f"HTTP {response.status_code}: {response.text}")
        except Exception as e:
            self.log_test("AI Signal Analysis", False, f"Request failed: {str(e)}")
        return False
        
    def test_signals_history(self):
        """Test GET /api/signals/history"""
        try:
            response = self.session.get(f"{self.base_url}/api/signals/history", timeout=15)
            if response.status_code == 200:
                data = response.json()
                if "signals" in data and isinstance(data["signals"], list):
                    signals_count = len(data["signals"])
                    if signals_count > 0:
                        sample_signal = data["signals"][0]
                        self.log_test("Signals History", True, f"Retrieved {signals_count} historical signals", 
                                    {"signals_count": signals_count, "latest_signal": sample_signal.get("symbol", "N/A")})
                    else:
                        self.log_test("Signals History", True, "No historical signals found (empty database)", 
                                    {"signals_count": 0})
                    return True
                else:
                    self.log_test("Signals History", False, f"Invalid response structure: {data}")
            else:
                self.log_test("Signals History", False, f"HTTP {response.status_code}: {response.text}")
        except Exception as e:
            self.log_test("Signals History", False, f"Request failed: {str(e)}")
        return False
        
    def test_top_movers(self):
        """Test GET /api/top-movers"""
        try:
            response = self.session.get(f"{self.base_url}/api/top-movers", timeout=20)
            if response.status_code == 200:
                data = response.json()
                if "gainers" in data and "losers" in data:
                    gainers = data["gainers"]
                    losers = data["losers"]
                    
                    if isinstance(gainers, list) and isinstance(losers, list):
                        gainers_count = len(gainers)
                        losers_count = len(losers)
                        
                        # Check structure of first gainer if available
                        if gainers_count > 0:
                            top_gainer = gainers[0]
                            if "symbol" in top_gainer and "priceChangePercent" in top_gainer:
                                self.log_test("Top Movers", True, 
                                            f"Retrieved {gainers_count} gainers, {losers_count} losers", 
                                            {"top_gainer": top_gainer["symbol"], 
                                             "top_gainer_change": top_gainer["priceChangePercent"]})
                                return True
                            else:
                                self.log_test("Top Movers", False, f"Invalid gainer structure: {top_gainer}")
                        else:
                            self.log_test("Top Movers", True, "No gainers/losers found (market data issue)", 
                                        {"gainers_count": gainers_count, "losers_count": losers_count})
                            return True
                    else:
                        self.log_test("Top Movers", False, f"Gainers/losers not lists: {type(gainers)}, {type(losers)}")
                else:
                    self.log_test("Top Movers", False, f"Missing gainers/losers in response: {data}")
            else:
                self.log_test("Top Movers", False, f"HTTP {response.status_code}: {response.text}")
        except Exception as e:
            self.log_test("Top Movers", False, f"Request failed: {str(e)}")
        return False
        
    def test_mexc_integration(self):
        """Test MEXC API integration by checking data quality"""
        print("\n🔍 Testing MEXC API Integration...")
        
        # Test if we can get real market data
        market_success = self.test_market_data("BTCUSDT")
        klines_success = self.test_klines_data("BTCUSDT", "1h")
        pairs_success = self.test_trading_pairs()
        
        if market_success and klines_success and pairs_success:
            self.log_test("MEXC Integration", True, "All MEXC endpoints working correctly")
            return True
        else:
            self.log_test("MEXC Integration", False, "Some MEXC endpoints failing")
            return False
            
    def test_mongodb_integration(self):
        """Test MongoDB integration"""
        print("\n🗄️ Testing MongoDB Integration...")
        
        # First generate a signal to test database write
        ai_success = self.test_ai_signal_analysis("BTCUSDT", "1h")
        
        # Then test reading history
        history_success = self.test_signals_history()
        
        if ai_success and history_success:
            self.log_test("MongoDB Integration", True, "Database read/write operations working")
            return True
        else:
            self.log_test("MongoDB Integration", False, "Database operations failing")
            return False
            
    def run_all_tests(self):
        """Run all backend tests"""
        print("🚀 Starting Backend API Tests...")
        print("=" * 60)
        
        # Basic endpoint tests
        print("\n📡 Testing Basic Endpoints...")
        self.test_health_endpoint()
        self.test_trading_pairs()
        self.test_market_data("BTCUSDT")
        self.test_klines_data("BTCUSDT", "1h")
        
        # AI functionality test
        print("\n🤖 Testing AI Functionality...")
        self.test_ai_signal_analysis("BTCUSDT", "1h")
        
        # Integration tests
        self.test_mexc_integration()
        self.test_mongodb_integration()
        
        # Additional endpoints
        print("\n📈 Testing Additional Features...")
        self.test_top_movers()
        
        # Summary
        print("\n" + "=" * 60)
        print("📊 TEST SUMMARY")
        print("=" * 60)
        
        passed = sum(1 for result in self.test_results if result["success"])
        total = len(self.test_results)
        
        print(f"Total Tests: {total}")
        print(f"Passed: {passed}")
        print(f"Failed: {total - passed}")
        print(f"Success Rate: {(passed/total)*100:.1f}%")
        
        print("\n📋 Detailed Results:")
        for result in self.test_results:
            status = "✅" if result["success"] else "❌"
            print(f"{status} {result['test']}: {result['details']}")
            
        return passed == total

if __name__ == "__main__":
    tester = BackendTester(BACKEND_URL)
    success = tester.run_all_tests()
    
    if success:
        print("\n🎉 All tests passed! Backend is working correctly.")
        exit(0)
    else:
        print("\n⚠️ Some tests failed. Check the details above.")
        exit(1)