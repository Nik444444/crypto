# 🚀 ДЕПЛОЙ НА FLY.IO - ИСПРАВЛЕННЫЕ КОМАНДЫ

Все файлы исправлены! Проблема была в файле package.json в корне проекта.

## 📋 Готовые команды для деплоя:

### 1. Очистка (если были предыдущие попытки)
```bash
flyctl apps destroy ai-trading-bot-backend
```

### 2. Создание приложения
```bash
flyctl apps create ai-trading-bot-backend --region fra
```

### 3. Деплой приложения
```bash
flyctl deploy --app ai-trading-bot-backend
```

### 4. Добавление переменных окружения
```bash
flyctl secrets set GEMINI_API_KEY="AIzaSyBUedxUkLvRC4-_uA4RNjwoI0nqjmJyk4A" --app ai-trading-bot-backend
flyctl secrets set TELEGRAM_BOT_TOKEN="7509126992:AAH5lvrFcB1fZbHH4VfRu4E8djaA7r19TFY" --app ai-trading-bot-backend
```

### 5. Проверка статуса
```bash
flyctl status --app ai-trading-bot-backend
flyctl logs --app ai-trading-bot-backend
```

## ✅ Что исправлено:

1. **Удален** `package.json` из корня проекта
2. **Удална** папка `node_modules` из корня
3. **Обновлен** `.flyignore` для игнорирования всех Node.js файлов
4. **Создан** `.dockerignore` для Docker
5. **Обновлен** `fly.toml` с правильными настройками

## 🎯 Теперь Fly.io должен определить это как Docker приложение!

После деплоя ваш backend будет доступен на: `https://ai-trading-bot-backend.fly.dev`

Проверьте: `https://ai-trading-bot-backend.fly.dev/api/health`

---

## 🚨 ЕСЛИ ВСЕ ЕЩЕ ОШИБКА:

Попробуйте создать приложение вручную:

```bash
# Создаем приложение без автоматического обнаружения
flyctl apps create ai-trading-bot-backend

# Деплоим принудительно как Docker
flyctl deploy --dockerfile Dockerfile --app ai-trading-bot-backend
```

**Теперь все должно работать! Сохраните на GitHub и попробуйте команды! 🚀**