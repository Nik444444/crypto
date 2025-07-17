import React, { useState, useEffect } from 'react';
import './App.css';

// Telegram WebApp SDK
declare global {
  interface Window {
    Telegram?: {
      WebApp?: {
        ready: () => void;
        expand: () => void;
        MainButton: {
          text: string;
          show: () => void;
          hide: () => void;
        };
        BackButton: {
          show: () => void;
          hide: () => void;
        };
        themeParams: {
          bg_color: string;
          text_color: string;
          hint_color: string;
          button_color: string;
          button_text_color: string;
        };
      };
    };
  }
}

const API_BASE_URL = process.env.REACT_APP_BACKEND_URL || 'http://localhost:8001';

function App() {
  const [currentView, setCurrentView] = useState('dashboard');
  const [selectedSymbol, setSelectedSymbol] = useState('BTCUSDT');
  const [selectedInterval, setSelectedInterval] = useState('1h');
  const [tradingPairs, setTradingPairs] = useState([]);
  const [marketData, setMarketData] = useState(null);
  const [klineData, setKlineData] = useState([]);
  const [currentSignal, setCurrentSignal] = useState(null);
  const [signalsHistory, setSignalsHistory] = useState([]);
  const [topMovers, setTopMovers] = useState({ gainers: [], losers: [] });
  const [isLoading, setIsLoading] = useState(false);

  useEffect(() => {
    // Initialize Telegram WebApp
    if (window.Telegram?.WebApp) {
      window.Telegram.WebApp.ready();
      window.Telegram.WebApp.expand();
    }
    
    // Load initial data
    loadTradingPairs();
    loadTopMovers();
    loadSignalsHistory();
  }, []);

  useEffect(() => {
    if (selectedSymbol) {
      loadMarketData();
      loadKlineData();
    }
  }, [selectedSymbol, selectedInterval]);

  const loadTradingPairs = async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/api/trading-pairs`);
      const data = await response.json();
      setTradingPairs(data.pairs || []);
    } catch (error) {
      console.error('Error loading trading pairs:', error);
    }
  };

  const loadMarketData = async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/api/market-data/${selectedSymbol}`);
      const data = await response.json();
      setMarketData(data);
    } catch (error) {
      console.error('Error loading market data:', error);
    }
  };

  const loadKlineData = async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/api/klines/${selectedSymbol}/${selectedInterval}`);
      const data = await response.json();
      setKlineData(data.klines || []);
    } catch (error) {
      console.error('Error loading kline data:', error);
    }
  };

  const loadSignalsHistory = async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/api/signals/history`);
      const data = await response.json();
      setSignalsHistory(data.signals || []);
    } catch (error) {
      console.error('Error loading signals history:', error);
    }
  };

  const loadTopMovers = async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/api/top-movers`);
      const data = await response.json();
      setTopMovers(data);
    } catch (error) {
      console.error('Error loading top movers:', error);
    }
  };

  const generateSignal = async () => {
    setIsLoading(true);
    try {
      const response = await fetch(`${API_BASE_URL}/api/analyze-signal`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          symbol: selectedSymbol,
          interval: selectedInterval,
        }),
      });
      const data = await response.json();
      setCurrentSignal(data);
      loadSignalsHistory(); // Refresh history
    } catch (error) {
      console.error('Error generating signal:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const formatPrice = (price) => {
    return parseFloat(price).toFixed(6);
  };

  const formatPercent = (percent) => {
    return parseFloat(percent).toFixed(2);
  };

  const getSignalColor = (signalType) => {
    switch (signalType) {
      case 'LONG':
        return '#00C851';
      case 'SHORT':
        return '#FF4444';
      default:
        return '#FFA500';
    }
  };

  const getSignalIcon = (signalType) => {
    switch (signalType) {
      case 'LONG':
        return '📈';
      case 'SHORT':
        return '📉';
      default:
        return '⏸️';
    }
  };

  const renderDashboard = () => (
    <div className="dashboard">
      <div className="header">
        <h1>🤖 AI Торговые Сигналы</h1>
        <p>Анализ криптовалют на MEXC с помощью AI</p>
      </div>

      <div className="trading-pair-selector">
        <select 
          value={selectedSymbol} 
          onChange={(e) => setSelectedSymbol(e.target.value)}
          className="symbol-select"
        >
          {tradingPairs.map(pair => (
            <option key={pair.symbol} value={pair.symbol}>
              {pair.symbol}
            </option>
          ))}
        </select>
        
        <select 
          value={selectedInterval} 
          onChange={(e) => setSelectedInterval(e.target.value)}
          className="interval-select"
        >
          <option value="1m">1 минута</option>
          <option value="5m">5 минут</option>
          <option value="15m">15 минут</option>
          <option value="1h">1 час</option>
          <option value="4h">4 часа</option>
          <option value="1d">1 день</option>
        </select>
      </div>

      {marketData && (
        <div className="market-data-card">
          <h3>{selectedSymbol}</h3>
          <div className="price-info">
            <div className="current-price">
              <span className="price">${formatPrice(marketData.price)}</span>
              <span className={`change ${marketData.change_24h >= 0 ? 'positive' : 'negative'}`}>
                {marketData.change_24h >= 0 ? '+' : ''}{formatPercent(marketData.change_24h)}%
              </span>
            </div>
            <div className="price-details">
              <span>Макс: ${formatPrice(marketData.high_24h)}</span>
              <span>Мин: ${formatPrice(marketData.low_24h)}</span>
              <span>Объем: {formatPrice(marketData.volume)}</span>
            </div>
          </div>
        </div>
      )}

      <div className="chart-container">
        <h3>График цены</h3>
        <div className="simple-chart">
          {klineData.length > 0 ? (
            <div className="chart-placeholder">
              <p>Свечей загружено: {klineData.length}</p>
              <p>Последняя цена: ${formatPrice(klineData[klineData.length - 1]?.close || 0)}</p>
            </div>
          ) : (
            <p>Загрузка данных графика...</p>
          )}
        </div>
      </div>

      <div className="signal-section">
        <button 
          onClick={generateSignal} 
          disabled={isLoading}
          className="generate-signal-btn"
        >
          {isLoading ? 'Анализируем...' : '🔍 Получить AI Сигнал'}
        </button>

        {currentSignal && (
          <div className="signal-card">
            <div className="signal-header">
              <span className="signal-icon">{getSignalIcon(currentSignal.signal.signal_type)}</span>
              <span 
                className="signal-type"
                style={{ color: getSignalColor(currentSignal.signal.signal_type) }}
              >
                {currentSignal.signal.signal_type}
              </span>
              <span className="confidence">
                Уверенность: {currentSignal.signal.confidence}%
              </span>
            </div>
            
            <div className="signal-details">
              <p><strong>Цена входа:</strong> ${formatPrice(currentSignal.signal.price)}</p>
              <p><strong>Причина:</strong> {currentSignal.signal.reason}</p>
              
              {currentSignal.ai_analysis && (
                <div className="ai-analysis">
                  <h4>Технический анализ:</h4>
                  <p>{currentSignal.ai_analysis.technical_analysis}</p>
                  
                  {currentSignal.ai_analysis.entry_price && (
                    <div className="trade-levels">
                      <p><strong>Стоп-лосс:</strong> ${formatPrice(currentSignal.ai_analysis.stop_loss)}</p>
                      <p><strong>Тейк-профит:</strong> ${formatPrice(currentSignal.ai_analysis.take_profit)}</p>
                    </div>
                  )}
                </div>
              )}
            </div>
          </div>
        )}
      </div>

      <div className="navigation">
        <button 
          onClick={() => setCurrentView('history')}
          className="nav-btn"
        >
          📊 История сигналов
        </button>
        <button 
          onClick={() => setCurrentView('movers')}
          className="nav-btn"
        >
          🚀 Топ движения
        </button>
      </div>
    </div>
  );

  const renderHistory = () => (
    <div className="history-view">
      <div className="header">
        <button onClick={() => setCurrentView('dashboard')} className="back-btn">
          ← Назад
        </button>
        <h2>История сигналов</h2>
      </div>
      
      <div className="signals-list">
        {signalsHistory.map((signal) => (
          <div key={signal.id} className="signal-history-item">
            <div className="signal-info">
              <span className="symbol">{signal.symbol}</span>
              <span 
                className="signal-type"
                style={{ color: getSignalColor(signal.signal_type) }}
              >
                {getSignalIcon(signal.signal_type)} {signal.signal_type}
              </span>
              <span className="confidence">{signal.confidence}%</span>
            </div>
            <div className="signal-details">
              <p>${formatPrice(signal.price)}</p>
              <p>{signal.reason}</p>
              <small>{new Date(signal.timestamp).toLocaleString()}</small>
            </div>
          </div>
        ))}
      </div>
    </div>
  );

  const renderMovers = () => (
    <div className="movers-view">
      <div className="header">
        <button onClick={() => setCurrentView('dashboard')} className="back-btn">
          ← Назад
        </button>
        <h2>Топ движения</h2>
      </div>
      
      <div className="movers-container">
        <div className="gainers">
          <h3>🚀 Лидеры роста</h3>
          {topMovers.gainers.map((ticker) => (
            <div key={ticker.symbol} className="mover-item">
              <span className="symbol">{ticker.symbol}</span>
              <span className="price">${formatPrice(ticker.lastPrice)}</span>
              <span className="change positive">
                +{formatPercent(ticker.priceChangePercent)}%
              </span>
            </div>
          ))}
        </div>
        
        <div className="losers">
          <h3>📉 Лидеры падения</h3>
          {topMovers.losers.map((ticker) => (
            <div key={ticker.symbol} className="mover-item">
              <span className="symbol">{ticker.symbol}</span>
              <span className="price">${formatPrice(ticker.lastPrice)}</span>
              <span className="change negative">
                {formatPercent(ticker.priceChangePercent)}%
              </span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );

  return (
    <div className="App">
      {currentView === 'dashboard' && renderDashboard()}
      {currentView === 'history' && renderHistory()}
      {currentView === 'movers' && renderMovers()}
    </div>
  );
}

export default App;