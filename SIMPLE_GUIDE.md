# 🎯 ПРОСТАЯ ИНСТРУКЦИЯ - ТОЛЬКО КНОПКИ

## 1️⃣ ЗАГРУЗИТЬ КОД НА GITHUB
1. Откройте https://github.com/new
2. Название: `ai-trading-bot-telegram`
3. Нажмите **"Create repository"**
4. Нажмите **"uploading an existing file"**
5. Перетащите ВСЕ файлы проекта
6. Нажмите **"Commit changes"**

## 2️⃣ ПОЛУЧИТЬ ТОКЕН FLY.IO
1. Откройте https://fly.io/user/personal_access_tokens
2. Нажмите **"Create token"**
3. Скопируйте токен

## 3️⃣ ДОБАВИТЬ ТОКЕН В GITHUB
1. В репозитории: **Settings** → **Secrets and variables** → **Actions**
2. Нажмите **"New repository secret"**
3. Name: `FLY_API_TOKEN`
4. Value: вставьте токен
5. Нажмите **"Add secret"**

## 4️⃣ ПОЛУЧИТЬ ТОКЕН NETLIFY
1. Откройте https://app.netlify.com/user/applications#personal-access-tokens
2. Нажмите **"New access token"**
3. Скопируйте токен

## 5️⃣ СОЗДАТЬ САЙТ НА NETLIFY
1. Откройте https://app.netlify.com/
2. Нажмите **"New site from Git"**
3. Выберите ваш репозиторий
4. Нажмите **"Deploy site"**
5. Скопируйте **Site ID** из настроек

## 6️⃣ ДОБАВИТЬ ТОКЕНЫ NETLIFY В GITHUB
1. В GitHub: **Settings** → **Secrets and variables** → **Actions**
2. Добавьте:
   - `NETLIFY_AUTH_TOKEN` = токен
   - `NETLIFY_SITE_ID` = Site ID

## 7️⃣ ЗАПУСТИТЬ АВТОДЕПЛОЙ
1. В GitHub: **Actions**
2. Выберите **"Auto Deploy to Fly.io and Netlify"**
3. Нажмите **"Run workflow"**
4. Нажмите **"Run workflow"**

## 🎉 ГОТОВО!
Через 5-10 минут все будет развернуто автоматически!

---

**ТОЛЬКО КНОПКИ, НИКАКИХ КОМАНД! 🚀**