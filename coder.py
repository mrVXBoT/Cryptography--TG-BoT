import logging
import base64
import asyncio
from aiogram import Bot, Dispatcher, F, types
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command
from aiogram.enums import ParseMode
from aiogram.exceptions import TelegramBadRequest
import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)

# Bot token
API_TOKEN = '<your-bot-token>'

# Admin ID
ADMIN_ID = <admin-id>

# Define a prefix for encrypted messages to identify them later
ENCRYPTION_PREFIX = "VX_ENCRYPTED:"

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)

class UserState(StatesGroup):
    waiting_for_encode = State()
    waiting_for_decode = State()

# Encryption/decryption functions
def encrypt_text(text):
    """Encrypt text using base64 with our custom prefix"""
    encoded_bytes = base64.b64encode(text.encode('utf-8'))
    return f"{ENCRYPTION_PREFIX}{encoded_bytes.decode('utf-8')}"

def decrypt_text(text):
    """Decrypt text using base64"""
    # Remove our prefix if it exists
    if text.startswith(ENCRYPTION_PREFIX):
        text = text[len(ENCRYPTION_PREFIX):]
    try:
        decoded_bytes = base64.b64decode(text)
        return decoded_bytes.decode('utf-8')
    except:
        return "Error: This doesn't appear to be a valid encrypted text."

def is_encrypted(text):
    """Check if the text is encrypted by our bot"""
    if not text:
        return False
        
    return text.startswith(ENCRYPTION_PREFIX) or (
        # Check if it looks like a base64 string (fallback detection)
        all(c in 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=' for c in text)
        and len(text) % 4 == 0
    )

# Create keyboards
def get_main_keyboard():
    buttons = [
        [
            types.KeyboardButton(text="🔒 Encrypt"),
            types.KeyboardButton(text="🔓 Decrypt")
        ],
        [
            types.KeyboardButton(text="👤 About Me"),
            types.KeyboardButton(text="📢 Channels")
        ]
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)
    return keyboard

# Command handlers
@dp.message(Command("start"))
async def send_welcome(message: types.Message):
    """Send welcome message and pin it"""
    welcome_text = (
        "*Welcome to VX Encoder & Decoder Bot* 👋\n\n"
        "📚 *Bot Functionality:*\n\n"
        "You send your code to the bot and it encrypts it. For example:\n\n"
        "`echo \"hello how are you\";`\n\n"
        "The bot will encrypt this code and convert it to:\n\n"
        "`VX_ENCRYPTED:ZWNobyAiaGVsbG8gaG93IGFyZSB5b3UiOw==`\n\n"
        "If you want to decrypt it, press the Decrypt button and send the encrypted text.\n\n"
        "*You can also use inline mode by typing @your_bot_username in any chat!*"
    )
    
    # Send welcome message with markdown formatting
    welcome_msg = await message.answer(
        welcome_text,
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=get_main_keyboard()
    )
    
    # Try to pin the message
    try:
        await bot.pin_chat_message(
            chat_id=message.chat.id,
            message_id=welcome_msg.message_id,
            disable_notification=True
        )
    except TelegramBadRequest as e:
        logging.error(f"Cannot pin message: {e}")

@dp.message(F.text == "📢 Channels")
async def show_channels(message: types.Message):
    """Show channel information"""
    channels_text = (
        "*Join our channels:*\n\n"
        "[@l27_0](https://t.me/l27_0)\n"
        "[@Pv_vX](https://t.me/Pv_vX)\n"
        "[@Ye_vX](https://t.me/Ye_vX)"
    )
    
    await message.answer(
        channels_text,
        parse_mode=ParseMode.MARKDOWN,
        disable_web_page_preview=True
    )

@dp.message(F.text == "👤 About Me")
async def show_about(message: types.Message):
    """Show developer information"""
    about_text = (
        "*Developer information:*\n\n"
        "[@KoxVX](https://t.me/KoxVX)"
    )
    
    await message.answer(
        about_text,
        parse_mode=ParseMode.MARKDOWN,
        disable_web_page_preview=True
    )

@dp.message(F.text == "🔒 Encrypt")
async def encrypt_command(message: types.Message, state: FSMContext):
    """Handle encrypt command"""
    await message.answer(
        "*Please enter the text you want to encrypt:*",
        parse_mode=ParseMode.MARKDOWN
    )
    await state.set_state(UserState.waiting_for_encode)

@dp.message(F.text == "🔓 Decrypt")
async def decrypt_command(message: types.Message, state: FSMContext):
    """Handle decrypt command"""
    await message.answer(
        "*Please enter the text you want to decrypt:*",
        parse_mode=ParseMode.MARKDOWN
    )
    await state.set_state(UserState.waiting_for_decode)

@dp.message(UserState.waiting_for_encode)
async def encrypt_text_handler(message: types.Message, state: FSMContext):
    """Encrypt user text"""
    encrypted = encrypt_text(message.text)
    
    # Create inline button to decrypt
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[[
            InlineKeyboardButton(text="🔓 Decrypt", callback_data=f"decrypt:{encrypted}")
        ]]
    )
    
    await message.answer(
        f"*Encrypted Text:*\n\n`{encrypted}`",
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=keyboard
    )
    await state.clear()

