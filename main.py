import os
import logging
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

from comfy import ComfyClient  # Updated import

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(module)s - %(message)s", 
    level=logging.INFO
)
# Set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

load_dotenv()
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# Create an instance of ComfyClient
comfy_client = ComfyClient()


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    await update.message.reply_text(
        "Hi! Send me an image description and I will generate it for you."
    )

async def generate_image(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Generate an image based on the user's description."""
    user_prompt = update.message.text  # The user's message text

    logging.info(f"Received prompt from user {update.effective_user.username}: {user_prompt}")

    # Generate the image using ComfyClient
    img_data = comfy_client.generate_image(
        user_prompt, seed=update.message.message_id
    )

    # Ensure the images directory exists
    os.makedirs("images", exist_ok=True)
    filename = "images/" + img_data["filename"]

    # Save the image using ComfyClient
    comfy_client.save_image(img_data, filename)

    # Send the generated image back to the user
    with open(filename, "rb") as photo_file:
        await context.bot.send_photo(
            chat_id=update.effective_chat.id, photo=photo_file
        )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    await update.message.reply_text("Help!")


def main() -> None:
    """Start the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(TOKEN).build()

    # On different commands - answer in Telegram
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))

    # On non-command message - generate image based on the message text
    application.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, generate_image)
    )

    # Run the bot until the user presses Ctrl-C
    application.run_polling()


if __name__ == "__main__":
    main()
