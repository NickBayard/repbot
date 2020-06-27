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
        self._credentials = None
        self.log = build_logger('repbot.gmail')

    @property
    def service(self):
        if self._service is None:
            self._service = build('gmail', 'v1', credentials=self.credentials)
        return self._service

    @property
    def credentials(self):
        if self._credentials is None:
            # The file token.pickle stores the user's access and refresh tokens, and is
            # created automatically when the authorization flow completes for the first
            # time.
            if self.ptoken.exists():
                with self.ptoken.open('rb') as token:
                    self._credentials = pickle.load(token)

        # If there are no (valid) credentials available, let the user log in.
        if not self._credentials.valid:
            try:
                if self._credentials.expired and self._credentials.refresh_token:
                    self._credentials.refresh(Request())
                else:
                    flow = InstalledAppFlow.from_client_secrets_file(
                        self.creds_file, self.SCOPES)
                    self._credentials = flow.run_local_server(port=0)
            except Exception as ex:
                raise GmailError('Failed to get google api token') from ex

            # Save the credentials for the next run
            with self.ptoken.open('wb') as token:
                pickle.dump(self._credentials, token)

        return self._credentials

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
