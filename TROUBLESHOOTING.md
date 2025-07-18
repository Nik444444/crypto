# 🔧 Troubleshooting Guide

## Проблемы с Backend (Fly.io)

### ❌ Backend не запускается
**Симптомы:** Сайт не отвечает, показывает "Service Unavailable"

**Решение:**
1. Откройте Fly.io Dashboard
2. Перейдите в ваше приложение
3. Откройте "Monitoring" → "Logs"
4. Найдите ошибки в логах
5. Чаще всего проблема в переменных окружения

### ❌ Ошибка "GEMINI_API_KEY not found"
**Симптомы:** AI сигналы не генерируются

**Решение:**
1. Fly.io Dashboard → Ваше приложение → "Settings" → "Environment"
2. Добавьте `GEMINI_API_KEY` со значением вашего ключа
3. Restart приложение

### ❌ SQLite ошибки
**Симптомы:** Ошибки при сохранении данных

**Решение:**
1. Проверьте права доступа к файлу базы данных
2. Перезапустите приложение через Fly.io Dashboard
3. База данных создастся автоматически при первом запуске

---

## Проблемы с Frontend (Netlify)

### ❌ Frontend не загружается
**Симптомы:** Белый экран, ошибка 404

**Решение:**
1. Netlify Dashboard → Ваш сайт → "Deploys"
2. Проверьте статус последнего деплоя
3. Если failed - посмотрите логи
4. Чаще всего проблема в build команде

### ❌ API запросы не работают
**Симптомы:** Данные не загружаются, ошибки CORS

**Решение:**
1. Netlify Dashboard → Site settings → Environment variables
2. Проверьте правильность `REACT_APP_BACKEND_URL`
3. URL должен быть: `https://ваш-backend.fly.dev`
4. Без слэша в конце!

### ❌ Build fails
**Симптомы:** Деплой прерывается с ошибкой

**Решение:**
1. Проверьте логи в Netlify Dashboard
2. Убедитесь, что `netlify.toml` правильно настроен
3. Build command: `cd frontend && npm install && npm run build`
4. Publish directory: `frontend/build`

---

## Проблемы с Telegram Mini App

### ❌ Mini App не открывается
**Симптомы:** Ошибка при открытии в Telegram

**Решение:**
1. Проверьте, что URL в BotFather правильный
2. URL должен быть: `https://ваш-сайт.netlify.app`
3. Попробуйте пересоздать Web App в BotFather

### ❌ Приложение медленно работает
**Симптомы:** Долгая загрузка, тормоза

**Решение:**
1. Проверьте логи backend на Fly.io
2. Возможно, нужно увеличить ресурсы в Fly.io
3. Проверьте сетевое соединение

---

## Общие проблемы

### ❌ Данные не сохраняются
**Симптомы:** История сигналов пропадает

**Причина:** SQLite база данных хранится в контейнере

**Решение:**
1. Это нормально для текущей конфигурации
2. Для постоянного хранения нужна внешняя база
3. Данные восстанавливаются при новых сигналах

### ❌ Превышены лимиты
**Симптомы:** Сервисы перестают работать

**Решение:**
1. **Fly.io**: 160 часов/месяц бесплатно
2. **Netlify**: 100GB трафика/месяц
3. **Gemini API**: проверьте лимиты в Google Cloud Console

---

## Команды для проверки

### Проверка Backend:
```
https://ваш-backend.fly.dev/api/health
```
Должен вернуть: `{"status": "healthy", "timestamp": "..."}`

### Проверка Frontend:
```
https://ваш-сайт.netlify.app
```
Должен загрузиться интерфейс приложения

### Проверка API:
```
https://ваш-backend.fly.dev/api/trading-pairs
```
Должен вернуть список торговых пар

---

## Контакты поддержки

**Fly.io Support:**
- https://fly.io/docs/getting-started/troubleshooting/
- Community: https://community.fly.io/

**Netlify Support:**
- https://docs.netlify.com/
- Community: https://answers.netlify.com/

**Gemini AI:**
- https://ai.google.dev/docs
- API Console: https://console.cloud.google.com/

---

## Полезные ссылки

- [Fly.io Dashboard](https://fly.io/dashboard)
- [Netlify Dashboard](https://app.netlify.com/)
- [GitHub Repository](https://github.com/yourusername/ai-trading-bot-telegram)
- [Telegram BotFather](https://t.me/BotFather)

**Если проблема не решается - проверьте каждый шаг в DEPLOY_INSTRUCTIONS.md еще раз!**