from googleapiclient.discovery import build


def append_to_sheet(creds, spreadsheet_id, rows):
    service = build("sheets", "v4", credentials=creds)

    body = {
        "values": rows
    }

    result = service.spreadsheets().values().append(
        spreadsheetId=spreadsheet_id,
        range="New Logs!A2:D",
        valueInputOption="RAW",
        insertDataOption="INSERT_ROWS",
        body=body
    ).execute()

    print(f"✅ Rows appended to sheet: {result.get('updates', {}).get('updatedRows', 0)}")
