import smtplib, ssl
from email.mime.text import MIMEText

import os
import dotenv
dotenv.load_dotenv()

import base64

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

SENDER_ADDRESS = os.getenv("SENDER_ADDRESS")
SENDER_PASSWORD = os.getenv("SENDER_PASSWORD")

assert SENDER_ADDRESS is not None, "SENDER_ADDRESS env var is not set"
assert SENDER_PASSWORD is not None, "SENDER_PASSWORD env var is not set"

SCOPES = [
    "https://www.googleapis.com/auth/gmail.readonly",
    "https://www.googleapis.com/auth/gmail.send"
    ]

port = 465

address = SENDER_ADDRESS
password = SENDER_PASSWORD

receiver_address = "mariano29878@gmail.com"

subject = "Hello World!"
body = "This message is sent from Python."

# context = ssl.create_default_context()

# with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
#     server.login(address, password)
#     server.sendmail(from_addr= address,
#                     to_addrs= receiver_address,
#                     msg= message,
#                     )

# For now, we assume the credentials exist on credentials.json
creds = Credentials.from_authorized_user_file("token.json", SCOPES)

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

# print(draft)

print(created_draft)
print(type(created_draft))

# # Print methods and attributes of draft object
# print(dir(draft))

# print(f"{draft.body=}")
# print(f"{draft.headers=}")
# print(f"{draft.uri=}")

# print(draft.to_json())
# print(dict(draft.to_json()))

email = service.users().drafts().send(
    userId="me",
    body={
        "id": created_draft["id"]
    }
)
sent_email = email.execute()

print("Debug stopper!")
