# Discord Bot Onboarding Data Storage Upgrade

## Notes
- User wants onboarding data stored in both Excel and a local MySQL database (phpMyAdmin on localhost).
- The database and required tables need to be created if not already present.
- The .env file currently lacks MySQL connection configuration.
- Excel export functionality must remain intact.

## Task List
- [ ] Create new MySQL database and tables for onboarding data
- [ ] Add MySQL connection configuration to .env
- [ ] Create a Python database utility/module for MySQL operations
- [ ] Modify the bot code to save onboarding data to both Excel and MySQL
- [ ] Test the implementation to ensure both storage methods work

## Current Goal
Create MySQL database and tables