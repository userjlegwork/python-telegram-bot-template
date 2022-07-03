# python-telegram-bot-template

Basic Python template for Telegram bot

Setup bot:

- Create bot with BotFather and request token
- Add TOKEN enviroment variable (by .env file or directly to system enviroment variables)

Setup database (testing):

- Log in to postgres using user `postgres`
- Create postgres database named `testbot`
- Change user password to `postgres`

Note: For other values different from default ones use a .env file at the project root or declare the enviroment variables within the Operative System. Variable names are `POSTGRES_HOST, POSTGRES_DB, POSTGRES_USER, POSTGRES_PASSWORD`.
