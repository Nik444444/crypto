# 🚀 ПОШАГОВАЯ ИНСТРУКЦИЯ ПО ДЕПЛОЮ TELEGRAM MINI APP

## 📋 Что мы деплоим:
- **Backend** (FastAPI + SQLite) → Fly.io
- **Frontend** (React) → Netlify
- **База данных** → SQLite (внутри backend)

---

## 🔧 ЭТАП 1: ПОДГОТОВКА АККАУНТОВ

### 1.1 Создаем аккаунт на Fly.io
1. Откройте https://fly.io/app/sign-up
2. Нажмите "Sign up with GitHub" (рекомендуется)
3. Авторизуйтесь через GitHub
4. Подтвердите email если потребуется
5. Вы попадете в Dashboard Fly.io

### 1.2 Создаем аккаунт на Netlify
1. Откройте https://app.netlify.com/signup
2. Нажмите "Sign up with GitHub" 
3. Авторизуйтесь через GitHub
4. Подтвердите email если потребуется
5. Вы попадете в Dashboard Netlify

---

## 🔧 ЭТАП 2: ПОДГОТОВКА КОДА НА GITHUB

### 2.1 Создаем репозиторий на GitHub
1. Откройте https://github.com/new
2. Название: `ai-trading-bot-telegram`
3. Описание: `AI Trading Bot for Telegram Mini App`
4. Выберите "Public" (чтобы Netlify мог деплоить бесплатно)
5. Нажмите "Create repository"

### 2.2 Загружаем код
1. На странице нового репозитория нажмите "uploading an existing file"
2. Откройте папку с вашим проектом на компьютере
3. Выберите ВСЕ файлы и папки (кроме node_modules если есть)
4. Перетащите их в окно GitHub
5. В поле "Commit changes" напишите: "Initial commit - AI Trading Bot"
6. Нажмите "Commit changes"

**⚠️ ВАЖНО:** Убедитесь, что загрузились:
- Папка `backend/` со всеми файлами
- Папка `frontend/` со всеми файлами
- Файл `Dockerfile`
- Файл `fly.toml`
- Файл `netlify.toml`

---

## 🔧 ЭТАП 3: ДЕПЛОЙ BACKEND НА FLY.IO

### 3.1 Создаем приложение на Fly.io
1. Откройте https://fly.io/dashboard
2. Нажмите "Create app"
3. Выберите "Deploy from GitHub"
4. Найдите ваш репозиторий `ai-trading-bot-telegram`
5. Нажмите "Connect"

### 3.2 Настройка деплоя
1. В поле "App name" введите: `ai-trading-bot-backend` (или любое уникальное имя)
2. В поле "Region" оставьте: `Frankfurt, Germany (fra)`
3. В разделе "Build settings":
   - Dockerfile path: `Dockerfile`
   - Build context: `./` (корень репозитория)
4. Нажмите "Deploy"

### 3.3 Добавление переменных окружения
1. После деплоя зайдите в настройки вашего приложения
2. Найдите раздел "Environment variables"
3. Добавьте переменные:
   - `GEMINI_API_KEY`: `AIzaSyBUedxUkLvRC4-_uA4RNjwoI0nqjmJyk4A`
   - `TELEGRAM_BOT_TOKEN`: `7509126992:AAH5lvrFcB1fZbHH4VfRu4E8djaA7r19TFY`
4. Нажмите "Save"

### 3.4 Проверка деплоя
1. Дождитесь окончания деплоя (обычно 2-5 минут)
2. Вы получите URL вида: `https://ai-trading-bot-backend.fly.dev`
3. Откройте этот URL в браузере
4. Должно появиться: `{"message": "AI Trading Signals Bot API"}`
5. Проверьте health: `https://ai-trading-bot-backend.fly.dev/api/health`

**✅ BACKEND ГОТОВ!** Запишите ваш URL - он понадобится для frontend.

---

## 🔧 ЭТАП 4: ОБНОВЛЕНИЕ FRONTEND ДЛЯ PRODUCTION

### 4.1 Обновляем URL backend
1. В вашем репозитории откройте файл `frontend/.env.production`
2. Замените URL на ваш реальный от Fly.io:
   ```
   REACT_APP_BACKEND_URL=https://ВАШ-APP-NAME.fly.dev
   ```
3. Сохраните файл

### 4.2 Коммитим изменения
1. На GitHub перейдите в файл `frontend/.env.production`
2. Нажмите карандашик для редактирования
3. Замените URL на ваш
4. Нажмите "Commit changes"

---

## 🔧 ЭТАП 5: ДЕПЛОЙ FRONTEND НА NETLIFY

### 5.1 Создаем сайт на Netlify
1. Откройте https://app.netlify.com/
2. Нажмите "New site from Git"
3. Выберите "GitHub" 
4. Найдите ваш репозиторий `ai-trading-bot-telegram`
5. Нажмите на него

