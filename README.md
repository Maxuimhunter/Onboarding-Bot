# AAR Insurance Discord Bot

A Discord bot for managing member onboarding and status tracking for AAR Insurance. The bot collects member information and maintains their status in an Excel file.

## Features

- Interactive onboarding process
- Unique entry code generation for each member
- Member status management (Active/Inactive)
- Excel data storage with formatting
- Easy-to-use Discord commands
- Real-time status updates

## Prerequisites

- Python 3.7+
- Discord Bot Token
- Required Python packages (install using `pip install -r requirements.txt`)

## Installation

1. Clone this repository
2. Navigate to the project directory
3. Install the required packages:
   ```
   pip install discord.py pandas openpyxl python-dotenv
   ```
4. Create a `.env` file in the project root with your Discord bot token:
   ```
   DISCORD_TOKEN=your_bot_token_here
   ```

## Bot Commands

### `!start`
Starts the onboarding process. The bot will guide you through collecting:
- Full Name
- Email Address
- Phone Number
- Date of Birth (DD/MM/YYYY)

Example:
```
!start
```

### `!status`
Displays all members and their current statuses.

Example:
```
!status
```

### `!status [entry_code] [action]`
Updates a member's status. Available actions: `activate` or `deactivate`

Examples:
```
!status A1B2C3D4 activate
!status X9Y8Z7W6 deactivate
```

### `!helpme`
Displays the help message with all available commands.

## Data Storage

All member information is stored in `onboarding_data.xlsx` with the following columns:
- Entry Code (auto-generated)
- User ID (Discord ID)
- Full Name
- Email
- Phone
- Date of Birth
- Registration Date (auto-filled)
- Status (Active/Inactive)

## Setup Instructions

1. Create a Discord bot in the [Discord Developer Portal](https://discord.com/developers/applications)
2. Add the bot to your server with the following permissions:
   - Send Messages
   - Read Messages/View Channels
   - Embed Links
   - Read Message History
3. Copy the bot token and add it to your `.env` file
4. Run the bot:
   ```
   python bot.py
   ```

## Notes
- The bot requires an internet connection to communicate with Discord's servers
- Ensure the bot has the necessary permissions in your Discord server
- The Excel file will be created automatically when the first user registers
- **Important**: Close the Excel file before using `!status` or onboarding commands, as the bot won't be able to modify the file while it's open in Excel

- The KRA verification is currently commented out as requested. Uncomment and implement the verification logic in the `verify_kra()` function as needed.
- Document scanning functionality is a placeholder. You'll need to integrate with a scanning library for actual scanning capabilities.
