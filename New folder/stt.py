import os
import discord
from discord.ext import commands
import speech_recognition as sr
from pydub import AudioSegment
import tempfile
import time

# Add your Discord bot token here
TOKEN = "MTMzNTk4ODk4NDY1NjAzOTk2Ng.GO9Zzy.to3Y7oigzmorDfXakjXg3DgOmmfooKiJTaD25o"

# Set up bot
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Bot is ready!')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    # Check if message has an audio attachment
    if message.attachments:
        for attachment in message.attachments:
            if attachment.filename.endswith(('.mp3', '.wav', '.ogg', '.oga')) or 'octet-stream.oga' in attachment.filename:
                temp_audio = None
                temp_wav = None
                try:
                    # Create unique filenames
                    timestamp = str(int(time.time()))
                    temp_audio_path = f"temp_audio_{timestamp}.oga"
                    temp_wav_path = f"temp_wav_{timestamp}.wav"
                    
                    # Download and save the audio file
                    await attachment.save(temp_audio_path)
                    
                    # Convert to WAV
                    audio = AudioSegment.from_file(temp_audio_path, format="ogg")
                    audio.export(temp_wav_path, format="wav")
                    
                    # Convert to text
                    recognizer = sr.Recognizer()
                    with sr.AudioFile(temp_wav_path) as source:
                        audio_data = recognizer.record(source)
                        text = recognizer.recognize_google(audio_data, language='en-US')
                        await message.channel.send(text)

                except Exception as e:
                    await message.channel.send(f"Error: {str(e)}")
                
                finally:
                    # Clean up temporary files
                    try:
                        if os.path.exists(temp_audio_path):
                            os.remove(temp_audio_path)
                        if os.path.exists(temp_wav_path):
                            os.remove(temp_wav_path)
                    except Exception:
                        pass

bot.run(TOKEN) 