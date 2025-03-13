# EXMACHINA Twitter Bot

This is a fork of the original [voyager_alpha](https://github.com/aivoyager/puti) project, modified to create an AI-powered Twitter bot.

<h1 align="center"><strong>EXMACHINA Twitter Bot</strong></h1>
<p align="center" style="color: aqua"><b>AI-powered Twitter automation</b></p>

<p align="center">
    <a href="./README.md">
        <img src="https://img.shields.io/badge/document-English-blue.svg" alt="EN doc">
    </a>
    <a href="https://opensource.org/licenses/MIT">
        <img src="https://img.shields.io/badge/License-MIT-blue.svg" alt="License: MIT">
    </a>
    <a href="./CHANGELOG.md">
        <img src="https://img.shields.io/badge/CHANGELOG-История-blue.svg" alt="Changelog">
    </a>
</p>


<p align="center">
    <!-- Project Stats -->
    <a href="https://github.com/yourusername/exmachina/issues">
        <img src="https://img.shields.io/github/issues/yourusername/exmachina" alt="GitHub issues">
    </a>
    <a href="https://github.com/yourusername/exmachina/network">
        <img src="https://img.shields.io/github/forks/yourusername/exmachina" alt="GitHub forks">
    </a>
    <a href="https://github.com/yourusername/exmachina/stargazers">
        <img src="https://img.shields.io/github/stars/yourusername/exmachina" alt="GitHub stars">
    </a>
    <a href="https://star-history.com/#aivoyager/puti">
        <img src="https://img.shields.io/github/stars/aivoyager/puti?style=social" alt="GitHub star chart">
    </a>
</p>

## About

EXMACHINA is a fork of the [voyager_alpha](https://github.com/aivoyager/puti) project, which was originally designed as a multi-agent system. This fork has been modified to create a specialized Twitter bot that uses GPT-4 for content generation and management.

### Key Differences from Original Project
- Focused on Twitter-specific functionality
- Added web interface for bot management
- Implemented test mode for safe testing
- Added tweet scheduling system
- Enhanced with Twitter-specific features

## Описание

EXMACHINA - это интеллектуальный Twitter бот, использующий GPT-4 для генерации и публикации твитов. Бот может работать как в тестовом, так и в боевом режиме, имеет настраиваемое расписание публикаций и поддерживает взаимодействие с упоминаниями.

## Возможности

- 🤖 Генерация твитов с помощью GPT-4
- ⏰ Настраиваемое расписание публикаций
- 🔄 Автоматическая обработка упоминаний
- 🎭 Настраиваемая личность бота
- 🧪 Тестовый режим для безопасного тестирования
- 📊 Веб-интерфейс для управления
- 📝 История твитов и статистика

## Установка

1. Клонируйте репозиторий:
```bash
git clone https://github.com/yourusername/exmachina.git
cd exmachina
```

2. Создайте виртуальное окружение и активируйте его:
```bash
python -m venv venv
source venv/bin/activate  # для Linux/Mac
venv\Scripts\activate     # для Windows
```

3. Установите зависимости:
```bash
pip install -r requirements.txt
```

4. Создайте файл `.env` на основе `.env.example`:
```bash
cp .env.example .env
```

5. Настройте переменные окружения в файле `.env`

## Конфигурация

### Основные настройки в `.env`:
```env
OPENAI_API_KEY=your_openai_api_key_here
TWITTER_BEARER_TOKEN=your_twitter_bearer_token_here
TEST_MODE=true
```

### Настройка личности бота:
```yaml
# conf/config.yaml
agent:
  name: "EXMACHINA"
  bio: "AI-powered Twitter bot"
  traits:
    - "friendly"
    - "professional"
  interests:
    - "AI"
    - "Technology"
  tone: "professional"
  use_emojis: true
  use_hashtags: true
```

## Использование

1. Запустите сервер:
```bash
python main.py
```

2. Откройте веб-интерфейс:
```
http://localhost:8000
```

3. Настройте параметры бота через веб-интерфейс

## Тестовый режим

В тестовом режиме (`TEST_MODE=true`):
- Твиты сохраняются локально
- Не происходит реальных публикаций
- Можно безопасно тестировать функциональность

## Разработка

### Структура проекта:
```
exmachina/
├── agent/           # Логика агента
├── api/            # API эндпоинты
├── client/         # Клиенты для внешних сервисов
├── conf/           # Конфигурационные файлы
├── core/           # Основные компоненты
├── models/         # Модели данных
├── static/         # Статические файлы
├── templates/      # HTML шаблоны
└── utils/          # Вспомогательные функции
```

## Лицензия

MIT License - см. файл [LICENSE](LICENSE) для подробностей.

## Вклад в проект

1. Форкните репозиторий
2. Создайте ветку для вашей функции (`git checkout -b feature/amazing-feature`)
3. Зафиксируйте изменения (`git commit -m 'Add some amazing feature'`)
4. Отправьте изменения в ветку (`git push origin feature/amazing-feature`)
5. Откройте Pull Request
