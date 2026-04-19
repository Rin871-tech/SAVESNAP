import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime
import uuid
import time

# Initialize Firebase (run once)
cred = credentials.Certificate("firebase_key.json")
firebase_admin.initialize_app(cred)

db = firestore.client()

# Sample commit messages
messages = [
    "Initial SaveSnap CLI setup",
    "Added Firebase Firestore support",
    "Fixed CLI argument bug",
    "Added test files",
    "Cloud sync validation commit",
    "Edu mode preparation"
]

files_list = [
    ["savesnap.py"],
    ["firebase_key.json", "savesnap.py"],
    ["savesnap.py"],
    ["test.txt", "sample.json"],
    ["savesnap.py", "test.txt"],
    ["colab_demo.ipynb"]
]

for i in range(len(messages)):
    commit_id = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    commit_data = {
        "commit_id": commit_id,
        "author": "vaish",
        "message": messages[i],
        "files": files_list[i],
        "stats": {
            "files_added": len(files_list[i]),
            "files_modified": i,
            "files_deleted": 0
        },
        "platform": "VS Code",
        "mode": "cloud",
        "status": "success",
        "time": datetime.utcnow().isoformat()
    }

    db.collection("savesnap_commits").document(str(uuid.uuid4())).set(commit_data)
    print(f"✅ Commit {i+1} saved")

    time.sleep(1)  # ensures unique timestamps
