import os
import re
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters
import logging
from telegram.error import InvalidToken
# Load environment variables from .env file
load_dotenv()

# Get the bot token from the environment variable
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

# Function to generate the prefix based on the number of carbons
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

# Function to identify the functional group and carbon count from the molecular structure
def get_functional_group(structure):
    grp = "Unavailable"
    carbon_count = 0
    pos = ""
    use_pos = False

    # Special case for formic acid (HCOOH)
    if structure in ["HCOOH", "HCO2H"]:
        grp = "alkanoic acid"
        carbon_count = 1  # Formic acid has only 1 carbon atom
        return {"grp": grp, "carbonCount": carbon_count, "usePos": use_pos, "pos": pos}

    # General hydrocarbon patterns: Alkanes, Alkenes, Alkynes
    hydro_carbon_match = re.match(r'^C(\d*)H(\d+)$', structure)
    if hydro_carbon_match:
        carbon_count = int(hydro_carbon_match.group(1) or '1')
        hydrogen_count = int(hydro_carbon_match.group(2))
        if hydrogen_count == 2 * carbon_count + 2:
            grp = "alkane"
        elif hydrogen_count == 2 * carbon_count:
            grp = "alkene"
        elif hydrogen_count == 2 * carbon_count - 2:
            grp = "alkyne"
        return {"grp": grp, "carbonCount": carbon_count, "usePos": use_pos, "pos": pos}

    # Alcohols (Alkanols): CnH2n+1OH
    alkanol_match = re.match(r'^C(\d*)H(\d+)OH$', structure)
    if alkanol_match:
        carbon_count = int(alkanol_match.group(1) or '1')
        grp = "alkanol"
        if carbon_count > 2:
            pos = "1"  # Primary alcohol (OH group on the first carbon)
            use_pos = True
        return {"grp": grp, "carbonCount": carbon_count, "usePos": use_pos, "pos": pos}

    # Carboxylic Acids (Alkanoic Acids): CnH2n+1COOH or CnH2n+1CO2H
    alkanoic_acid_match = re.match(r'^C(\d*)H(\d+)(COOH|CO2H)$', structure)
    if alkanoic_acid_match:
        carbon_count = int(alkanoic_acid_match.group(1) or '1') + 1  # Add 1 for the carboxyl group (COOH)
        grp = "alkanoic acid"
        return {"grp": grp, "carbonCount": carbon_count, "usePos": use_pos, "pos": pos}

    # Esters (RCOOR): Alkanoic acids where the -OH group is replaced by -OR
    ester_match = re.match(r'^C(\d*)H(\d+)(COOR|CO2R)$', structure)
    if ester_match:
        carbon_count = int(ester_match.group(1) or '1') + 1
        grp = "ester"
        return {"grp": grp, "carbonCount": carbon_count, "usePos": use_pos, "pos": pos}

    # Aldehydes (RCHO): Alkanal group
    aldehyde_match = re.match(r'^C(\d*)H(\d+)O$', structure)
    if aldehyde_match:
        carbon_count = int(aldehyde_match.group(1) or '1')
        grp = "aldehyde"
        return {"grp": grp, "carbonCount": carbon_count, "usePos": use_pos, "pos": pos}

    # Ketones (RCOR): Alkanone group
    ketone_match = re.match(r'^C(\d*)H(\d+)O$', structure)
    if ketone_match:
        carbon_count = int(ketone_match.group(1) or '1')
        grp = "ketone"
        return {"grp": grp, "carbonCount": carbon_count, "usePos": use_pos, "pos": pos}

    return {"grp": grp, "carbonCount": carbon_count, "usePos": use_pos, "pos": pos}

# Function to generate IUPAC names based on molecular formula
def name_compound(structure):
    compound_data = get_functional_group(structure)

    if compound_data['carbonCount'] > 1000:
        return "Structure too complex for current naming logic."

    prefix = generate_prefix(compound_data['carbonCount'])

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
    elif compound_data['grp'] == "ester":
        name = prefix + "oate"
    elif compound_data['grp'] == "aldehyde":
        name = prefix + "al"
    elif compound_data['grp'] == "ketone":
        name = prefix + "one"
    else:
        return "Invalid structure"

    if compound_data['usePos']:
        name = compound_data['pos'] + "-" + name

    return name.capitalize()

# Start function for the bot
async def start(update: Update, context) -> None:
    """Send a welcome message with main menu and available links as buttons."""
    keyboard = [
        [InlineKeyboardButton("💬 WhatsApp Us", url="https://wa.me/233534544454")],
        [InlineKeyboardButton("📧 Email Us", url="mailto:info@chemlab.com")],
        [InlineKeyboardButton("📍 Find Us on Map", url="https://maps.app.goo.gl/vjXPCjceysvijGyT7")],
        [InlineKeyboardButton("🔗 Visit Website", url='https://chemistry-app-six.vercel.app')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        "👋 Welcome to ChemLab Bot!\n\n⚗️ Enter a molecular formula (e.g., C3H8) to get the IUPAC name.\n\n"
        "Here are some useful links for you:",
        reply_markup=reply_markup
    )

# Help command to list available commands
async def help_command(update: Update, context) -> None:
    await update.message.reply_text(
        "🛠 Available commands:\n"
        "/start - Start the bot and access the links\n"
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

    # Register message handler for IUPAC name generation
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Log all errors
    application.add_error_handler(error)

    # Start the Bot
    application.run_polling()

if __name__ == '__main__':
    main()
