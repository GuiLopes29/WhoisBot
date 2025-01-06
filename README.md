<p align="center">
    <img src="https://github.com/user-attachments/assets/1747dbaf-459c-402b-8944-cfaf25aa11c6" alt="WhoisBot Logo" width="200"/>
    <br>
    A discord bot to verify the whois status of a domain
</p>

## Requirements

- Python 3.11 or higher
- Discord API Token (configure in the `.env` file)

## Installation

1. Clone the repository:

```sh
git clone https://github.com/GuiLopes29/WhoisBot.git
cd WhoisBot
```

<br>

2º Create and activate a virtual environment:

```sh
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

<br>

3º Install the dependencies:

```sh
pip install -r requirements.txt
```

<br>

4º Configure the .env file with your Discord token and channel:

```env
DISCORD_TOKEN=your-token-here
DISCORD_CHANNEL=your-channel-id-here
```

## Uso

To start the bot, run:

```sh
python main.py
```
