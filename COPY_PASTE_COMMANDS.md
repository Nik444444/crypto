# 🎯 ФИНАЛЬНЫЕ КОМАНДЫ - ГАРАНТИРОВАННО РАБОТАЮТ!

## ⚡ КОПИРУЙТЕ И ВСТАВЛЯЙТЕ ПО ПОРЯДКУ:

### 1️⃣ Вход в аккаунт
```bash
flyctl auth login
```

### 2️⃣ Создание приложения (БЕЗ launch!)
```bash
flyctl apps create ai-trading-bot-backend
```

### 3️⃣ Установка региона
```bash
flyctl regions set fra --app ai-trading-bot-backend
```

### 4️⃣ Деплой
```bash
flyctl deploy --app ai-trading-bot-backend
```

### 5️⃣ Добавление API ключей
```bash
flyctl secrets set GEMINI_API_KEY="AIzaSyBUedxUkLvRC4-_uA4RNjwoI0nqjmJyk4A" --app ai-trading-bot-backend
flyctl secrets set TELEGRAM_BOT_TOKEN="7509126992:AAH5lvrFcB1fZbHH4VfRu4E8djaA7r19TFY" --app ai-trading-bot-backend
```

### 6️⃣ Проверка
```bash
flyctl status --app ai-trading-bot-backend
```

---

## 🎯 РЕЗУЛЬТАТ:

Ваш backend будет на: `https://ai-trading-bot-backend.fly.dev`

---

**НЕ ИСПОЛЬЗУЙТЕ `flyctl launch` - только эти команды! 🚀**