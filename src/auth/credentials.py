import os
import pickle
import logging
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from typing import Optional
from google.oauth2.credentials import Credentials

class SetAuth:
    SCOPES = [
        'https://www.googleapis.com/auth/youtube.readonly',
        'https://www.googleapis.com/auth/yt-analytics.readonly',
        'https://www.googleapis.com/auth/documents'  # Add Google Docs scope
    ]

    def __init__(self, credentials_path: str = 'credentials.json'):
        """Initialize auth manager with credentials path."""
        self.credentials_path = credentials_path
        self.token_path = os.path.join(os.path.dirname(credentials_path), 'token.pickle')
        self._setup_logging()

    def get_credentials(self) -> Optional[Credentials]:
        """Get valid credentials, refreshing or creating new ones if needed."""
        creds = self._load_existing_credentials()
        
        if not creds or not creds.valid:
            creds = self._refresh_or_create_credentials(creds)
            
        return creds

    def _load_existing_credentials(self) -> Optional[Credentials]:
        """Load credentials from pickle file if exists."""
        if not os.path.exists(self.token_path):
            return None

        try:
            with open(self.token_path, 'rb') as token:
                return pickle.load(token)
        except Exception as e:
            logging.error(f"Error loading credentials: {e}")
            return None

    def _refresh_or_create_credentials(self, creds: Optional[Credentials]) -> Optional[Credentials]:
        """Refresh existing credentials or create new ones."""
        if creds and creds.expired and creds.refresh_token:
            try:
                creds.refresh(Request())
                logging.info("Credentials refreshed successfully")
            except Exception as e:
                logging.error(f"Error refreshing credentials: {e}")
                creds = None

        if not creds:
            creds = self._create_new_credentials()

        if creds:
            self._save_credentials(creds)
            
        return creds

    def _create_new_credentials(self) -> Optional[Credentials]:
        """Create new credentials via OAuth2 flow."""
        try:
            flow = InstalledAppFlow.from_client_secrets_file(
                self.credentials_path, self.SCOPES)
            creds = flow.run_local_server(port=0)
            logging.info("New credentials created successfully")
            return creds
        except Exception as e:
            logging.error(f"Error creating credentials: {e}")
            return None

    def _save_credentials(self, creds: Credentials) -> None:
        """Save credentials to pickle file."""
        try:
            with open(self.token_path, 'wb') as token:
                pickle.dump(creds, token)
            logging.info(f"Credentials saved to {self.token_path}")
        except Exception as e:
            logging.error(f"Error saving credentials: {e}")

    def _setup_logging(self) -> None:
        """Configure logging."""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )