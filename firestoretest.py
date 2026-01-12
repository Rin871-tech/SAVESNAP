import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime
import uuid

# Initialize Firebase
cred = credentials.Certificate("firebase_key.json")
firebase_admin.initialize_app(cred)

db = firestore.client()

# Generate commit data
commit_id = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

commit_data = {
    "commit_id": commit_id,
    "author": "vaish",
    "message": "Commit from VS Code",
    "files": [
        "savesnap.py",
        "test.txt"
    ],
    "stats": {
        "files_added": 1,
        "files_modified": 1,
        "files_deleted": 0
    },
    "platform": "VS Code",
    "mode": "cloud",
    "status": "success",
    "time": datetime.utcnow().isoformat()
}

# Save to Firestore
doc_ref = db.collection("savesnap_commits").document(str(uuid.uuid4()))
doc_ref.set(commit_data)

print("✅ Commit successfully saved to Firestore!")
