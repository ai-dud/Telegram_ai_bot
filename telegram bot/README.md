# AI Voice Bot Setup Guide

This guide will help you set up and use the AI Voice Bot with Gemini AI and ElevenLabs on Windows.

## Requirements

1. **Python 3.8 or newer**
   - Download from [Python.org](https://www.python.org/downloads/)
   - Make sure to check "Add Python to PATH" during installation

2. **Git**
   - Download from [Git for Windows](https://git-scm.com/download/win)

## Setup Steps

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd ai-voice-bot
   ```

2. **Create and activate virtual environment**
   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```

3. **Install required packages**
   ```bash
   pip install -r requirements.txt
   ```

4. **Setup API Keys**
   - Create a `.env` file and add the following keys:
     ```
     GOOGLE_API_KEY=your_gemini_api_key
     ELEVENLABS_API_KEY=your_elevenlabs_api_key
     ```
   - Get Gemini API key from: [Google AI Studio](https://makersuite.google.com/app/apikey)
   - Get ElevenLabs API key from: [ElevenLabs](https://elevenlabs.io/)

## Running the Program

1. Activate the virtual environment (if not already activated):
   ```bash
   venv\Scripts\activate
   ```

2. Run the program:
   ```bash
   python ai_voice_bot.py
   ```

## How to Use

1. After starting the program, type your question
2. Press Enter
3. The bot will respond using Gemini AI and generate an audio file using ElevenLabs
4. Audio files are saved in the `output` folder

## Troubleshooting

1. **"Python not found" error**
   - Add Python to PATH or reinstall Python

2. **"pip not found" error**
   - Make sure pip is installed during Python installation

3. **API errors**
   - Ensure your API keys are correct and properly set in the `.env` file
   - For Gemini AI: Check if you're in a supported region
   - For ElevenLabs: Verify your quota limits

4. **Audio not playing**
   - Install a media player like Windows Media Player or VLC

## Notes

- ElevenLabs free tier has a limited monthly quota
- Gemini AI has a generous free tier with limits on queries per minute
- Press `Ctrl+C` to stop the program

## Features

- Text-to-Speech conversion using ElevenLabs
- AI responses powered by Google's Gemini AI
- Automatic audio file generation
- Simple command-line interface

## System Requirements

- Windows 7 or later
- Minimum 4GB RAM
- Internet connection
- At least 500MB free disk space

## Common Issues and Solutions

1. **Slow Response Times**
   - Check your internet connection
   - Ensure you're not exceeding API rate limits

2. **Audio Quality Issues**
   - Check if you have sufficient ElevenLabs credits
   - Try shorter text inputs

3. **Installation Problems**
   - Make sure you have administrator privileges
   - Check if all dependencies are properly installed

## Best Practices

1. Keep your API keys secure
2. Regularly update the dependencies
3. Monitor your API usage
4. Back up important conversations
5. Clean up old audio files regularly

## Support

For any issues:
1. Create an issue in the repository
2. Check the troubleshooting section
3. Contact: [Your Email/Contact]

## Updates

Check the repository regularly for updates and new features. 