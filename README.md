# 🤖 AI Trading Bot - Telegram Mini App

Telegram Mini App для получения AI торговых сигналов по криптовалютам с использованием MEXC API и Gemini AI.

## 🚀 Возможности

- 📊 Анализ рынка криптовалют в реальном времени
- 🤖 AI-powered торговые сигналы через Gemini AI
- 📈 Технический анализ с индикаторами (SMA, RSI)
- 📱 Telegram Mini App интерфейс
- 💹 Топ движения рынка (лидеры роста/падения)
- 📝 История торговых сигналов

## 🛠️ Технологии

**Backend:**
- FastAPI (Python)
- SQLite (база данных)
- MEXC API (данные рынка)
- Gemini AI (анализ)
- Fly.io (хостинг)

**Frontend:**
- React 19
- Tailwind CSS
- Telegram WebApp SDK
- Netlify (хостинг)

## 📦 Деплой

Подробная инструкция по деплою находится в файле `DEPLOY_INSTRUCTIONS.md`

### Быстрый старт:
1. Клонируйте репозиторий
2. Создайте аккаунты на Fly.io и Netlify
3. Следуйте инструкциям в `DEPLOY_INSTRUCTIONS.md`

## 🔧 Локальная разработка

### Backend:
```bash
cd backend
pip install -r requirements.txt
python server.py
```

### Frontend:
```bash
cd frontend
npm install
npm start
```

## 📱 Использование

1. Откройте Telegram Mini App через вашего бота
2. Выберите торговую пару (например, BTCUSDT)
3. Выберите временной интервал
4. Нажмите "Получить AI Сигнал"
5. Просмотрите анализ и рекомендации

## 🔑 API Ключи

Для работы необходимы:
- `GEMINI_API_KEY` - для AI анализа
- `TELEGRAM_BOT_TOKEN` - для Telegram интеграции

## 📊 API Endpoints

- `GET /api/health` - проверка состояния
- `GET /api/market-data/{symbol}` - рыночные данные
- `POST /api/analyze-signal` - генерация AI сигнала
- `GET /api/signals/history` - история сигналов
- `GET /api/top-movers` - топ движения

## 🛡️ Безопасность

- Все API ключи хранятся в переменных окружения
- CORS настроен для безопасного доступа
- SQLite база данных изолирована в контейнере

## 📝 Лицензия

MIT License

## 🤝 Поддержка

При возникновении проблем:
1. Проверьте логи в Fly.io Dashboard
2. Проверьте статус деплоя в Netlify
3. Убедитесь, что все переменные окружения настроены правильно

---

**Создано с ❤️ для Telegram Mini Apps**
