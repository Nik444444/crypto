# 🚨 ВАЖНО! НЕ ИСПОЛЬЗУЙТЕ `flyctl launch`

## ❌ НЕ ДЕЛАЙТЕ:
```bash
flyctl launch  # ← ЭТО ВЫЗЫВАЕТ ОШИБКУ!
```

## ✅ ДЕЛАЙТЕ ТАК:

### 1. Создаем приложение через веб-интерфейс
1. Откройте https://fly.io/dashboard
2. Нажмите **"Create app"**
3. Выберите **"Blank app"**
4. Название: `ai-trading-bot-backend`
5. Регион: `Frankfurt (fra)`
6. Нажмите **"Create app"**

### 2. Затем в командной строке:
```bash
# Переходим в папку проекта
cd путь\к\вашему\проекту

# Деплоим напрямую
flyctl deploy --app ai-trading-bot-backend --dockerfile Dockerfile

# Добавляем переменные окружения
flyctl secrets set GEMINI_API_KEY="AIzaSyBUedxUkLvRC4-_uA4RNjwoI0nqjmJyk4A" --app ai-trading-bot-backend
flyctl secrets set TELEGRAM_BOT_TOKEN="7509126992:AAH5lvrFcB1fZbHH4VfRu4E8djaA7r19TFY" --app ai-trading-bot-backend
```

---

## 🎯 АЛЬТЕРНАТИВНЫЙ СПОСОБ - ЧЕРЕЗ CLI

```bash
# 1. Создаем приложение БЕЗ launch
flyctl apps create ai-trading-bot-backend

# 2. Деплоим с указанием Dockerfile
flyctl deploy --app ai-trading-bot-backend --dockerfile ./Dockerfile

# 3. Добавляем переменные
flyctl secrets set GEMINI_API_KEY="AIzaSyBUedxUkLvRC4-_uA4RNjwoI0nqjmJyk4A" --app ai-trading-bot-backend
flyctl secrets set TELEGRAM_BOT_TOKEN="7509126992:AAH5lvrFcB1fZbHH4VfRu4E8djaA7r19TFY" --app ai-trading-bot-backend
```

---

**ГЛАВНОЕ: НЕ ИСПОЛЬЗУЙТЕ `flyctl launch`! Используйте `flyctl apps create` или веб-интерфейс! 🚀**