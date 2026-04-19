import os
import sys
import shutil
import hashlib
import webbrowser
import requests
import json
from datetime import datetime

# -------- n8n Webhook URL --------
N8N_WEBHOOK_URL = "https://vaishnavichavan.app.n8n.cloud/webhook-test/86284942-9c9f-4836-b475-2fd0662c7711"

def trigger_n8n(event, data):
    try:
        payload = {
            "event": event,
            "timestamp": datetime.now().isoformat(),
            **data
        }
        requests.post(N8N_WEBHOOK_URL, json=payload, timeout=5)
        print("n8n automation triggered successfully.")
    except Exception as e:
        print(f"n8n trigger failed (offline?): {e}")

# -------- Firebase Setup (Optional) --------
firebase_enabled = False
try:
    import firebase_admin
    from firebase_admin import credentials, firestore

    if os.path.exists("firebase_key.json"):
        cred = credentials.Certificate("firebase_key.json")
        firebase_admin.initialize_app(cred)
        db = firestore.client()
        firebase_enabled = True
        print("Firebase connected successfully.")
    else:
        print("firebase_key.json not found. Running in offline mode.")
except Exception as e:
    print("Firebase not available:", e)
    firebase_enabled = False

# ------------------- EDUCATION MODE -------------------

def education_mode():
    while True:
        print("-------------------Educational Mode-------------------")
        print("1. init --- Initialization of repository")
        print("2. commit --- commit+hashing")
        print("3. checkout --- Checkout process")
        print("4. undo-checkout --- Undo Checkout")
        print("5. log --- Commit Logs")
        print("0. Exit")

        try:
            choice = int(input("Enter your choice : "))
        except ValueError:
            print("Please enter a number.")
            continue

        match choice:
            case 1:
                webbrowser.open('https://colab.research.google.com/drive/1lZbSa9P5UNq2tAZEyibrduXhcKrvA7zr')
            case 2:
                webbrowser.open('https://colab.research.google.com/drive/1qQc-7of7ecQ2jTD1j-kB_3i4NfXUmyQu')
            case 3:
                webbrowser.open('https://colab.research.google.com/drive/1zTVtdyLFdhpE6ib0LCQ4ZmWFKJBDhgj1')
            case 4:
                webbrowser.open('https://colab.research.google.com/drive/1zTVtdyLFdhpE6ib0LCQ4ZmWFKJBDhgj1')
            case 5:
                webbrowser.open('https://colab.research.google.com/drive/15vf06o9cw4sAZJObZ5bhH3gJ-wIJy_oz')
            case 0:
                print('Exiting Education Mode......')
                break
            case _:
                print("Invalid Choice ")

# -----------------Global Configuration-------------------

repo_folder = '.savesnap'
commits_folder = os.path.join(repo_folder, 'commits')
backup_folder = os.path.join(repo_folder, ".checkout_backup")
log_file = os.path.join(repo_folder, 'commit_log.txt')

# --------Initializing a repository---------

def init_repo():
    if os.path.exists(repo_folder):
        print('Repository already exists')
        return

    os.makedirs(commits_folder)
    with open(log_file, 'w') as f:
        f.write("SaveSnap Commit Log \n")

    # Ask user for name and email
    print("\nSaveSnap Setup")
    user_name = input("Enter your name: ").strip()
    user_email = input("Enter your email (for commit notifications): ").strip()

    # Save user config
    config = {"name": user_name, "email": user_email}
    config_path = os.path.join(repo_folder, "config.json")
    with open(config_path, "w") as f:
        json.dump(config, f)

    print(f"\nSaveSnap repository created successfully!")
    print(f"Notifications will be sent to: {user_email}")

    # Trigger n8n
    trigger_n8n("init", {
        "user_name": user_name,
        "user_email": user_email,
        "message": "SaveSnap repository initialized",
        "project_path": os.getcwd()
    })

def get_user_config():
    config_path = os.path.join(repo_folder, "config.json")
    if os.path.exists(config_path):
        with open(config_path, "r") as f:
            return json.load(f)
    return {"name": "Developer", "email": ""}

# -------------------Hashing-----------------

