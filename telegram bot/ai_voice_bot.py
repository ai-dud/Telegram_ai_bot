import os
import tempfile
import time
from datetime import datetime
import speech_recognition as sr
from pydub import AudioSegment
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters
import google.generativeai as genai
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
ELEVENLABS_API_KEY = os.getenv('ELEVENLABS_API_KEY')

# Initialize Gemini AI
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-pro')

# Create temp directory
TEMP_DIR = "temp"
if not os.path.exists(TEMP_DIR):
    os.makedirs(TEMP_DIR)

async def start(update: Update, context):
    welcome_message = """
🤖 *AI Voice Bot में आपका स्वागत है!*
मुझे कोई भी सवाल पूछें, मैं हिंदी में जवाब दूंगा।
    """
    await update.message.reply_text(welcome_message, parse_mode='Markdown')

async def generate_hindi_response(text):
    try:
        prompt = f"""
        आप एक बहुत ही कुशल और मज़ेदार AI सहायक हैं। यूज़र के सवाल का जवाब इन निर्देशों के अनुसार दें:

        1. जवाब की विशेषताएं:
           - बिल्कुल सटीक और तथ्यात्मक जानकारी दें
           - सरल और रोचक भाषा का प्रयोग करें
           - हर जवाब में एक मज़ेदार टिप्पणी या उदाहरण जोड़ें
           - जवाब को संक्षिप्त लेकिन पूर्ण रखें (40-50 शब्द)

        2. जवाब का प्रारूप:
           - पहले मुख्य जानकारी दें
           - फिर एक मज़ेदार टिप्पणी या उदाहरण
           - अंत में एक छोटी सी सलाह या निष्कर्ष

        3. विशेष ध्यान:
           - हर जवाब 100% सटीक होना चाहिए
           - जवाब हिंदी में ही दें
           - जटिल विषयों को भी सरल बनाकर समझाएं
           - यदि कोई बात स्पष्ट नहीं है, तो स्पष्टीकरण मांगें

        उदाहरण जवाब:
        "सूर्य से पृथ्वी की दूरी 15 करोड़ किलोमीटर है। इतनी दूरी तो मेरे पड़ोसी की चाय की दुकान से भी ज्यादा है! 😄 लेकिन यही दूरी हमारे लिए एकदम सही है।"

        यूज़र का प्रश्न/संदेश: "{text}"
        """
        
        # Generate response with optimized parameters
        response = model.generate_content(prompt, generation_config={
            'temperature': 0.6,  # Balance between creativity and accuracy
            'top_p': 0.95,
            'top_k': 40,
            'max_output_tokens': 250,
            'candidate_count': 1,
        })
        
        # Clean and format response
        response_text = response.text.strip()
        
        # Remove any English/Roman text if present, but keep emojis
        hindi_only = ''.join(char for char in response_text 
                           if ord(char) > 127 
                           or char in [' ', '।', '?', '!', ',', '.', '-', '\n', '😄', '😊', '😃', '😅', '🌟', '💡', '✨'])
        
        # If no Hindi text was generated
        if not hindi_only.strip():
            return "अरे वाह! आपका सवाल बड़ा दिलचस्प है। कृपया इसे थोड़ा और स्पष्ट करें, ताकि मैं बेहतर जवाब दे सकूं। 😊"
            
        return hindi_only.strip()

    except Exception as e:
        print(f"AI Error: {e}")
        return "ओह! मेरे दिमाग में थोड़ी खराबी आ गई है। कृपया थोड़ी देर बाद फिर से पूछें। तब तक एक चाय का आनंद लें! 😄"

async def generate_audio(text, output_path):
    try:
        url = f"https://api.elevenlabs.io/v1/text-to-speech/oPM3trUCF4e0vTcsrMQr"
        headers = {
            'Accept': 'audio/mpeg',
            'Content-Type': 'application/json',
            'xi-api-key': ELEVENLABS_API_KEY
        }
        data = {
            'text': text,
            'model_id': 'eleven_multilingual_v2',
            'voice_settings': {
                'stability': 0.8,
                'similarity_boost': 0.8,
                'style': 0.7,
                'use_speaker_boost': True
            }
        }
        
        response = requests.post(url, headers=headers, json=data)
        if response.status_code == 200:
            with open(output_path, 'wb') as f:
                f.write(response.content)
            return True
        else:
            print(f"ElevenLabs API Error: {response.text}")
            return False
    except Exception as e:
        print(f"Audio generation error: {e}")
        return False

