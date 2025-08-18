# Discord Onboarding Bot Excel & File Upload Plan

## Notes
- User reported Excel not saving onboarding data; fixed by always appending new entries and ensuring robust file handling.
- Fixed duplicate message issue by updating event handler logic.
- User requested an option for onboarding users to optionally upload a file (e.g., PDF).
- Bot is confirmed running with previous fixes; now needs file upload enhancement.
- User requested ID/Passport logic: ask for ID (5-9 digits), if not available, ask for Passport (2 letters + 5 numbers); must validate formats.
- User requested KRA number prompt: alphanumeric, 11 digits.
- User requested a new Excel sheet to store ID/Passport/KRA numbers linked by Entry Code, and that the KRA prompt should be asked separately.
- Fixed onboarding flow bug: resolved ID/Passport prompt loop.
- Fixed bug where ID, Passport, and KRA numbers were not being saved due to awaiting_input logic; added targeted state transitions after each input.
- Fixed syntax/indentation error in KRA prompt handling.

## Task List
- [x] Diagnose and fix Excel saving bug
- [x] Fix duplicate onboarding completion messages
- [x] Restart bot and verify Excel saving
- [ ] Implement optional file upload step in onboarding
- [ ] Test onboarding with and without file upload
- [x] Add ID/Passport and KRA number questions with validation to onboarding
- [ ] Test onboarding with new ID/Passport and KRA logic
- [x] Create a new Excel sheet for ID/Passport/KRA numbers linked by Entry Code
- [x] Test new Excel sheet linkage and data integrity

## Current Goal
Test onboarding with and without file upload