# 🚀 ИСПРАВЛЕННЫЕ КОМАНДЫ ДЛЯ FLY.IO

## 🔧 ДРУГОЙ ПОДХОД - БЕЗ LAUNCH

Проблема в конфликте манифестов. Давайте создадим приложение по-другому:

### ШАГ 1: Вход в аккаунт
```bash
flyctl auth login
```

### ШАГ 2: Создание приложения напрямую
```bash
flyctl apps create ai-trading-bot-backend
```

### ШАГ 3: Установка региона
```bash
flyctl regions set fra --app ai-trading-bot-backend
```

### ШАГ 4: Деплой приложения
```bash
flyctl deploy --app ai-trading-bot-backend
```

### ШАГ 5: Добавление переменных окружения
```bash
flyctl secrets set GEMINI_API_KEY="AIzaSyBUedxUkLvRC4-_uA4RNjwoI0nqjmJyk4A" --app ai-trading-bot-backend
flyctl secrets set TELEGRAM_BOT_TOKEN="7509126992:AAH5lvrFcB1fZbHH4VfRu4E8djaA7r19TFY" --app ai-trading-bot-backend
```

---

## 🎯 АЛЬТЕРНАТИВНЫЙ СПОСОБ - ЧЕРЕЗ ВЕБ-ИНТЕРФЕЙС

### Способ 1: Создание через Dashboard
1. Откройте https://fly.io/dashboard
2. Нажмите "Create app"
3. Выберите "Blank app"
4. Название: `ai-trading-bot-backend`
5. Регион: `Frankfurt (fra)`
6. Нажмите "Create"

Затем в командной строке:
```bash
flyctl deploy --app ai-trading-bot-backend
```

---

## 🔧 ЕСЛИ ВСЕ ЕЩЕ НЕ РАБОТАЕТ

### Способ 2: Принудительный деплой
```bash
# Создаем приложение
flyctl apps create ai-trading-bot-backend

# Деплоим с принудительным Dockerfile
flyctl deploy --dockerfile ./Dockerfile --app ai-trading-bot-backend
```

### Способ 3: Проверка файлов
```bash
# Проверим что у нас есть
ls -la | grep -E "(Dockerfile|fly.toml)"

# Проверим содержимое Dockerfile
head -5 Dockerfile
```

---

## ✅ ГЛАВНОЕ - НЕ ИСПОЛЬЗУЙТЕ `flyctl launch`

Используйте:
- `flyctl apps create` - для создания приложения
- `flyctl deploy` - для деплоя

**Попробуйте команды выше! Теперь должно работать! 🚀**