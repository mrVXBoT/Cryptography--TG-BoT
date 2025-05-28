# Cryptography--TG-BoT
# VX Encoder & Decoder Bot

A Telegram bot for encrypting and decrypting messages using Base64 encoding.

![Telegram Bot](https://img.shields.io/badge/Telegram-Bot-2CA5E0?style=flat-square&logo=telegram)
![Python](https://img.shields.io/badge/Python-3.7+-blue.svg?style=flat-square&logo=python)
![Aiogram](https://img.shields.io/badge/Aiogram-3.0+-2CA5E0.svg?style=flat-square)

## Features

- **Text Encryption**: Convert plain text to Base64 encoded format with a custom prefix
- **Text Decryption**: Convert encoded text back to readable format
- **Auto-Detection**: Automatically recognize and decrypt messages that look encrypted
- **Inline Mode**: Use the bot in any chat by typing its username and your text
- **Interactive Buttons**: Easy-to-use inline buttons for encryption/decryption actions
- **Message Pinning**: Welcome message is automatically pinned in chat
- **Rich Formatting**: Uses Markdown formatting for better readability

## Commands

- `/start` - Start the bot and display welcome message
- `🔒 Encrypt` - Switch to encryption mode
- `🔓 Decrypt` - Switch to decryption mode
- `👤 About Me` - Display developer information
- `📢 Channels` - Show related Telegram channels

## How It Works

### Encryption
The bot uses Base64 encoding and adds a custom prefix (`VX_ENCRYPTED:`) to identify encrypted messages:

```
Input: echo "hello how are you";
Output: VX_ENCRYPTED:ZWNobyAiaGVsbG8gaG93IGFyZSB5b3UiOw==
```

### Decryption
The bot removes the prefix (if present) and decodes the Base64 string:

```
Input: VX_ENCRYPTED:ZWNobyAiaGVsbG8gaG93IGFyZSB5b3UiOw==
Output: echo "hello how are you";
```

### Inline Mode
You can use the bot in any chat by typing `@your_bot_username` followed by text to encrypt or decrypt:

1. Type `@your_bot_username text_to_process`
2. Select whether to encrypt or decrypt (if the text appears to be encrypted)
3. The bot will send the processed text with an option to reverse the operation

## Installation and Setup

1. Clone this repository
2. Install requirements:
   ```
   pip install aiogram>=3.0.0 python-dotenv==1.0.0
   ```
3. Set your bot token in `coder.py`:
   ```python
   API_TOKEN = 'YOUR_BOT_TOKEN'
   ```
4. Run the bot:
   ```
   python coder.py
   ```

## Technical Details

- Framework: Aiogram 3.x
- State management: FSM (Finite State Machine)
- Encryption: Base64 with custom prefix
- Keyboard types: Reply keyboard and inline keyboard

## Contact

- [@KoxVX](https://t.me/KoxVX)

## Related Channels

- [@l27_0](https://t.me/l27_0)
- [@Pv_vX](https://t.me/Pv_vX)
- [@Ye_vX](https://t.me/Ye_vX) 
