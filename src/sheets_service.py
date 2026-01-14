from googleapiclient.discovery import build


def append_to_sheet(creds, spreadsheet_id, rows):
    service = build("sheets", "v4", credentials=creds)

    body = {
        "values": rows
    }

    service.spreadsheets().values().append(
        spreadsheetId=spreadsheet_id,
        range="Sheet1!A:D",
        valueInputOption="RAW",
        body=body
    ).execute()
