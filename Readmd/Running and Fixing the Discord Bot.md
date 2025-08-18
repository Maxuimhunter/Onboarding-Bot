# Plan: Running and Fixing the Discord Bot

## Notes
- User encountered a Python syntax error: "Try statement must have at least one except or finally clause" in `database.py` (line 191).
- The error was due to an incorrectly indented try block in `save_member`; this was fixed by properly nesting the code and ensuring an except block exists.
- The bot is run from `bot.py`, which requires environment variables and several Python dependencies listed in `requirements.txt`.
- The `.env` file has all necessary tokens and database credentials.
- The NumPy/pandas incompatibility has been resolved by installing compatible versions for Python 3.12.
- The bot is running, but onboarding messages (passport validation, file upload, etc.) are duplicating due to a bug in the message handling flow.
- The duplicate onboarding message bug has been fixed.
- Excel-related imports and code are being removed; only DB storage will remain.

## Task List
- [x] Diagnose and fix the try/except/finally bug in `save_member` method
- [x] Inspect `bot.py` to confirm how to run the bot
- [x] Verify required environment variables in `.env`
- [x] Locate and review `requirements.txt` for dependencies
- [x] Install Python dependencies from `requirements.txt`
- [x] Resolve NumPy/pandas incompatibility error
- [x] Run the Discord bot script
- [x] Diagnose and fix duplicate onboarding messages/responses bug
- [ ] Remove Excel export functionality, keep only DB storage (in progress)

## Current Goal
Remove Excel export functionality and keep only DB storage