import os
import re
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters
import logging

# Load environment variables from .env file
load_dotenv()

# Get the bot token from the environment variable
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

# Function to dynamically generate prefixes up to 1000 carbons
def generate_prefix(n):
    base_prefixes = [
        "meth", "eth", "prop", "but", "pent", "hex", "hept", "oct", "non", "dec"
    ]
    tens_prefixes = [
        "dec", "icos", "tricos", "tetracos", "pentacos", "hexacos", "heptacos", "octacos", "nonacos"
    ]

    if n <= 10:
        return base_prefixes[n - 1]
    elif n < 100:
        tens = n // 10
        ones = n % 10
        return tens_prefixes[tens - 1] + (base_prefixes[ones - 1] if ones > 0 else "")
    else:
        hundreds = n // 100
        remainder = n % 100
        hundreds_prefix = base_prefixes[hundreds - 1] + "cent"
        return hundreds_prefix + (generate_prefix(remainder) if remainder > 0 else "")

# Function to generate IUPAC names based on molecular formula
def name_compound(structure):
    compound_data = get_functional_group(structure)

    if compound_data['carbon_count'] > 1000:
        return "Structure too complex for current naming logic."

    prefix = generate_prefix(compound_data['carbon_count'])

    if compound_data['grp'] == "alkane":
        name = prefix + "ane"
    elif compound_data['grp'] == "alkene":
        name = prefix + "ene"
    elif compound_data['grp'] == "alkyne":
        name = prefix + "yne"
    elif compound_data['grp'] == "alkanol":
        name = prefix + "anol"
    elif compound_data['grp'] == "alkanoic acid":
        name = prefix + "anoic acid"
    else:
        return "Invalid structure"

    return name.capitalize()

# Function to identify the functional group and carbon count
def get_functional_group(structure):
    grp = "Unavailable"
    carbon_count = 0

    # Special case for formic acid (HCOOH)
    if structure == "HCOOH" or structure == "HCO2H":
        grp = "alkanoic acid"
        carbon_count = 1
        return {'grp': grp, 'carbon_count': carbon_count}

    # Hydrocarbons: alkanes, alkenes, alkynes
    hydrocarbon_match = re.match(r'^C(\d*)H(\d+)$', structure.upper())
    if hydrocarbon_match:
        carbon_count = int(hydrocarbon_match.group(1) or '1')
        hydrogen_count = int(hydrocarbon_match.group(2))

        if hydrogen_count == 2 * carbon_count + 2:
            grp = "alkane"
        elif hydrogen_count == 2 * carbon_count:
            grp = "alkene"
        elif hydrogen_count == 2 * carbon_count - 2:
            grp = "alkyne"

    return {'grp': grp, 'carbon_count': carbon_count}

# Function to display the main menu
async def show_menu(update: Update, context) -> None:
    keyboard = [
        [InlineKeyboardButton("💬 WhatsApp Us", url="https://wa.me/233534544454")],
        [InlineKeyboardButton("📧 Email Us", url="mailto:info@chemlab.com")],
        [InlineKeyboardButton("📍 Find Us on Map", url="https://maps.app.goo.gl/vjXPCjceysvijGyT7")],
        [InlineKeyboardButton("🔗 Visit Website", url='https://t.me/iv?url=https://chemistry-app-six.vercel.app')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        "🔍 Main Menu:\n\nChoose from the options below:", 
        reply_markup=reply_markup
    )

# Start function for the bot
async def start(update: Update, context) -> None:
    """Send a welcome message with main menu and available commands."""
    await update.message.reply_text(
        "👋 Welcome to ChemLab Bot!\n\n⚗️ Enter a molecular formula (e.g., C3H8) to get the IUPAC name.\n\nYou can use the following commands:\n"
        "/menu - Access the main menu\n"
        "/help - List of commands"
    )
    await show_menu(update, context)

# Help command to list available commands
async def help_command(update: Update, context) -> None:
    await update.message.reply_text(
        "🛠 Available commands:\n"
        "/start - Start the bot\n"
        "/menu - Access the main menu\n"
        "/help - List of available commands\n"
        "\nEnter a molecular formula to get the IUPAC name."
    )

# Function to handle the IUPAC name based on user input
async def handle_message(update: Update, context) -> None:
    text = update.message.text
    # Check if input is in lowercase and prompt user to correct it
    if text != text.upper():
        await update.message.reply_text("⚠️ Please enter the formula in uppercase. The bot is case-sensitive.")
        return

    try:
        iupac_name = name_compound(text.strip().upper())
        await update.message.reply_text(f"🧪 IUPAC Name: {iupac_name}")
    except Exception as e:
        await update.message.reply_text(f"❌ An error occurred: {str(e)}")

# Error handling
async def error(update: Update, context) -> None:
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)

def main() -> None:
    """Start the bot."""
    application = Application.builder().token(TOKEN).build()

    # Register start command
    application.add_handler(CommandHandler("start", start))

    # Register help command
    application.add_handler(CommandHandler("help", help_command))

    # Register /menu command to access main menu anytime
    application.add_handler(CommandHandler("menu", show_menu))

    # Register message handler for IUPAC name generation
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Log all errors
    application.add_error_handler(error)

    # Start the Bot
    application.run_polling()

if __name__ == '__main__':
    main()
