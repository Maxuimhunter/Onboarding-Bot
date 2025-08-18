# Plan for File Storage Upgrade in Onboarding Bot

## Notes
- User wants uploaded files stored directly in the database (BLOB), not just file paths.
- The current schema only stores file paths; must be updated to store file binary data.
- The database schema and save logic have been updated to support file BLOB storage.
- The bot is running and can be tested after code changes.

## Task List
- [x] Diagnose current file upload and storage flow
- [x] Update database schema to add file BLOB storage
- [ ] Update file upload handler to save file data in DB
- [x] Update save logic to store/retrieve files from DB
- [x] Add file retrieval (download) endpoint/command
- [ ] Test onboarding and file upload/download end-to-end

## Current Goal
Update file upload handler to save file data in DB