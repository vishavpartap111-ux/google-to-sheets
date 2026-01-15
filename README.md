# 📧 Gmail to Google Sheets Automation

A Python automation project that reads emails from Gmail and automatically stores structured data into Google Sheets using Google APIs.

Built to simplify manual data entry and improve productivity.

---

## 👨‍💻 Author
**Vishav Partap Singh**

---

## 📌 Features
- Connects securely to Gmail using Google API  
- Reads and filters emails automatically  
- Extracts useful information from emails  
- Saves data directly into Google Sheets  
- Avoids duplicate entries using processed IDs  
- Fully automated workflow  

---

## 🛠️ Technologies Used
- Python  
- Google Gmail API  
- Google Sheets API  
- OAuth 2.0 Authentication  
- VS Code  

---

## 📂 Project Structure
google-to-sheet/
│── src/
│ ├── main.py
│ ├── gmail_service.py
│ ├── sheets_service.py
│ └── config.py
│── processed_ids.txt
│── requirements.txt
│── README.md

---

## ⚙️ How to Run This Project

### 1️⃣ Install dependencies
```bash
pip install -r requirements.txt
python main.py
🔐 Setup Required

To use this project, you must:

Enable Gmail API and Google Sheets API in Google Cloud Console

Create OAuth credentials

Download credentials.json

Login once to allow access

🎯 Use Case

This project is useful for:

Automating email data collection

Storing leads automatically

Managing applications

Organizing reports

Reducing manual copy-paste work

📈 Future Improvements

Add GUI interface

Deploy as a web app

Add database support

Improve email parsing with AI

⭐ If you like this project

Give it a star on GitHub and feel free to fork it!