async def convert_voice_to_text(file_path):
    try:
        # Convert to WAV with better quality
        audio = AudioSegment.from_ogg(file_path)
        audio = audio.set_channels(1)  # Convert to mono
        audio = audio.set_frame_rate(16000)  # Set sample rate
        wav_path = file_path.replace('.ogg', '.wav')
        audio.export(wav_path, format="wav", parameters=["-q:a", "0"])

        # Initialize recognizer with noise handling
        recognizer = sr.Recognizer()
        recognizer.dynamic_energy_threshold = True
        recognizer.energy_threshold = 300
        
        # Convert speech to text with better accuracy
        with sr.AudioFile(wav_path) as source:
            # Adjust for ambient noise
            recognizer.adjust_for_ambient_noise(source)
            audio_data = recognizer.record(source)
            
            # Try multiple language models for better accuracy
            try:
                text = recognizer.recognize_google(audio_data, language='hi-IN')
            except:
                # Fallback to English if Hindi fails (for mixed language)
                text = recognizer.recognize_google(audio_data, language='en-IN')
            
        # Clean up
        os.remove(wav_path)
        
        return {'success': True, 'text': text}
    except Exception as e:
        print(f"Voice processing error: {e}")
        return {
            'success': False,
            'text': "आपकी आवाज़ स्पष्ट नहीं है। कृपया धीरे और स्पष्ट रूप से बोलें या अपना प्रश्न टेक्स्ट के रूप में लिखें।"
        }

async def handle_message(update: Update, context):
    try:
        chat_id = update.message.chat_id
        
        if update.message.voice:
            # Send processing message
            processing_msg = await update.message.reply_text("🎙️ आवाज़ को समझ रहा हूं...")
            
            # Download voice message
            voice = await update.message.voice.get_file()
            voice_path = os.path.join(TEMP_DIR, f"voice_{int(time.time())}.ogg")
            await voice.download_to_drive(voice_path)
            
            # Convert voice to text
            voice_result = await convert_voice_to_text(voice_path)
            os.remove(voice_path)
            
            # Delete processing message
            await processing_msg.delete()
            
            if not voice_result['success']:
                error_audio_path = os.path.join(TEMP_DIR, f"error_{int(time.time())}.mp3")
                gen_msg = await update.message.reply_text("🔊 आवाज़ तैयार कर रहा हूं...")
                await generate_audio(voice_result['text'], error_audio_path)
                with open(error_audio_path, 'rb') as audio:
                    await update.message.reply_voice(audio)
                os.remove(error_audio_path)
                await gen_msg.delete()
                return
                
            user_text = voice_result['text']
        elif update.message.text and not update.message.text.startswith('/'):
            user_text = update.message.text
            print(f"Received text message: {user_text}")  # Debug log
        else:
            return

        # Show AI thinking message
        thinking_msg = await update.message.reply_text("🤔 आपके सवाल का जवाब तैयार कर रहा हूं...")
        
        # Get AI response
        print(f"Sending to AI: {user_text}")  # Debug log
        ai_text = await generate_hindi_response(user_text)
        print(f"AI Response: {ai_text}")  # Debug log
        
        # Show generating audio message
        gen_msg = await update.message.reply_text("🔊 आवाज़ तैयार कर रहा हूं...")
        
        # Delete thinking message
        await thinking_msg.delete()
        
        # Generate audio response
        audio_path = os.path.join(TEMP_DIR, f"response_{int(time.time())}.mp3")
        audio_generated = await generate_audio(ai_text, audio_path)
        
        # Delete generating message
        await gen_msg.delete()
        
        # Send only voice response
        if audio_generated:
            with open(audio_path, 'rb') as audio:
                await update.message.reply_voice(audio)
            os.remove(audio_path)
        else:
            error_msg = "माफ़ कीजिये, आवाज़ बनाने में समस्या आई है।"
            error_audio_path = os.path.join(TEMP_DIR, f"error_{int(time.time())}.mp3")
            gen_error_msg = await update.message.reply_text("🔊 त्रुटि संदेश तैयार कर रहा हूं...")
            await generate_audio(error_msg, error_audio_path)
            with open(error_audio_path, 'rb') as audio:
                await update.message.reply_voice(audio)
            os.remove(error_audio_path)
            await gen_error_msg.delete()

    except Exception as e:
        print(f"Error: {e}")
        error_msg = "कुछ तकनीकी समस्या आई है। कृपया फिर से कोशिश करें।"
        error_audio_path = os.path.join(TEMP_DIR, f"error_{int(time.time())}.mp3")
        gen_error_msg = await update.message.reply_text("🔊 त्रुटि संदेश तैयार कर रहा हूं...")
        await generate_audio(error_msg, error_audio_path)
        with open(error_audio_path, 'rb') as audio:
            await update.message.reply_voice(audio)
        os.remove(error_audio_path)
        await gen_error_msg.delete()

def main():
    # Create the Application
    application = Application.builder().token(TELEGRAM_TOKEN).build()
    
    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT | filters.VOICE, handle_message))
    
    # Start the bot
    print("Bot is running...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main() 