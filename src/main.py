import os
import config
from datetime import datetime
from src.gmail_service import get_gmail_service
from src.email_parser import extract_email_data
from src.sheets_service import append_to_sheet


# --- Ensure processed_ids.txt is always created in project root ---
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATE_FILE = os.path.join(BASE_DIR, "processed_ids.txt")


def log(msg):
    print(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}")


def load_processed_ids():
    try:
        with open(STATE_FILE, "r", encoding="utf-8") as f:
            return set(line.strip() for line in f.readlines())
    except FileNotFoundError:
        return set()


def save_processed_id(msg_id):
    with open(STATE_FILE, "a", encoding="utf-8") as f:
        f.write(msg_id + "\n")


def main():
    log("Starting Gmail → Sheets automation")

    gmail_service, creds = get_gmail_service()

    processed = load_processed_ids()
    log(f"Already processed emails: {len(processed)}")

    # Fetch latest emails
    results = gmail_service.users().messages().list(
        userId="me",
        labelIds=["INBOX"],
        maxResults=20
    ).execute()

    messages = results.get("messages", [])
    log(f"Fetched {len(messages)} recent emails")

    if not messages:
        log("No emails found")
        return

    rows = []
    new_count = 0

    for msg in messages:
        if msg["id"] in processed:
            continue

        # Get full email
        full_msg = gmail_service.users().messages().get(
            userId="me",
            id=msg["id"],
            format="full"
        ).execute()

        sender, subject, date, body = extract_email_data(full_msg)

        # Add to rows for Sheets
        rows.append([sender, subject, date, body])

        # ✅ Mark email as READ (remove UNREAD label)
        gmail_service.users().messages().modify(
            userId="me",
            id=msg["id"],
            body={"removeLabelIds": ["UNREAD"]}
        ).execute()

        # Save ID so it won't be processed again
        save_processed_id(msg["id"])
        new_count += 1

    if rows:
        append_to_sheet(creds, config.SPREADSHEET_ID, rows)
        log(f"{new_count} new emails added to sheet")
    else:
        log("No new emails to add")

    log("Run completed")


if __name__ == "__main__":
    main()
