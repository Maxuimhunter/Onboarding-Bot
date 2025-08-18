# Onboarding Bot

> **Note:** There may be a slight duplication issue that will be addressed in a future update.

## Update History

### August 15, 2025
- **Fixed Message Duplication**: Completely rewrote message handling to prevent duplicate prompts
- **Improved Command Processing**: Enhanced command handling to prevent conflicts between bot commands and onboarding flow
- **Added Session Management**: Implemented checks to prevent multiple concurrent onboarding sessions
- **Updated Error Messages**: More descriptive error messages for better user guidance

### August 14, 2025
- **Removed Excel Dependencies**: Completely removed Excel file storage in favor of MySQL database
- **Enhanced Security**: All data now stored in a secure MySQL database with proper relationships
- **Improved Error Handling**: Better error handling and user feedback during onboarding
- **Updated Dependencies**: Removed unused packages (pandas, openpyxl) and added mysql-connector-python

### August 13, 2025
- **Database Integration**: Implemented MySQL database connection and schema
- **Data Migration**: Migrated all data storage from Excel files to MySQL database
- **Schema Design**: Created normalized database schema with proper relationships
  - `members` table for user information
  - `identity_info` table for sensitive identity data
  - Proper indexing and foreign key constraints
- **Environment Configuration**: Added database configuration to `.env` file

### August 5, 2025
- **Separate Identity Data Storage**: Implemented secure storage of sensitive identity information (ID, Passport, KRA) in a separate Excel file (`onboarding_data_identity.xlsx`)
- **Enhanced Security**: Improved data handling by isolating sensitive information from general user data
- **Updated Documentation**: Revised README to reflect new data storage structure and security measures

---

A Discord bot for managing member onboarding and status tracking for AAR Insurance. The bot collects member information and maintains their status in a secure MySQL database.

## Features

- Interactive onboarding process with guided conversation flow
- Unique entry code generation for each member
- Member status management (Active/Inactive)
- Secure MySQL database storage with proper relationships
- Real-time status updates and member lookup
- Duplicate message prevention
- Session management to prevent concurrent onboarding

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

### Database Schema

#### `members` Table
- `id`: Primary key
- `discord_id`: Discord user ID
- `entry_code`: Unique entry code
- `full_name`: Member's full name
- `email`: Contact email
- `phone`: Contact number
- `date_of_birth`: Date of birth
- `registration_date`: When the member registered
- `status`: Active/Inactive status
- `created_at`: Timestamp of record creation
- `updated_at`: Timestamp of last update

#### `identity_info` Table
- `id`: Primary key
- `member_id`: Foreign key to members table
- `id_number`: National ID
- `passport_number`: Passport number
- `kra_pin`: KRA PIN
- `created_at`: Timestamp of record creation
- `updated_at`: Timestamp of last update

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
- All sensitive data is stored in a secure MySQL database with proper access controls
- Database connections use parameterized queries to prevent SQL injection
- The bot only stores the data you provide during the onboarding process
- Regular database backups are recommended

## Future Improvements

### Data Management
- [x] Database Integration: Successfully migrated from Excel to MySQL database
- [ ] Data Encryption: Implement encryption for sensitive data at rest
- [ ] Backup System: Add automated backup functionality for the data files

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
