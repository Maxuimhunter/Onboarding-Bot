# On-Boarding Discord Bot

## Update History

### August 5, 2025
- **Separate Identity Data Storage**: Implemented secure storage of sensitive identity information (ID, Passport, KRA) in a separate Excel file (`onboarding_data_identity.xlsx`)
- **Enhanced Security**: Improved data handling by isolating sensitive information from general user data
- **Updated Documentation**: Revised README to reflect new data storage structure and security measures

---


A Discord bot for managing member onboarding and status tracking for AAR Insurance. The bot collects member information and maintains their status in Excel files, with sensitive data stored separately for security.

## Features

- Interactive onboarding process
- Unique entry code generation for each member
- Member status management (Active/Inactive)
- Secure storage of sensitive identity information in a separate file
- Excel data storage with automatic formatting
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

### Main Data File: `onboarding_data.xlsx`
Contains general member information:
- Entry Code (auto-generated)
- User ID (Discord ID)
- Full Name
- Email
- Phone
- Date of Birth
- Registration Date (auto-filled)
- Status (Active/Inactive)

### Identity Data File: `onboarding_data_identity.xlsx`
Stores sensitive identity information separately:
- Full Name
- ID Number (if provided)
- Passport Number (if provided)
- KRA PIN (if provided)
- Last Updated timestamp

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

## Security Notes
- Sensitive identity information is stored in a separate file for enhanced security
- The bot only stores the data you provide during the onboarding process
- Ensure proper file system permissions are set for the Excel files

## Future Improvements

### Data Management
- [ ] Database Integration: Migrate from Excel to a proper database (e.g., SQLite or PostgreSQL) for better performance and reliability
- [ ] Data Encryption: Implement encryption for sensitive data at rest
- [ ] Backup System: Add automated backup functionality for the data files
- [ ] Imigration with MySQL DataBase for Easier and quicker storage of User data and Input

### Bot Features
- [ ] Admin Dashboard: Web interface for managing users and viewing statistics
- [ ] Bulk Operations: Commands for managing multiple users at once
- [ ] Data Export: Additional export formats (CSV, PDF) for reports
- [ ] Advanced Search: Enhanced search functionality for user records

### Security Enhancements
- [ ] Role-based Access Control: Different permission levels for different user roles
- [ ] Audit Logging: Track all changes made to user data
- [ ] Two-Factor Authentication: Additional security for sensitive operations

### User Experience
- [ ] Progress Saving: Allow users to save and resume the onboarding process
- [ ] Form Validation: More robust input validation and error messages
- [ ] Multi-language Support: Support for multiple languages in the bot interface

## Usage Notes
- The bot requires an internet connection to communicate with Discord's servers
- Ensure the bot has the necessary permissions in your Discord server
- The Excel files will be created automatically when the first user registers
- **Important**: Close the Excel files before using bot commands, as they won't be modifiable while open in Excel
- The bot will automatically create and manage both the main data file and the identity data file
