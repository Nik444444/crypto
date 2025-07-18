# 🚀 ДЕПЛОЙ НА FLY.IO - ГОТОВЫЕ КОМАНДЫ

Все файлы исправлены! Теперь просто выполните эти команды:

## 📋 Команды для деплоя:

### 1. Создаем приложение
```bash
flyctl apps create ai-trading-bot-backend --region fra
```

### 2. Деплоим приложение
```bash
flyctl deploy --app ai-trading-bot-backend
```

### 3. Добавляем переменные окружения
```bash
flyctl secrets set GEMINI_API_KEY="AIzaSyBUedxUkLvRC4-_uA4RNjwoI0nqjmJyk4A" --app ai-trading-bot-backend
flyctl secrets set TELEGRAM_BOT_TOKEN="7509126992:AAH5lvrFcB1fZbHH4VfRu4E8djaA7r19TFY" --app ai-trading-bot-backend
```

### 4. Проверяем статус
```bash
flyctl status --app ai-trading-bot-backend
```

## ✅ Что исправлено:

1. **fly.toml** - убрана лишняя секция services
2. **.flyignore** - добавлен для игнорирования frontend папки
3. **Dockerfile** - добавлены правильные права доступа
4. **server.py** - путь к базе данных исправлен для production
5. **package.json** - добавлен engines для Node.js версии

## 🎯 После деплоя:

Ваш backend будет доступен на: `https://ai-trading-bot-backend.fly.dev`

Проверьте: `https://ai-trading-bot-backend.fly.dev/api/health`

---

**Все готово для деплоя! Сохраните на GitHub и выполните команды выше! 🚀**