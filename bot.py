import logging
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, filters, CallbackContext

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

# Your bot token from the BotFather
TOKEN = "***REMOVED***"

# List of prefixes for carbon chain length (up to 1000 carbons)
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
    hydrocarbon_match = structure.upper().match(r'^C(\d*)H(\d+)$')
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

# Start function for the bot
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(
        "Welcome to ChemLab Bot! Enter a molecular formula (e.g., C3H8) to get the IUPAC name."
    )

# Function to handle the IUPAC name based on user input
def handle_message(update: Update, context: CallbackContext) -> None:
    text = update.message.text
    try:
        iupac_name = name_compound(text.strip().upper())
        update.message.reply_text(f"IUPAC Name: {iupac_name}")
    except Exception as e:
        update.message.reply_text(f"An error occurred: {str(e)}")

# Error handling
def error(update: Update, context: CallbackContext) -> None:
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)

def main() -> None:
    # Create the Updater and pass it your bot's token.
    updater = Updater(TOKEN, use_context=True)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # Register start command
    dispatcher.add_handler(CommandHandler("start", start))

    # Register message handler for IUPAC name generation
    dispatcher.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Log all errors
    dispatcher.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT, SIGTERM or SIGABRT
    updater.idle()

if __name__ == '__main__':
    main()