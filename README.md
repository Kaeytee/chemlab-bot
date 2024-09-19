# Molecular Formula to IUPAC Name Converter Bot

This Telegram bot converts molecular formulas to their corresponding IUPAC (International Union of Pure and Applied Chemistry) names. Simply send a molecular formula to the bot, and it will respond with the IUPAC name of the compound.

## Features

- Converts molecular formulas to IUPAC names
- Easy to use within Telegram
- Provides quick and accurate responses
- Integrated contact options (WhatsApp, Email, and Map links)
- Main menu for easy access to bot features

## How to Use

1. Start a chat with the bot on Telegram: [@ChemLab_Bot](https://t.me/Chemlabb_bot)
2. Send a molecular formula (e.g., "C3H8", "H2O", "C6H12O6")
3. The bot will reply with the IUPAC name of the compound

## Examples

- Input: `C3H8`  
  Output: Propane

- Input: `H2O`  
  Output: Water

- Input: `C6H12O6`  
  Output: Hexose

## Technical Details

This bot is built using **Python** and the **python-telegram-bot** library. It uses custom logic for determining the IUPAC names based on molecular formulas.

### Key Libraries:
- `python-telegram-bot`: To handle Telegram Bot API
- `python-dotenv`: To securely manage environment variables like the Telegram bot token

## Installation

Follow these steps to set up and run the bot locally or on your own server.

### Prerequisites

- Python 3.7 or higher
- pip (Python package installer)

### Step 1: Clone the repository

```bash
git clone https://github.com/your-username/molecular-formula-bot.git
cd molecular-formula-bot
```

### Step 2: Create a virtual environment

It's recommended to use a virtual environment to manage dependencies:

```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

### Step 3: Install dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Set up environment variables

Create a `.env` file in the root directory and add your Telegram Bot Token:

```
TELEGRAM_BOT_TOKEN=your_bot_token_here
```

### Step 5: Run the bot

```bash
python bot.py
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact

If you have any questions or suggestions, please feel free to reach out:

- **WhatsApp**: [+233534544454](https://wa.me//+233534544454)
- **Email**: [@Austin](mailto:austinbediako4@gmail.com)
- **Location**: [View_on_Google_Maps]([https://www.google.com/maps?q=your+location](https://www.google.com/maps/d/viewer?mid=1lTnYKOYpRIhgnZGYozcfmoOh9tc&hl=en&ll=6.129593864887134%2C-0.20541400000001597&z=8))

You can also open an issue in this repository for bug reports or feature requests.

---

Made with ❤️ by [Austin Bediako]
