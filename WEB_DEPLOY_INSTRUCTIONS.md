# 🚀 АВТОДЕПЛОЙ БЕЗ КОМАНДНОЙ СТРОКИ

## 📋 Что нужно сделать:
1. Загрузить код на GitHub
2. Настроить автодеплой через веб-интерфейсы
3. Нажать кнопку "Deploy" - все готово!

---

## 🔧 ЭТАП 1: ЗАГРУЗКА КОДА НА GITHUB

### 1.1 Создаем репозиторий
1. Откройте https://github.com/new
2. Название: `ai-trading-bot-telegram`
3. Выберите **"Public"**
4. Нажмите **"Create repository"**

### 1.2 Загружаем файлы
1. На странице репозитория нажмите **"uploading an existing file"**
2. Перетащите ВСЕ файлы из папки проекта
3. Напишите: "Initial commit"
4. Нажмите **"Commit changes"**

---

## 🔧 ЭТАП 2: НАСТРОЙКА АВТОДЕПЛОЯ FLY.IO

### 2.1 Получаем API токен Fly.io
1. Откройте https://fly.io/user/personal_access_tokens
2. Нажмите **"Create token"**
3. Название: `GitHub Actions`
4. Скопируйте токен (он показывается один раз!)

### 2.2 Добавляем токен в GitHub
1. В вашем репозитории GitHub откройте **"Settings"**
2. Слева выберите **"Secrets and variables"** → **"Actions"**
3. Нажмите **"New repository secret"**
4. Name: `FLY_API_TOKEN`
5. Value: вставьте скопированный токен
6. Нажмите **"Add secret"**

---

## 🔧 ЭТАП 3: НАСТРОЙКА АВТОДЕПЛОЯ NETLIFY

### 3.1 Получаем токены Netlify
1. Откройте https://app.netlify.com/user/applications#personal-access-tokens
2. Нажмите **"New access token"**
3. Название: `GitHub Actions`
4. Скопируйте токен

### 3.2 Создаем сайт на Netlify
1. Откройте https://app.netlify.com/
2. Нажмите **"New site from Git"**
3. Выберите **"GitHub"**
4. Выберите репозиторий `ai-trading-bot-telegram`
5. **НЕ НАСТРАИВАЙТЕ BUILD SETTINGS** - просто нажмите **"Deploy site"**
6. После создания зайдите в **"Site settings"**
7. Скопируйте **"Site ID"** (в разделе Site information)

### 3.3 Добавляем токены в GitHub
1. В GitHub репозитории: **"Settings"** → **"Secrets and variables"** → **"Actions"**
2. Добавьте секрет:
   - Name: `NETLIFY_AUTH_TOKEN`
   - Value: токен от Netlify
3. Добавьте еще секрет:
   - Name: `NETLIFY_SITE_ID`
   - Value: Site ID от Netlify

---

## 🎯 ЭТАП 4: АВТОДЕПЛОЙ ГОТОВ!

### 4.1 Запуск автодеплоя
1. В GitHub репозитории откройте **"Actions"**
2. Выберите **"Auto Deploy to Fly.io and Netlify"**
3. Нажмите **"Run workflow"**
4. Нажмите зеленую кнопку **"Run workflow"**

### 4.2 Ожидание результата
1. Дождитесь выполнения (5-10 минут)
2. Если все зеленое ✅ - деплой успешен!
3. Если красное ❌ - посмотрите логи ошибок

---

## 🎉 РЕЗУЛЬТАТ

После успешного автодеплоя:
- **Backend**: `https://ai-trading-bot-backend.fly.dev`
- **Frontend**: `https://ваш-сайт.netlify.app`

---

## 🔧 НАСТРОЙКА TELEGRAM BOT

### Создание Mini App
1. Найдите в Telegram: **@BotFather**
2. Отправьте: `/newapp`
3. Выберите вашего бота
4. Название: `AI Trading Signals`
5. Описание: `AI торговые сигналы`
6. URL: `https://ваш-сайт.netlify.app`

---

## 🎯 ГОТОВО!

Теперь при каждом изменении кода на GitHub автоматически будет происходить деплой на Fly.io и Netlify!

**Просто загружайте код на GitHub и все развернется автоматически! 🚀**