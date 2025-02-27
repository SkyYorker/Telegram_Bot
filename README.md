# Telegram Quiz Bot

Этот проект представляет собой Telegram-бота, который позволяет пользователям участвовать в викторинах. Бот задает вопросы с несколькими вариантами ответов и предоставляет обратную связь по ответам пользователя.

## Структура проекта

```
Telegram_Bot
├── bot
│   ├── handlers.py
│   ├── keyboards.py
│   ├── quiz.py
│   └── utils.py
├── data
│   └── quiz_data.py
├── run_bot.py
├── requirements.txt
└── README.md
```

## Описание файлов


- **bot/handlers.py**: Содержит обработчики callback-запросов для бота, включая функции, которые обрабатывают ответы пользователей на вопросы викторины.

- **bot/keyboards.py**: Определяет макеты клавиатур для бота, включая inline-клавиатуру для вариантов ответов викторины.

- **bot/quiz.py**: Управляет логикой викторины, включая получение вопросов и обновление прогресса пользователя в викторине.

- **bot/utils.py**: Содержит вспомогательные функции, которые используются по всему боту.

- **data/quiz_data.py**: Содержит структуру данных викторины, включая вопросы, варианты ответов и правильные ответы.

- **run_bot.py**: Точка входа в приложение, которая инициализирует бота, настраивает базу данных и начинает опрос обновлений.

- **requirements.txt**: Список зависимостей, необходимых для проекта, таких как `aiogram` и `aiosqlite`.

## Инструкции по установке

1. Клонируйте репозиторий:
   ```
   git clone https://github.com/SkyYorker/Telegram_Bot
   ```

2. Перейдите в директорию проекта:
   ```
   cd Telegram_Bot
   ```

3. Установите необходимые зависимости:
   ```
   pip install -r requirements.txt
   ```

4. Замените `YOUR_BOT_TOKEN` в `run_bot.py` на ваш фактический токен Telegram-бота, полученный от BotFather.

5. Запустите бота:
   ```
   python run_bot.py
   ```

## Использование

- Запустите бота, отправив команду `/start`.
- Следуйте подсказкам, чтобы участвовать в викторине.

## Команды бота

- Запускает бота `/start`
- Запускает викторину`/quiz`
- Показывает статистику игрока `/stat`
- Сбрасывает статистику игрока `/cleanstat`
