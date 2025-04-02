🎬 Telegram Bot for Movie and Book Recommendations

Looking for your next favorite movie or book? This bot provides personalized recommendations based on your preferences!
With this bot, you can get tailored suggestions for movies and books, making it easier to find something great to watch or read next.

✅ What does it do?

 • 🎥 Suggests movies based on your genre preferences
 • 📚 Recommends books that match your interests
 • 💡 Offers detailed descriptions, ratings, and links to find more information
 • 🗣️ Allows for feedback on recommendations to improve future suggestions

🔧 Features

✅ Personalizes recommendations based on your preferences
✅ Offers both movie and book suggestions in a single bot
✅ Provides quick links to find and explore your recommendations

📩 Need help finding your next movie or book?

Contact me on Telegram, and I’ll set up this bot to suggest the perfect next watch or read for you! 🚀

# Instructions for installing and launching a Telegram bot for recommending movies and books

This guide will help you install and run the bot even if you have never worked with programming before.

## What needs to be prepared before installation:

1. **Telegram Bot token** - obtained from [@BotFather](https://t.me/BotFather ) in the Telegram
2. **TMDb API key** - to get information about movies
3. **Google Books API key** - to get information about books

## Getting the required API keys:

###1. Getting a Telegram Bot Token:
1. Open Telegram and find the bot @BotFather
2. Send him the command `/newbot`
3. Follow the instructions by specifying the bot's name and username (must end with "bot")
4. After creating the bot, you will receive a token like `123456789:ABCDefGhIJKlmnOPQRstUVwxYZ`
5. Save this token - you will need it to set up the bot.

### 2. Getting the TMDb API key:
1. Log in to the website [https://www.themoviedb.org /](https://www.themoviedb.org /)
2. Register or log in to an existing account
3. Go to the "Settings" section in the profile drop-down menu.
4. Select "API" from the menu on the left
5. Follow the instructions to get the API key (Version 3 auth)
6. Save the received key

###3. Getting the Google Books API Key:
1. Go to the [Google Cloud Console] website(https://console.cloud .google.com /)
2. Create a new project or select an existing one
3. In the menu on the left, find "APIs & Services" > "Library"
4. Find the "Google Books API" and activate it
5. Go back to "APIs & Services" > "Credentials"
6. Click "Create credentials" > "API key"
7. Save the received key.

## Install and run on Windows:

### Step 1: Install Python 3.10
1. Download the Python 3.10.x installer from the official website: [https://www.python.org/downloads/release/python-3100/](https://www.python.org/downloads/release/python-3100/)
2. Select the installer "Windows installer (64-bit)" and download it
3. Run the installer
4. **IMPORTANT**: Check the box "Add Python to PATH" at the beginning of the installation.
5. Click "Install Now" and wait for the installation to complete.

### Step 2: Download the bot code
1. Create a new folder on your computer, for example, "telegram-bot"
2. Save the file with the bot code to this folder called `bot.py `

### Step 3: Open the Command Prompt
1. Press the `Win + R` keys on your keyboard
2. Type `cmd` and press Enter
3. In the command prompt that opens, navigate to the folder you created:
``
   cd path to your folder\telegram-bot
   ``
(for example: `cd C:\Users\Name of \Documents\telegram-bot`)

### Step 4: Install the necessary libraries
1. At the command prompt, type:
   ```
   pip install aiogram==3.0.0 requests
   ```
2. Wait for the installation to finish

### Step 5: Configuring API Keys
1. Open the file `bot.py ` in any text editor (for example, Notepad)
2. Find the following lines:
``python
   API_TOKEN = 'YOUR_TELEGRAM_BOT_TOKEN'
   TMDB_API_KEY = 'YOUR_TMDB_API_KEY'
   GOOGLE_BOOKS_API_KEY = 'YOUR_GOOGLE_BOOKS_API_KEY'
   ```
3. Replace `YOUR_TELEGRAM_BOT_TOKEN" with the token received from @BotFather, keeping the quotes.
4. Replace `YOUR_TMDB_API_KEY" with your TMDb key, keeping the quotes.
5. Replace `YOUR_GOOGLE_BOOKS_API_KEY" with your Google Books key, keeping the quotes.
6. Save the changes to the file

### Step 6: Launch the Bot
1. At the command prompt, type:
   ```
   python bot.py
   ```
2. If the bot has started successfully, you will see the message "The bot is running!"
3. Now you can open Telegram and start communicating with your bot.

### Step 7: Stop the Bot
To stop the bot, press `Ctrl + C' in the command prompt

## Install and run on Linux:

### Step 1: Install Python 3.10
Open a terminal and enter the following commands:

For Ubuntu/Debian:
```
sudo apt update
sudo apt install software-properties-common
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt update
sudo apt install python3.10 python3.10-venv python3-pip
```

For Fedora:
```
sudo dnf install python3.10
```

### Step 2: Create a directory and a bot file
1. Create a new directory:
   ```
   mkdir ~/telegram-bot
   cd ~/telegram-bot
   ```
2. Create a bot file:
   ```
   nano bot.py
   ```
3. Copy the bot code into the editor that opens
4. Press `Ctrl + O', then Enter to save
5. Press `Ctrl + X` to exit the editor

### Step 3: Create a virtual environment and install dependencies
1. In the terminal (located in the ~/telegram-bot folder), run:
   ```
   python3.10 -m venv venv
   source venv/bin/activate
   pip install aiogram==3.0.0 requests
   ```

### Step 4: Configuring API Keys
1. Open the bot file for editing:
   ```
   nano bot.py
   ```
2. Find the following lines:
``python
   API_TOKEN = 'YOUR_TELEGRAM_BOT_TOKEN'
   TMDB_API_KEY = 'YOUR_TMDB_API_KEY'
   GOOGLE_BOOKS_API_KEY = 'YOUR_GOOGLE_BOOKS_API_KEY'
   ```
3. Replace `YOUR_TELEGRAM_BOT_TOKEN" with the token received from @BotFather, keeping the quotes.
4. Replace `YOUR_TMDB_API_KEY" with your TMDb key, keeping the quotes.
5. Replace `YOUR_GOOGLE_BOOKS_API_KEY" with your Google Books key, keeping the quotes.
6. Press `Ctrl + O', then Enter to save
7. Press `Ctrl + X' to exit the editor

### Step 5: Launch the Bot
1. In the terminal, enter:
   ```
   python bot.py
   ```
2. If the bot has started successfully, you will see the message "The bot is running!"
3. Now you can open Telegram and start communicating with your bot

### Step 6: Running the bot in the background (optional)
If you want the bot to run in the background after closing the terminal:
1. Install screen:
   ```
   sudo apt install screen # for Ubuntu/Debian
   sudo dnf install screen # for Fedora
   ```
2. Create a new screen session:
   ```
   screen -S bot
   ```
3. Activate the virtual environment and launch the bot:
   ```
   cd ~/telegram-bot
   source venv/bin/activate
   python bot.py
   ```
4. Press `Ctrl + A', then `D` to disconnect from the screen session (the bot will continue to work)
5. To return to the session, enter:
   ```
   screen -r bot
   ```

## Using a bot:

After launching the bot, you can use the following commands in Telegram:

1. `/start` - start interacting with the bot
2. `/help` - get instructions for use
3. `/recommend` - get a random recommendation
4. `/genre` - select a specific genre for the recommendation

## Problem solving:

1. **Error "ModuleNotFoundError"**: Make sure that you have installed all libraries correctly using pip
2. **Error when launching the bot**: Check that you have correctly specified the Telegram bot token and API keys
3. **The bot is not responding in Telegram**: Make sure that the bot is running on the command line/terminal and that you have started a dialogue with the correct bot

## Additional information:

- The bot uses The Movie Database (TMDb) to get information about movies
- The bot uses Google Books API to get information about books
- All data is updated in real time

If you have any problems or questions, you can refer to the documentation.:
- [aiogram documentation](https://docs.aiogram.dev /)
- [TMDb API Documentation](https://developers .themoviedb.org/3 )
- [Google Books API Documentation](https://developers.google.com/books )
