from os import path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES = [
    "https://www.googleapis.com/auth/gmail.readonly",
    "https://www.googleapis.com/auth/gmail.send",
    "https://www.googleapis.com/auth/gmail.modify",
    "https://www.googleapis.com/auth/gmail.compose",
    "https://mail.google.com/"
    ]

SETTINGS = {
    "token_file": "keys/token.json",
    "credentials_file": "keys/credentials.json"
}

def set_settings(token_file: str | None,
                 credentials_file: str | None) -> None:
    assert any([token_file, credentials_file]), "At least one setting must be provided"
    global SETTINGS
    if token_file:
        SETTINGS["token_file"] = token_file
    if credentials_file:
        SETTINGS["credentials_file"] = credentials_file
    return

def get_token():
    global SETTINGS
    credentials_file = SETTINGS["credentials_file"]
    token_file = SETTINGS["token_file"]

    creds = None
    if path.exists(token_file):
        creds = Credentials.from_authorized_user_file(token_file, SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                credentials_file, SCOPES
            )
            creds = flow.run_local_server(port=0)
        with open(token_file, "w") as token:
            token.write(creds.to_json())
    return creds
