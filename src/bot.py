import logging
import os
import random
import tempfile
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
from gtts import gTTS
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class EthiopianEnglishBot:
    def __init__(self):
        # Enhanced vocabulary with categories
        self.vocabularies = {
            'amharic': {
                'name': 'አማርኛ (Amharic)',
                'flag': '🇪🇹',
                'words': [
                    ('hello', 'ሰላም', 'greeting'),
                    ('goodbye', 'ደህና ሁን', 'greeting'),
                    ('thank you', 'አመሰግናለሁ', 'courtesy'),
                    ('water', 'ውሃ', 'daily'),
                    ('food', 'ምግብ', 'daily'),
                    ('house', 'ቤት', 'daily'),
                    ('family', 'ቤተሰብ', 'family'),
                    ('friend', 'ጓደኛ', 'social'),
                    ('work', 'ስራ', 'daily'),
                    ('money', 'ገንዘብ', 'daily'),
                    ('school', 'ትምህርት ቤት', 'education'),
                    ('book', 'መጽሐፍ', 'education'),
                    ('mother', 'እናት', 'family'),
                    ('father', 'አባት', 'family'),
                    ('child', 'ልጅ', 'family'),
                ]
            },
            'tigrinya': {
                'name': 'ትግርኛ (Tigrinya)',
                'flag': '🇪🇹',
                'words': [
                    ('hello', 'ሰላም', 'greeting'),
                    ('goodbye', 'ሰላም ኩን', 'greeting'),
                    ('thank you', 'የቐንየለይ', 'courtesy'),
                    ('water', 'ማይ', 'daily'),
                    ('food', 'መግቢ', 'daily'),
                    ('house', 'ቤት', 'daily'),
                    ('family', 'ቤተሰብ', 'family'),
                    ('friend', 'ዓርኪ', 'social'),
                    ('work', 'ስራሕ', 'daily'),
                    ('money', 'ገንዘብ', 'daily'),
                    ('school', 'ቤት ትምህርቲ', 'education'),
                    ('book', 'መጽሓፍ', 'education'),
                    ('mother', 'ኣደ', 'family'),
                    ('father', 'ኣቦ', 'family'),
                    ('child', 'ቆልዓ', 'family'),
                ]
            },
            'oromo': {
                'name': 'Oromiffa (Oromo)',
                'flag': '🇪🇹',
                'words': [
                    ('hello', 'akkam', 'greeting'),
                    ('goodbye', 'nagaatti', 'greeting'),
                    ('thank you', 'galatoomaa', 'courtesy'),
                    ('water', 'bishaan', 'daily'),
                    ('food', 'nyaata', 'daily'),
                    ('house', 'mana', 'daily'),
                    ('family', 'maatii', 'family'),
                    ('friend', 'hiriyaa', 'social'),
                    ('work', 'hojii', 'daily'),
                    ('money', 'maallaqa', 'daily'),
                    ('school', 'mana barumsaa', 'education'),
                    ('book', 'kitaaba', 'education'),
                    ('mother', 'haadha', 'family'),
                    ('father', 'abbaa', 'family'),
                    ('child', 'ijoollee', 'family'),
                ]
            }
        }
        
    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user = update.effective_user
        if not user or not update.message:
            return
        
        welcome_text = (
            f"🌟 Welcome {user.first_name}! 🌟\n\n"
            "🇪🇹➡️🇺🇸 Ethiopian-English Learning Bot\n\n"
            "✨ Features:\n"
            "📚 Interactive vocabulary learning\n"
            "🎵 Audio pronunciation\n"
            "🏆 Progress tracking\n"
            "🎯 Adaptive difficulty\n\n"
            "Choose your native language:"
        )
        
        keyboard = []
        for lang_key, lang_data in self.vocabularies.items():
            button_text = f"{lang_data['flag']} {lang_data['name']}"
            keyboard.append([InlineKeyboardButton(button_text, callback_data=f"lang_{lang_key}")])
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text(welcome_text, reply_markup=reply_markup)
    
    async def button_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        query = update.callback_query
        await query.answer()
        
        try:
            if query.data.startswith("lang_"):
                await self.set_language(query, context)
            elif query.data == "start_learning":
                await self.start_quiz(query, context)
            elif query.data == "hear_pronunciation":
                await self.send_pronunciation(query, context)
            elif query.data.startswith("answer_"):
                await self.check_answer(query, context)
            elif query.data == "next_question":
                await self.start_quiz(query, context)
            elif query.data == "view_progress":
                await self.show_progress(query, context)
            elif query.data == "main_menu":
                await self.show_main_menu(query, context)
        except Exception as e:
            logger.error(f"Button handler error: {e}")
            await query.edit_message_text(f"❌ Error: {str(e)}")
    
    async def set_language(self, query, context):
        language_key = query.data.replace("lang_", "")
        lang_data = self.vocabularies[language_key]
        
        context.user_data['native_language'] = language_key
        context.user_data['score'] = 0
        context.user_data['total'] = 0
        context.user_data['streak'] = 0
        
        confirmation_text = (
            f"🎉 Excellent choice!\n\n"
            f"{lang_data['flag']} You selected: {lang_data['name']}\n\n"
            f"📖 Vocabulary loaded: {len(lang_data['words'])} words\n"
            f"🎯 Ready to master English!\n\n"
            f"Let's begin your learning journey! 🚀"
        )
        
        keyboard = [
            [InlineKeyboardButton("📚 Start Learning", callback_data="start_learning")],
            [InlineKeyboardButton("📊 View Progress", callback_data="view_progress")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(confirmation_text, reply_markup=reply_markup)
    
    async def start_quiz(self, query, context):
        try:
            native_lang = context.user_data.get('native_language', 'amharic')
            lang_data = self.vocabularies[native_lang]
            words = lang_data['words']
            
            correct_word = random.choice(words)
            context.user_data['current_answer'] = correct_word[0]
            context.user_data['current_native'] = correct_word[1]
            context.user_data['current_category'] = correct_word[2]
            
            other_words = [w for w in words if w != correct_word]
            wrong_answers = random.sample(other_words, min(2, len(other_words)))
            
            options = [correct_word[0]] + [w[0] for w in wrong_answers]
            random.shuffle(options)
            
            score = context.user_data.get('score', 0)
            total = context.user_data.get('total', 0)
            streak = context.user_data.get('streak', 0)
            
            category_emoji = {
                'greeting': '👋', 'courtesy': '🙏', 'daily': '🏠',
                'family': '👨‍👩‍👧‍👦', 'social': '👥', 'education': '🎓'
            }
            
            quiz_text = (
                f"🎯 Quiz Time!\n\n"
                f"📊 Score: {score}/{total} | 🔥 Streak: {streak}\n"
                f"{category_emoji.get(correct_word[2], '📝')} Category: {correct_word[2].title()}\n\n"
                f"❓ What is the English translation of:\n\n"
                f"🇪🇹 '{correct_word[1]}' ?"
            )
            
            keyboard = []
            for option in options:
                keyboard.append([InlineKeyboardButton(f"🔤 {option}", callback_data=f"answer_{option}")])
            
            keyboard.append([InlineKeyboardButton("🔊 Hear Pronunciation", callback_data="hear_pronunciation")])
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            await query.edit_message_text(quiz_text, reply_markup=reply_markup)
            
        except Exception as e:
            logger.error(f"Quiz error: {e}")
            await query.edit_message_text(f"❌ Quiz error: {str(e)}")
    
    async def send_pronunciation(self, query, context):
        try:
            english_word = context.user_data.get('current_answer')
            if not english_word:
                await query.answer("No word to pronounce!")
                return
            
            await query.answer("🎵 Generating pronunciation...")
            
            tts = gTTS(text=english_word, lang='en', slow=False)
            
            with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as tmp_file:
                temp_path = tmp_file.name
                
            tts.save(temp_path)
            
            with open(temp_path, 'rb') as audio_file:
                await query.message.reply_voice(
                    voice=audio_file,
                    caption=f"🔊 Pronunciation: '{english_word}'"
                )
            
            os.unlink(temp_path)
            
        except Exception as e:
            logger.error(f"Pronunciation error: {e}")
            await query.answer(f"❌ Audio error: {str(e)}")
    
    async def check_answer(self, query, context):
        try:
            user_answer = query.data.replace("answer_", "")
            correct_answer = context.user_data.get('current_answer')
            native_word = context.user_data.get('current_native')
            
            context.user_data['total'] = context.user_data.get('total', 0) + 1
            
            if user_answer == correct_answer:
                context.user_data['score'] = context.user_data.get('score', 0) + 1
                context.user_data['streak'] = context.user_data.get('streak', 0) + 1
                
                encouragements = [
                    "🎉 Excellent!", "✨ Perfect!", "🌟 Amazing!", 
                    "🏆 Outstanding!", "💫 Brilliant!", "🎯 Spot on!"
                ]
                result = f"{random.choice(encouragements)} Correct!"
                
                streak = context.user_data.get('streak', 0)
                if streak >= 5:
                    result += f"\n🔥 {streak} in a row! You're on fire!"
                elif streak >= 3:
                    result += f"\n⚡ {streak} streak! Keep going!"
                    
            else:
                context.user_data['streak'] = 0
                result = f"❌ Not quite!\n\n✅ Correct answer: '{correct_answer}'\n🇪🇹 Native word: '{native_word}'"
            
            score = context.user_data.get('score', 0)
            total = context.user_data.get('total', 0)
            accuracy = (score / total * 100) if total > 0 else 0
            
            result_text = (
                f"{result}\n\n"
                f"📊 Current Score: {score}/{total} ({accuracy:.1f}%)\n"
                f"🎯 Keep practicing to improve!"
            )
            
            keyboard = [
                [InlineKeyboardButton("➡️ Next Question", callback_data="next_question")],
                [InlineKeyboardButton("🔊 Hear Correct Answer", callback_data="hear_pronunciation")],
                [InlineKeyboardButton("📊 View Progress", callback_data="view_progress")],
                [InlineKeyboardButton("🏠 Main Menu", callback_data="main_menu")]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            await query.edit_message_text(result_text, reply_markup=reply_markup)
            
        except Exception as e:
            logger.error(f"Answer check error: {e}")
            await query.edit_message_text(f"❌ Answer error: {str(e)}")
    
    async def show_progress(self, query, context):
        score = context.user_data.get('score', 0)
        total = context.user_data.get('total', 0)
        streak = context.user_data.get('streak', 0)
        native_lang = context.user_data.get('native_language', 'amharic')
        
        if total == 0:
            progress_text = (
                "📊 Your Learning Progress\n\n"
                "🎯 No questions answered yet!\n"
                "Start learning to see your progress."
            )
        else:
            accuracy = (score / total * 100)
            lang_data = self.vocabularies[native_lang]
            
            if accuracy >= 90:
                level = "🏆 Master"
                level_emoji = "🌟"
            elif accuracy >= 75:
                level = "🥇 Expert"
                level_emoji = "⭐"
            elif accuracy >= 60:
                level = "🥈 Advanced"
                level_emoji = "✨"
            elif accuracy >= 40:
                level = "🥉 Intermediate"
                level_emoji = "💫"
            else:
                level = "📚 Beginner"
                level_emoji = "🌱"
            
            progress_text = (
                f"📊 Your Learning Progress\n\n"
                f"{lang_data['flag']} Language: {lang_data['name']}\n"
                f"{level_emoji} Level: {level}\n\n"
                f"✅ Correct Answers: {score}\n"
                f"📝 Total Questions: {total}\n"
                f"🎯 Accuracy: {accuracy:.1f}%\n"
                f"🔥 Current Streak: {streak}\n\n"
                f"🎓 Keep practicing to reach Master level!"
            )
        
        keyboard = [
            [InlineKeyboardButton("📚 Continue Learning", callback_data="start_learning")],
            [InlineKeyboardButton("🏠 Main Menu", callback_data="main_menu")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(progress_text, reply_markup=reply_markup)
    
    async def show_main_menu(self, query, context):
        native_lang = context.user_data.get('native_language')
        if not native_lang:
            await query.edit_message_text("Please start with /start to select your language.")
            return
        
        lang_data = self.vocabularies[native_lang]
        score = context.user_data.get('score', 0)
        total = context.user_data.get('total', 0)
        
        menu_text = (
            f"🏠 Main Menu\n\n"
            f"{lang_data['flag']} Learning: {lang_data['name']} → English\n"
            f"📊 Progress: {score}/{total}\n\n"
            f"Choose an option:"
        )
        
        keyboard = [
            [InlineKeyboardButton("📚 Start Learning", callback_data="start_learning")],
            [InlineKeyboardButton("📊 View Progress", callback_data="view_progress")],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(menu_text, reply_markup=reply_markup)

def main():
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    if not token:
        print("Error: TELEGRAM_BOT_TOKEN not found in .env file")
        return
    
    application = Application.builder().token(token).build()
    bot = EthiopianEnglishBot()
    
    application.add_handler(CommandHandler("start", bot.start))
    application.add_handler(CallbackQueryHandler(bot.button_handler))
    
    print("Ethiopian-English Learning Bot is running!")
    print("Features: Audio pronunciation, Progress tracking, Beautiful UI")
    print("Send /start to your bot on Telegram")
    application.run_polling()

if __name__ == '__main__':
    main()