"""
Google Sheets Service Module.
Handles all interactions with Google Sheets API using gspread.
"""
import os
from datetime import datetime
from typing import List, Dict, Optional, Tuple
import gspread
from google.oauth2.service_account import Credentials
from google.auth.exceptions import GoogleAuthError

import config


class SheetsService:
    """Service class for Google Sheets operations."""

    def __init__(self):
        """Initialize the Sheets service with credentials."""
        self.gc = None
        self.spreadsheet = None
        self.worksheet = None
        self._authenticate()
        self._open_spreadsheet()

    def _authenticate(self) -> None:
        """
        Authenticate using Service Account credentials.
        
        Raises:
            GoogleAuthError: If authentication fails
        """
        try:
            if not os.path.exists(config.CREDENTIALS_FILE):
                raise FileNotFoundError(
                    f"Credentials file '{config.CREDENTIALS_FILE}' not found. "
                    "Please download from Google Cloud Console."
                )

            scopes = [
                'https://www.googleapis.com/auth/spreadsheets',
                'https://www.googleapis.com/auth/drive'
            ]

            credentials = Credentials.from_service_account_file(
                config.CREDENTIALS_FILE,
                scopes=scopes
            )

            self.gc = gspread.authorize(credentials)

        except GoogleAuthError as e:
            print(f"Google Auth Error: {e}")
            raise
        except Exception as e:
            print(f"Authentication Error: {e}")
            raise

    def _open_spreadsheet(self) -> None:
        """Open the Google Sheet by name."""
        try:
            self.spreadsheet = self.gc.open(config.GOOGLE_SHEET_NAME)
            self.worksheet = self.spreadsheet.sheet1

            headers = self.worksheet.row_values(1)
            if not headers or headers != config.SHEET_HEADERS:
                self.worksheet.update('A1', [config.SHEET_HEADERS])

        except gspread.SpreadsheetNotFound:
            print(f"Spreadsheet '{config.GOOGLE_SHEET_NAME}' not found.")
            raise
        except Exception as e:
            print(f"Error opening spreadsheet: {e}")
            raise

    def add_transaction(
        self,
        transaction_type: str,
        amount: int,
        description: str,
        user_name: str
    ) -> bool:
        """
        Add a new transaction to the sheet.
        
        Args:
            transaction_type: 'Income' or 'Expense'
            amount: Transaction amount
            description: Transaction description
            user_name: Discord username
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            row = [
                timestamp,
                user_name,
                transaction_type,
                amount,
                description
            ]

            self.worksheet.append_row(row)
            return True

        except Exception as e:
            print(f"Error adding transaction: {e}")
            return False

    def get_all_transactions(self) -> List[Dict]:
        """
        Get all transactions from the sheet.
        
        Returns:
            List of dictionaries containing transaction data
        """
        try:
            data = self.worksheet.get_all_records()
            return data if data else []

        except Exception as e:
            print(f"Error getting transactions: {e}")
            return []

    def get_monthly_transactions(self, year: int, month: int) -> List[Dict]:
        """
        Get transactions for a specific month.
        
        Args:
            year: Year (e.g., 2026)
            month: Month (1-12)
            
        Returns:
            List of transactions for the specified month
        """
        try:
            all_data = self.get_all_transactions()
            monthly_data = []

            for row in all_data:
                try:
                    if 'Tanggal' in row:
                        date_str = str(row['Tanggal'])
                        if ' ' in date_str:
                            date_obj = datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
                        else:
                            date_obj = datetime.strptime(date_str, '%Y-%m-%d')

                        if date_obj.year == year and date_obj.month == month:
                            monthly_data.append(row)
                except (ValueError, KeyError):
                    continue

            return monthly_data

        except Exception as e:
            print(f"Error getting monthly transactions: {e}")
            return []

    def get_recent_transactions(self, limit: int = 5) -> List[Dict]:
        """
        Get the most recent transactions.
        
        Args:
            limit: Number of recent transactions to retrieve
            
        Returns:
            List of recent transactions
        """
        try:
            all_data = self.worksheet.get_all_values()
            if len(all_data) <= 1:
                return []

            rows = all_data[1:]
            rows.reverse()

            recent = []
            for row in rows[:limit]:
                if len(row) >= 5:
                    recent.append({
                        'Tanggal': row[0],
                        'User': row[1],
                        'Type': row[2],
                        'Amount': row[3],
                        'Description': row[4]
                    })

            return recent

        except Exception as e:
            print(f"Error getting recent transactions: {e}")
            return []

    def is_empty(self) -> bool:
        """
        Check if the sheet has no data (excluding header).
        
        Returns:
            bool: True if sheet is empty, False otherwise
        """
        try:
            values = self.worksheet.get_all_values()
            return len(values) <= 1
        except Exception:
            return True


_sheets_service = None


def get_sheets_service() -> SheetsService:
    """Get singleton instance of SheetsService."""
    global _sheets_service
    if _sheets_service is None:
        _sheets_service = SheetsService()
    return _sheets_service