def calculate_hash(file_path):
    hasher = hashlib.sha256()
    with open(file_path, 'rb') as f:
        while chunk := f.read(8192):
            hasher.update(chunk)
    return hasher.hexdigest()

# -------------create commits-------------

def create_commits(message):
    if not os.path.exists(repo_folder):
        print("Repository not initialized. Run init first.")
        return

    commit_id = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    commit_folder = os.path.join(commits_folder, f'commit_{commit_id}')
    os.makedirs(commit_folder)

    metadata_path = os.path.join(commit_folder, 'metadata.txt')
    files = []

    with open(metadata_path, 'w') as meta:
        meta.write('File MetaData (SHA-256 hashes) \n\n')
        for file in os.listdir():
            if file.startswith('.') or not os.path.isfile(file):
                continue
            file_hash = calculate_hash(file)
            shutil.copy(file, commit_folder)
            meta.write(f'{file} : {file_hash}\n')
            files.append(file)

    with open(log_file, 'a') as f:
        f.write(f'\n Commit ID : {commit_id}\n')
        f.write(f'Time : {datetime.now()}\n')
        f.write(f'Message : {message}\n')

    # -------- Push to Firebase --------
    if firebase_enabled:
        try:
            db.collection("savesnap_commits").add({
                "commit_id": commit_id,
                "message": message,
                "time": datetime.now().isoformat(),
                "files": files
            })
            print("Commit synced to Firebase.")
        except Exception as e:
            print("Firebase sync failed:", e)

    # -------- Trigger n8n --------
    config = get_user_config()
    trigger_n8n("commit", {
        "commit_id": commit_id,
        "message": message,
        "files": files,
        "file_count": len(files),
        "project_path": os.getcwd(),
        "user_name": config["name"],
        "user_email": config["email"]
    })

    print(f'Commit {commit_id} created successfully')

# ------------Show logs------------------

def show_log():
    if not os.path.exists(log_file):
        print('No commit history available')
        return
    with open(log_file, 'r') as f:
        print(f.read())

# ---------------Checkout-----------------

def checkout(commit_id):
    commit_folder = os.path.join(commits_folder, f'commit_{commit_id}')

    if not os.path.exists(commit_folder):
        print('Commit not found')
        return

    if os.path.exists(backup_folder):
        shutil.rmtree(backup_folder)
    os.makedirs(backup_folder)

    for file in os.listdir():
        if file.startswith('.') or not os.path.isfile(file):
            continue
        shutil.copy(file, backup_folder)

    for file in os.listdir(commit_folder):
        if file == 'metadata.txt':
            continue
        shutil.copy(os.path.join(commit_folder, file), file)

    # Trigger n8n
    trigger_n8n("checkout", {
        "commit_id": commit_id,
        "message": f"Restored to commit {commit_id}",
        "project_path": os.getcwd()
    })

    print(f'Checked out commit {commit_id} successfully')

# ----------------Undo Checkout------------

def undo_checkout():
    if not os.path.exists(backup_folder):
        print("No checkout to undo.")
        return

    for file in os.listdir(backup_folder):
        shutil.copy(os.path.join(backup_folder, file), file)

    shutil.rmtree(backup_folder)

    # Trigger n8n
    trigger_n8n("undo-checkout", {
        "message": "Checkout undone successfully",
        "project_path": os.getcwd()
    })

    print("Checkout undone.")

# ----------------Main CLI-----------------

def main():
    if len(sys.argv) < 2:
        print('Usage : ')
        print(' python savesnap.py init')
        print(" python savesnap.py commit \"message\"")
        print(" python savesnap.py log")
        print(' python savesnap.py checkout <commit_id>')
        print(' python savesnap.py undo-checkout')
        print(" python savesnap.py edu\n")
        return

    command = sys.argv[1]

    if command == 'init':
        init_repo()
    elif command == 'commit':
        if len(sys.argv) < 3:
            print('Commit message required')
            return
        create_commits(sys.argv[2])
    elif command == 'log':
        show_log()
    elif command == 'checkout':
        checkout(sys.argv[2])
    elif command == 'undo-checkout':
        undo_checkout()
    elif command == 'edu':
        education_mode()
    else:
        print('Unknown command')

if __name__ == '__main__':
    main()