ven laps import discord
from discord.ext import commands
from elevenlabs import Voice
from elevenlabs.client import ElevenLabs
import os
import tempfile
import logging
import asyncio
import sys

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# API Keys
ELEVEN_LABS_API_KEY = "you token"
DISCORD_TOKEN = "your discord token "
N8N_CHANNEL_ID = "1333736717093703680"  # n8n channel ID
os.environ["ELEVEN_API_KEY"] = ELEVEN_LABS_API_KEY

# Initialize ElevenLabs client
eleven = ElevenLabs(api_key=ELEVEN_LABS_API_KEY)

# Voice settings
VOICE_ID = "oPM3trUCF4e0vTcsrMQr"  # Mahesh voice ID
MODEL_ID = "eleven_multilingual_v2"  # Using multilingual model for better support

# Discord Intents setup
intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.messages = True

# Discord Bot setup
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    logger.info(f'Successfully logged in as {bot.user} (ID: {bot.user.id})')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    try:
        # Generate TTS audio using elevenlabs with Mahesh voice
        audio_generator = eleven.text_to_speech.convert(
            text=message.content,
            voice_id=VOICE_ID,
            model_id=MODEL_ID
        )

        # Save the audio to a temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as tmp_file:
            # Write all audio chunks to the file
            for chunk in audio_generator:
                if isinstance(chunk, bytes):
                    tmp_file.write(chunk)
            tmp_file_path = tmp_file.name

        # Send the audio file back to the same channel where message was received
        await message.channel.send(file=discord.File(tmp_file_path))
        
        await message.add_reaction('✅')

    except Exception as e:
        logger.error(f"Error processing message: {e}", exc_info=True)
        await message.add_reaction('❌')
    
    finally:
        if 'tmp_file_path' in locals():
            try:
                os.remove(tmp_file_path)
            except Exception as e:
                logger.error(f"Error removing temporary file: {e}")

async def main():
    try:
        logger.info("Starting bot...")
        await bot.start(DISCORD_TOKEN)
    except Exception as e:
        logger.error(f"Error starting bot: {e}", exc_info=True)
    finally:
        await bot.close()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Bot stopped by user")
    except Exception as e:
        logger.error(f"Fatal error: {e}", exc_info=True)
