import smtplib, ssl
from email.mime.text import MIMEText

import sys
import os
import dotenv
dotenv.load_dotenv()

import base64

from googleapiclient.discovery import build

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from oauth import get_token

SENDER_ADDRESS = os.getenv("SENDER_ADDRESS")
SENDER_PASSWORD = os.getenv("SENDER_PASSWORD")

assert SENDER_ADDRESS is not None, "SENDER_ADDRESS env var is not set"
assert SENDER_PASSWORD is not None, "SENDER_PASSWORD env var is not set"

address = SENDER_ADDRESS
password = SENDER_PASSWORD

receiver_address = "mariano29878@gmail.com"

subject = "Hello World!"
body = "This message is sent from Python."

creds = get_token()
service = build("gmail", "v1", credentials=creds)

def create_message(sender, receiver, subject, body):
    message = MIMEText(body)
    message["to"] = receiver
    message["from"] = sender
    message["subject"] = subject
    return {"raw": base64.urlsafe_b64encode(message.as_bytes()).decode()}

message = create_message(
    sender=address,
    receiver=receiver_address,
    subject=subject,
    body=body
)

draft = service.users().drafts().create(
    userId="me",
    body={
        "message": message
    }
)
created_draft = draft.execute()

email = service.users().drafts().send(
    userId="me",
    body={
        "id": created_draft["id"]
    }
)
sent_email = email.execute()

print("Debug stopper!")
