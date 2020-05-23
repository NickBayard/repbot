import base64
import pickle

from pathlib import Path
from email.message import EmailMessage

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from apiclient import errors

from lib.utils import build_logger
from lib.errors import GmailError


class Gmail:
    SCOPES = ['https://www.googleapis.com/auth/gmail.send']

    def __init__(self, notification, creds_file, ptoken):
        self.notification = notification
        self.creds_file = creds_file
        self.ptoken = Path(ptoken)
        self._service = None
        self.log = build_logger('repbot.gmail')

    @property
    def service(self):
        if self._service is None:
            self._service = self.get_service()
        return self._service

    def get_service(self):
        creds = None
        # The file token.pickle stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if self.ptoken.exists():
            with self.ptoken.open('rb') as token:
                creds = pickle.load(token)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.creds_file, self.SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with self.ptoken.open('wb') as token:
                pickle.dump(creds, token)

        return build('gmail', 'v1', credentials=creds)

    def send(self, subject, message_text):
        for recipient in self.notification.emails:
            body = self.create_message_body(sender=self.notification.api_account,
                                            recipient=recipient,
                                            subject=subject,
                                            message_text=message_text)
            try:
                self.service.users().messages().send(userId='me', body=body).execute()
                self.log.debug(f'Sent email to {recipient}')
            except errors.HttpError as error:
                self.log.error(f'An error occurred: {repr(error)}')
                raise GmailError(f'Failed to send email to {recipient}') from error

    @staticmethod
    def create_message_body(sender, recipient, subject, message_text):
        message = EmailMessage()
        message.set_content(message_text)
        message['Subject'] = subject
        message['To'] = recipient
        message['From'] = sender
        encoded_msg = base64.urlsafe_b64encode(message.as_bytes())
        raw = encoded_msg.decode('utf-8')
        return dict(raw=raw)
