# Onboarding Bot Excel Data Storage Update

## Notes
- Identity data (ID, Passport, KRA) is now stored in a separate Excel file (`onboarding_data_identity.xlsx`) instead of a separate sheet.
- The identity data file uses the user's full name as the primary identifier, not the entry code.
- The onboarding process and main data storage in `onboarding_data.xlsx` remain unchanged for non-sensitive info.
- README.md was updated to document these changes and add an update history section.

## Task List
- [x] Diagnose and fix entry code issue in identity data saving
- [x] Change identity data storage to use user name, not entry code
- [x] Store identity data in a separate Excel file, not a sheet
- [x] Update README.md to reflect new data storage and add update history
- [x] Restart and test bot after changes
- [ ] Monitor for further user requests or improvements

## Current Goal
Monitor for further user requests or improvements.