# Backup Infrastructure Approach

## Goal
Provide a simple backup plan while the app is still using local JSON storage.

## Proposed Approach
- Keep `data/bookstore_data.json` as the primary live file
- Create timestamped copies in `data/backups/`
- Run a backup before major write operations or on app shutdown
- Retain the most recent 7 backup files locally

## Recovery
- Select the latest healthy file from `data/backups/`
- Replace `data/bookstore_data.json` with the backup
- Restart the app and verify inventory, customers, and orders

## Future Upgrade Path
- Move persistence from JSON to SQLite
- Add scheduled automatic backups
- Add restore controls to an admin-only settings screen
- Log backup success and failure events for review