@dp.message(UserState.waiting_for_decode)
async def decrypt_text_handler(message: types.Message, state: FSMContext):
    """Decrypt user text"""
    decrypted = decrypt_text(message.text)
    
    # Create inline button to encrypt again
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[[
            InlineKeyboardButton(text="🔒 Encrypt Again", callback_data=f"encrypt:{decrypted}")
        ]]
    )
    
    await message.answer(
        f"*Decrypted Text:*\n\n`{decrypted}`",
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=keyboard
    )
    await state.clear()

# Automatically decrypt if the message appears to be encrypted
@dp.message(lambda message: is_encrypted(message.text))
async def auto_decrypt_handler(message: types.Message):
    """Auto-decrypt encrypted messages"""
    decrypted = decrypt_text(message.text)
    
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[[
            InlineKeyboardButton(text="🔒 Encrypt Again", callback_data=f"encrypt:{decrypted}")
        ]]
    )
    
    await message.answer(
        f"*Auto-Detected Encrypted Text! Decrypted:*\n\n`{decrypted}`",
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=keyboard
    )

# Callback query handlers for inline buttons
@dp.callback_query(lambda c: c.data.startswith('decrypt:'))
async def process_decrypt_callback(callback_query: types.CallbackQuery):
    """Process decrypt button press"""
    await callback_query.answer()
    
    # Get the encrypted text from callback data
    encrypted_text = callback_query.data[8:]  # Remove 'decrypt:' prefix
    decrypted = decrypt_text(encrypted_text)
    
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[[
            InlineKeyboardButton(text="🔒 Encrypt Again", callback_data=f"encrypt:{decrypted}")
        ]]
    )
    
    await callback_query.message.edit_text(
        f"*Decrypted Text:*\n\n`{decrypted}`",
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=keyboard
    )

@dp.callback_query(lambda c: c.data.startswith('encrypt:'))
async def process_encrypt_callback(callback_query: types.CallbackQuery):
    """Process encrypt button press"""
    await callback_query.answer()
    
    # Get the plain text from callback data
    plain_text = callback_query.data[8:]  # Remove 'encrypt:' prefix
    encrypted = encrypt_text(plain_text)
    
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[[
            InlineKeyboardButton(text="🔓 Decrypt", callback_data=f"decrypt:{encrypted}")
        ]]
    )
    
    await callback_query.message.edit_text(
        f"*Encrypted Text:*\n\n`{encrypted}`",
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=keyboard
    )

# Inline mode handlers
@dp.inline_query()
async def inline_query_handler(inline_query: types.InlineQuery):
    """Handle inline queries"""
    text = inline_query.query or "Type something to encrypt/decrypt"
    
    # Generate results
    results = []
    
    # Option to encrypt
    encrypted = encrypt_text(text)
    
    # Result for encryption
    encrypt_result = types.InlineQueryResultArticle(
        id="1",
        title="🔒 Encrypt Text",
        description=f"Encrypt: {text}",
        input_message_content=types.InputTextMessageContent(
            message_text=f"*Encrypted:*\n\n`{encrypted}`",
            parse_mode=ParseMode.MARKDOWN
        ),
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[[
                InlineKeyboardButton(text="🔓 Decrypt", callback_data=f"decrypt:{encrypted}")
            ]]
        )
    )
    
    results.append(encrypt_result)
    
    # If it looks like an encrypted message, also offer to decrypt
    if is_encrypted(text):
        decrypted = decrypt_text(text)
        decrypt_result = types.InlineQueryResultArticle(
            id="2",
            title="🔓 Decrypt Text",
            description=f"Decrypt: {text[:20]}...",
            input_message_content=types.InputTextMessageContent(
                message_text=f"*Decrypted:*\n\n`{decrypted}`",
                parse_mode=ParseMode.MARKDOWN
            ),
            reply_markup=InlineKeyboardMarkup(
                inline_keyboard=[[
                    InlineKeyboardButton(text="🔒 Encrypt Again", callback_data=f"encrypt:{decrypted}")
                ]]
            )
        )
        results.append(decrypt_result)
    
    # Send results
    await bot.answer_inline_query(
        inline_query.id, 
        results=results, 
        cache_time=1
    )

async def main():
    # Start the bot
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main()) 