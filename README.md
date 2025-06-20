# Ethiopian-English Learning Bot 🇪🇹➡️🇺🇸

An intelligent Telegram bot that helps Ethiopian speakers learn English through interactive vocabulary exercises and audio pronunciation.

## Features

### 🌍 Multi-Language Support
- **አማርኛ (Amharic)** - Most widely spoken Ethiopian language
- **ትግርኛ (Tigrinya)** - Spoken in northern Ethiopia and Eritrea  
- **Oromiffa (Oromo)** - Largest ethnic group in Ethiopia

### 🎤 Audio Integration
- **Text-to-Speech** - Get correct English pronunciation audio
- **Interactive Learning** - Audio feedback for every word
- **Pronunciation Practice** - Hear words as many times as needed

### 🎯 Smart Learning Features
- **Progress Tracking** - Monitor your learning journey
- **Streak Counter** - Build learning momentum
- **Difficulty Levels** - From Beginner to Master
- **Category-based Learning** - Greetings, Family, Daily Life, Education

### 📚 Rich Vocabulary
- **Essential Words** - Core vocabulary for daily communication
- **Cultural Context** - Words relevant to Ethiopian learners
- **Multiple Categories** - Organized learning by topic
- **Adaptive Exercises** - Questions adapt to your progress

## Quick Start

### 1. Setup
```bash
# Clone the repository
git clone https://github.com/yourusername/ethiopian-english-bot.git
cd ethiopian-english-bot

# Install dependencies
pip install -r requirements.txt

# Create environment file
cp .env.example .env
# Edit .env and add your bot token
```

### 2. Get Bot Token
1. Message [@BotFather](https://t.me/BotFather) on Telegram
2. Send `/newbot`
3. Follow instructions to create your bot
4. Copy the token to your `.env` file

### 3. Run the Bot
```bash
python src/bot.py
```

### 4. Start Learning
1. Find your bot on Telegram
2. Send `/start`
3. Choose your native language
4. Begin learning English!

## How It Works

### Language Selection
Choose from three major Ethiopian languages:
- 🇪🇹 **አማርኛ (Amharic)** - 25M+ speakers
- 🇪🇹 **ትግርኛ (Tigrinya)** - 7M+ speakers  
- 🇪🇹 **Oromiffa (Oromo)** - 35M+ speakers

### Learning Process
1. **Quiz Questions** - Multiple choice format
2. **Audio Pronunciation** - Hear correct English pronunciation
3. **Instant Feedback** - Know immediately if you're correct
4. **Progress Tracking** - See your improvement over time
5. **Streak Building** - Maintain learning momentum

### Vocabulary Categories
- **👋 Greetings** - Hello, goodbye, thank you
- **🙏 Courtesy** - Please, excuse me, sorry
- **🏠 Daily Life** - Water, food, house, work
- **👨‍👩‍👧‍👦 Family** - Mother, father, child, family
- **👥 Social** - Friend, neighbor, community
- **🎓 Education** - School, book, learning

## Example Usage

```
Bot: 🌟 Welcome! Choose your native language:
User: [Selects አማርኛ (Amharic)]

Bot: 🎯 Quiz Time!
     📊 Score: 0/0 | 🔥 Streak: 0
     👋 Category: Greeting
     
     ❓ What is the English translation of:
     🇪🇹 'ሰላም' ?
     
     🔤 Hello    🔤 Water    🔤 Food
     🔊 Hear Pronunciation

User: [Selects Hello]
Bot: 🎉 Excellent! Correct!
     📊 Current Score: 1/1 (100.0%)
```

## Technical Details

### Dependencies
- **python-telegram-bot** - Telegram Bot API wrapper
- **gTTS** - Google Text-to-Speech for audio
- **python-dotenv** - Environment variable management

### Architecture
- **Single File Design** - Easy to understand and modify
- **In-Memory Storage** - No database required
- **Event-Driven** - Responds to user interactions
- **Error Handling** - Graceful error recovery

### Supported Platforms
- **Windows** - Full support
- **macOS** - Full support  
- **Linux** - Full support
- **Cloud Deployment** - Heroku, Railway, etc.

## Customization

### Adding New Languages
```python
'new_language': {
    'name': 'Language Name',
    'flag': '🏳️',
    'words': [
        ('english_word', 'native_translation', 'category'),
        # Add more words...
    ]
}
```

### Adding Vocabulary
```python
('english_word', 'native_translation', 'category')
```

### Categories
- `greeting` - Basic greetings
- `courtesy` - Polite expressions
- `daily` - Daily life items
- `family` - Family members
- `social` - Social interactions
- `education` - Learning related

## Deployment

### Local Development
```bash
python src/bot.py
```

### Cloud Deployment (Heroku)
```bash
# Create Procfile
echo "worker: python src/bot.py" > Procfile

# Deploy to Heroku
heroku create your-bot-name
heroku config:set TELEGRAM_BOT_TOKEN=your_token
git push heroku main
```

### Docker
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY src/ ./src/
CMD ["python", "src/bot.py"]
```

## Contributing

### Ways to Contribute
1. **Add Vocabulary** - Expand word lists
2. **New Languages** - Add more Ethiopian languages
3. **Features** - Enhance learning experience
4. **Bug Fixes** - Report and fix issues
5. **Documentation** - Improve guides

### Development Setup
```bash
git clone https://github.com/yourusername/ethiopian-english-bot.git
cd ethiopian-english-bot
pip install -r requirements.txt
# Make your changes
# Test thoroughly
# Submit pull request
```

## Troubleshooting

### Common Issues

**Bot not responding:**
- Check bot token in `.env` file
- Ensure bot is running (`python src/bot.py`)
- Verify internet connection

**Audio not working:**
- Check internet connection (gTTS requires online access)
- Try restarting the bot
- Ensure gTTS dependency is installed

**Import errors:**
- Run `pip install -r requirements.txt`
- Check Python version (3.7+ required)
- Verify all files are in correct directories

### Getting Help
1. Check this README
2. Review error messages in terminal
3. Test with simple `/start` command
4. Create GitHub issue with details

## License

MIT License - Feel free to use, modify, and distribute!

## Acknowledgments

- **Ethiopian Community** - For inspiration and cultural input
- **Telegram Bot API** - For excellent bot platform
- **Google TTS** - For audio pronunciation
- **Python Community** - For amazing libraries

---

**Happy Learning! 🎓 Learn English, Keep Your Culture! 🇪🇹**

*Made with ❤️ for the Ethiopian diaspora community*