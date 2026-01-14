import config
from src.gmail_service import get_gmail_service
from src.email_parser import extract_email_data
from src.sheets_service import append_to_sheet


def load_state():
    try:
        with open(config.STATE_FILE, "r") as f:
            return f.read().strip()
    except:
        return None


def save_state(message_id):
    with open(config.STATE_FILE, "w") as f:
        f.write(message_id)


def main():
    gmail_service, creds = get_gmail_service()

    last_processed_id = load_state()

    results = gmail_service.users().messages().list(
        userId="me",
        labelIds=["INBOX", "UNREAD"],
        maxResults=20
    ).execute()

    messages = results.get("messages", [])

    if not messages:
        print("No unread emails.")
        return

    rows = []

    for msg in messages:
        if msg["id"] == last_processed_id:
            break

        full_msg = gmail_service.users().messages().get(
            userId="me",
            id=msg["id"],
            format="full"
        ).execute()

        rows.append(list(extract_email_data(full_msg)))

        gmail_service.users().messages().modify(
            userId="me",
            id=msg["id"],
            body={"removeLabelIds": ["UNREAD"]}
        ).execute()

    if rows:
        append_to_sheet(creds, config.SPREADSHEET_ID, rows)
        save_state(messages[0]["id"])
        print(f"{len(rows)} emails added to sheet.")
    else:
        print("No new emails to add.")


if __name__ == "__main__":
    main()
