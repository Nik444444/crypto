# ✅ Чек-лист перед деплоем

## 📋 Подготовка файлов

- [ ] `backend/server.py` - обновлен для SQLite
- [ ] `backend/requirements.txt` - добавлен aiosqlite
- [ ] `Dockerfile` - добавлен sqlite3
- [ ] `fly.toml` - настроен для Fly.io
- [ ] `netlify.toml` - настроен для Netlify
- [ ] `.env.production` файлы созданы
- [ ] `package.json` в корне проекта
- [ ] `README.md` обновлен

## 🔑 API Ключи

- [ ] `GEMINI_API_KEY`: AIzaSyBUedxUkLvRC4-_uA4RNjwoI0nqjmJyk4A
- [ ] `TELEGRAM_BOT_TOKEN`: 7509126992:AAH5lvrFcB1fZbHH4VfRu4E8djaA7r19TFY

## 🌐 Аккаунты

- [ ] Fly.io аккаунт создан
- [ ] Netlify аккаунт создан
- [ ] GitHub репозиторий создан
- [ ] Код загружен на GitHub

## 🚀 Деплой Backend (Fly.io)

- [ ] Приложение создано на Fly.io
- [ ] Dockerfile путь указан правильно
- [ ] Переменные окружения добавлены
- [ ] Деплой завершен успешно
- [ ] URL работает: `https://ваш-backend.fly.dev/api/health`

## 🎨 Деплой Frontend (Netlify)

- [ ] Сайт создан на Netlify
- [ ] Подключен GitHub репозиторий
- [ ] Build settings правильные
- [ ] Environment variables добавлены
- [ ] Деплой завершен успешно
- [ ] URL работает: `https://ваш-сайт.netlify.app`

## 📱 Telegram Mini App

- [ ] Web App создан через BotFather
- [ ] URL от Netlify добавлен в BotFather
- [ ] Получена ссылка на Mini App
- [ ] Приложение открывается в Telegram

## 🧪 Тестирование

### Backend API:
- [ ] `/api/health` - возвращает healthy
- [ ] `/api/trading-pairs` - возвращает список пар
- [ ] `/api/market-data/METALUSDT` - возвращает данные

### Frontend:
- [ ] Главная страница загружается
- [ ] Торговые пары отображаются
- [ ] Рыночные данные загружаются
- [ ] Кнопка "Получить AI Сигнал" работает

### Telegram Mini App:
- [ ] Открывается в Telegram
- [ ] Все функции работают
- [ ] Интерфейс адаптирован для мобильного

## 🔧 Финальные настройки

- [ ] URL в `frontend/.env.production` обновлен на реальный от Fly.io
- [ ] GitHub репозиторий обновлен с правильным URL
- [ ] Все файлы закоммичены
- [ ] Автоматический деплой настроен (опционально)

## 📞 Поддержка

Если что-то не работает:
1. Проверьте `TROUBLESHOOTING.md`
2. Посмотрите логи на Fly.io и Netlify
3. Убедитесь, что все переменные окружения правильные

---

**🎉 Готово! Ваш AI Trading Bot готов к использованию!**