# Search Files Feature - Root Cause Analysis

## Problem Summary
When user clicks "🔎 Search Files" and enters a keyword (e.g., "ssh"), the bot does not respond. The message is silently ignored.

## Root Cause: Missing Message Handler Chain

### The Flow (Expected):
1. User clicks "🔎 Search Files" button
2. `data == "search_files"` callback sets `SEARCH_MODE[uid] = True`
3. User sends text message "ssh"
4. Message handler checks `if SEARCH_MODE.get(user_id)` and processes search
5. Bot returns matching files

### What Actually Happens (Broken):
1. ✅ User clicks "🔎 Search Files" → callback works, sets `SEARCH_MODE[uid] = True`
2. ✅ User sends text message "ssh"
3. ❌ **Message enters `handle_message()` BUT the handler is registered AFTER `CallbackQueryHandler`**
4. ❌ The `MessageHandler` has no state filter - it catches ALL text messages
5. ❌ However, **other ConversationHandlers (addfile, listfiles, etc.) are registered FIRST**
6. ❌ These ConversationHandlers consume the message with their own filters
7. ❌ The generic `handle_message()` never gets called because the conversation handler intercepts it

### Critical Issue in bot.py (line ~550):

```python
app.add_handler(listfiles_handler)      # ← These are ConversationHandlers
app.add_handler(deletefile_handler)     # ← They have their own state filters
app.add_handler(addfile_handler)        # ← They consume messages
app.add_handler(testfile_handler)
app.add_handler(backupdb_handler)
app.add_handler(restoredb_handler)
app.add_handler(applyrestore_handler)
app.add_handler(filestats_handler)
app.add_handler(adminpanel_handler)

app.add_handler(CallbackQueryHandler(buttons))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
# ↑ By the time this runs, the ConversationHandlers have already matched/consumed the message
```

## Secondary Issue: Database Query Problem

In `handle_message()` (bot.py line ~450):

```python
cur.execute(
    "SELECT name, file_id FROM files WHERE LOWER(name) LIKE ?",
    (f"%{text}%",)
)
```

**Problem**: The `files` table has NO `name` column. Looking at `database.py` line ~22:

```python
CREATE TABLE IF NOT EXISTS files(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    category TEXT,        # ← Actual column (not "name")
    size TEXT,
    file_id TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
```

The query should search `category`, NOT `name`. This will cause an SQL error: `OperationalError: no such column: name`

## Tertiary Issue: Missing Search Function in files.py

There is NO `search_files()` function in `services/files.py`. The search logic is hardcoded into `handle_message()` in bot.py, which violates separation of concerns.

---

## Solutions Required

### Fix 1: Add search_files() function to files.py
Create a proper search function that queries the correct column.

### Fix 2: Correct the SQL column name in bot.py
Change `SELECT name, file_id` to `SELECT category, file_id`

### Fix 3: Fix handler registration order
Move `handle_message()` MessageHandler BEFORE the ConversationHandlers, or wrap search in a ConversationHandler to guarantee it runs.

### Fix 4: Send matching files as documents
After search, the bot should send the actual Telegram documents using `file_id`, not just list file names.

---

## Files Affected
- `bot.py` (handle_message function, handler registration order)
- `services/files.py` (missing search_files function)
- Potentially `commands/` (if creating a proper ConversationHandler wrapper)