### 5.2 Настройка деплоя
1. **Branch to deploy**: `main` (или `master`)
2. **Build command**: `cd frontend && npm install && npm run build`
3. **Publish directory**: `frontend/build`
4. В "Environment variables" добавьте:
   - Key: `REACT_APP_BACKEND_URL`
   - Value: `https://ВАШ-APP-NAME.fly.dev`
5. Нажмите "Deploy site"

### 5.3 Настройка домена (опционально)
1. Дождитесь окончания деплоя
2. Вы получите URL вида: `https://random-name-123.netlify.app`
3. Можете изменить название в "Site settings" → "Change site name"

**✅ FRONTEND ГОТОВ!**

---

## 🔧 ЭТАП 6: НАСТРОЙКА TELEGRAM BOT

### 6.1 Создание Web App в Telegram
1. Найдите в Telegram: @BotFather
2. Отправьте команду: `/newapp`
3. Выберите вашего бота (token который у вас есть)
4. Введите название: `AI Trading Signals`
5. Введите описание: `AI торговые сигналы для криптовалют`
6. Отправьте иконку бота (любое изображение)
7. Введите URL вашего Netlify сайта: `https://ваш-сайт.netlify.app`

### 6.2 Получение Web App URL
1. BotFather пришлет вам ссылку на Web App
2. Эта ссылка будет вида: `https://t.me/ваш_бот/app`
3. Именно эту ссылку нужно использовать для доступа к приложению

---

## 🔧 ЭТАП 7: ФИНАЛЬНОЕ ТЕСТИРОВАНИЕ

### 7.1 Тестируем Backend
1. Откройте: `https://ваш-backend.fly.dev/api/health`
2. Должно быть: `{"status": "healthy", "timestamp": "..."}`
3. Откройте: `https://ваш-backend.fly.dev/api/trading-pairs`
4. Должен вернуться список торговых пар

### 7.2 Тестируем Frontend
1. Откройте ваш Netlify сайт
2. Проверьте, что:
   - ✅ Загружается главная страница
   - ✅ Отображается список торговых пар
   - ✅ Работает выбор валютной пары
   - ✅ Показывается рыночная информация
   - ✅ Работает кнопка "Получить AI Сигнал"

### 7.3 Тестируем Telegram Web App
1. Откройте ссылку от BotFather в Telegram
2. Проверьте, что приложение загружается
3. Проверьте все функции в Telegram окружении

---

## 🎉 ГОТОВО! ВАШ TELEGRAM MINI APP РАЗВЕРНУТ!

### 📱 Как пользоваться:
1. **Для пользователей**: Отправьте ссылку `https://t.me/ваш_бот/app`
2. **Для разработки**: Используйте `https://ваш-сайт.netlify.app`

### 🔗 Ваши URL:
- **Backend API**: `https://ваш-backend.fly.dev`
- **Frontend Web**: `https://ваш-сайт.netlify.app`
- **Telegram Mini App**: `https://t.me/ваш_бот/app`

---

## 🛠️ ОБСЛУЖИВАНИЕ И ОБНОВЛЕНИЯ

### Обновление кода:
1. Загрузите новые файлы на GitHub
2. Fly.io и Netlify автоматически развернут изменения
3. Обычно занимает 2-5 минут

### Мониторинг:
1. **Fly.io Dashboard**: Следите за логами backend
2. **Netlify Dashboard**: Следите за логами frontend
3. **Telegram Analytics**: Статистика использования mini app

### Лимиты бесплатных планов:
- **Fly.io**: 160 часов/месяц, 3 приложения
- **Netlify**: 100GB трафика/месяц, 300 минут сборки
- **SQLite**: Без ограничений, но данные хранятся локально

---

## ❓ ЧАСТО ЗАДАВАЕМЫЕ ВОПРОСЫ

**Q: Что если backend не запускается?**
A: Проверьте логи в Fly.io Dashboard. Часто проблема в неправильных переменных окружения.

**Q: Что если frontend не загружается?**
A: Проверьте в Netlify Dashboard, правильно ли указан REACT_APP_BACKEND_URL.

**Q: Потеряются ли данные при перезапуске?**
A: В текущей конфигурации - да, SQLite хранится в контейнере. Для постоянного хранения нужна внешняя база.

**Q: Как добавить свой домен?**
A: В Netlify: Settings → Domain management → Add custom domain

**Q: Как масштабировать приложение?**
A: Fly.io позволяет легко увеличивать ресурсы и количество инстансов в настройках.

---

## 🔒 БЕЗОПАСНОСТЬ

**⚠️ ВАЖНО:**
- Никогда не публикуйте API ключи в открытом коде
- Используйте environment variables для всех секретов
- Регулярно обновляйте зависимости
- Мониторьте использование ресурсов

**Готово! Если что-то не работает, проверьте каждый этап еще раз. Удачи с вашим AI Trading Bot! 🚀**