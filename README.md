# 💾 SaveSnap

> A lightweight local version control and snapshot management system for students and beginner developers.

---

## 📌 What is SaveSnap?

SaveSnap is a beginner-friendly alternative to Git that allows users to save, manage, and restore snapshots of their project files using simple command-line commands. It works completely offline and stores all data locally — no internet required.

It also features **n8n cloud automation** that sends email notifications and logs every commit to Google Sheets automatically.

---

## 🚀 Features

- 📁 Initialize a local project repository
- 💾 Save snapshots (commits) of your files
- 📜 View full commit history
- ⏪ Restore previous versions easily
- 🔁 Undo a restore if needed
- 🎓 Education mode with interactive Google Colab notebooks
- 🔔 **n8n Automation:** Email notification on every commit
- 📊 **n8n Automation:** Auto-log commits to Google Sheets
- ☁️ Optional Firebase cloud sync

---

## 🛠️ Technology Stack

| Layer | Technology |
|---|---|
| Frontend | Command Line Interface (CLI) |
| Backend | Python |
| Database | Local File System |
| Automation | n8n (Webhook + Gmail + Google Sheets) |
| Cloud Sync | Firebase Firestore (Optional) |
| Platform | Windows / Linux / macOS |

---

## 📦 Installation

### 1. Clone the repository
```bash
git clone https://github.com/Rin871-tech/SAVESNAP.git
cd SAVESNAP
```

### 2. Create and activate virtual environment

**Mac/Linux:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

**Windows:**
```bash
python -m venv .venv
.venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install requests
```

### 4. (Optional) Install Firebase
```bash
pip install firebase-admin
```

---

## 💻 Commands

### Initialize a repository
```bash
python3 savesnap.py init
```
Sets up a new SaveSnap repository in the current folder. Asks for your name and email for commit notifications.

---

### Save a snapshot (commit)
```bash
python3 savesnap.py commit "your commit message"
```
Saves a snapshot of all files in the current directory. Automatically triggers email notification and Google Sheets log via n8n.

---

### View commit history
```bash
python3 savesnap.py log
```
Displays all previous commits with their IDs, timestamps, and messages.

---

### Restore a previous version
```bash
python3 savesnap.py checkout <commit_id>
```
Restores your files to a previous snapshot. Example:
```bash
python3 savesnap.py checkout 2026-04-19_14-48-35
```

---

### Undo a restore
```bash
python3 savesnap.py undo-checkout
```
Reverts back to the state before the last checkout.

---

### Education mode
```bash
python3 savesnap.py edu
```
Opens interactive Google Colab notebooks explaining version control concepts like init, commit, checkout, and more.

---

## 🤖 n8n Automation

SaveSnap integrates with **n8n** to automate notifications and logging every time a commit is made.

### How it works:
```
savesnap commit → Webhook → Gmail Notification
                          → Google Sheets Log
```

### What gets sent:
| Field | Description |
|---|---|
| Timestamp | When the commit was made |
| User Name | Name entered during init |
| User Email | Email entered during init |
| Commit ID | Unique commit identifier |
| Message | Commit message |
| Files | List of files saved |

### Setup:
1. Create an n8n account at [n8n.io](https://n8n.io)
2. Create a new workflow with a **Webhook** node
3. Add a **Gmail** node for email notifications
4. Add a **Google Sheets** node for logging
5. Copy your webhook URL and update `N8N_WEBHOOK_URL` in `savesnap.py`

---

## ☁️ Firebase Setup (Optional)

1. Create a Firebase project at [firebase.google.com](https://firebase.google.com)
2. Download your `firebase_key.json` credentials file
3. Place it in the root of your SaveSnap folder
4. Install firebase-admin: `pip install firebase-admin`
5. Run SaveSnap — commits will automatically sync to Firestore

---

## 📁 Project Structure

```
SaveSnap/
├── savesnap.py          # Main CLI script
├── firebase_key.json    # Firebase credentials (optional)
├── .savesnap/           # Repository folder (created on init)
│   ├── config.json      # User configuration (name, email)
│   ├── commit_log.txt   # Commit history
│   └── commits/         # Snapshot folders
│       └── commit_YYYY-MM-DD_HH-MM-SS/
│           ├── metadata.txt
│           └── (saved files)
└── README.md
```

---

## ⚠️ Show Stoppers / Limitations

- Risk of data loss if restore is used incorrectly
- Performance issues with very large files
- User errors in command usage
- Cross-platform file handling edge cases

---

## 🎓 Education Mode

SaveSnap includes an interactive education mode that opens Google Colab notebooks for learning version control concepts:

| Option | Topic |
|---|---|
| 1 | Initialization |
| 2 | Commit + Hashing |
| 3 | Checkout |
| 4 | Undo Checkout |
| 5 | Commit Logs |

---

## 👩‍💻 Author

**Vaishnavi Chavan**
Built as part of ISE-II Project

---

## 📄 License

This project is for educational purposes.
