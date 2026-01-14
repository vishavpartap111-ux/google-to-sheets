import base64
from bs4 import BeautifulSoup


def extract_email_data(message):
    headers = message["payload"]["headers"]

    sender = ""
    subject = ""
    date = ""

    # Extract headers
    for header in headers:
        if header["name"] == "From":
            sender = header["value"]
        elif header["name"] == "Subject":
            subject = header["value"]
        elif header["name"] == "Date":
            date = header["value"]

    body = ""
    payload = message["payload"]

    # Handle multipart emails
    if "parts" in payload:
        for part in payload["parts"]:
            if part["mimeType"] == "text/plain":
                data = part["body"].get("data")
                if data:
                    body = base64.urlsafe_b64decode(data).decode("utf-8", errors="ignore")
                    return sender, subject, date, body.strip()

            elif part["mimeType"] == "text/html":
                data = part["body"].get("data")
                if data:
                    html = base64.urlsafe_b64decode(data).decode("utf-8", errors="ignore")
                    body = BeautifulSoup(html, "html.parser").get_text()
                    return sender, subject, date, body.strip()

    # Fallback if no parts
    data = payload["body"].get("data")
    if data:
        body = base64.urlsafe_b64decode(data).decode("utf-8", errors="ignore")

    return sender, subject, date, body.strip()
