"""
Finance Service Module.
Handles balance calculations and financial reports using pandas.
"""
from datetime import datetime
from typing import Dict, List, Tuple, Optional
import pandas as pd

from sheets_service import get_sheets_service


class FinanceService:
    """Service class for financial calculations."""

    def __init__(self):
        """Initialize the finance service."""
        self.sheets = get_sheets_service()

    def get_balance(self) -> Tuple[int, int, int]:
        """
        Calculate total income, expense, and balance.
        
        Returns:
            Tuple of (total_income, total_expense, balance)
        """
        try:
            transactions = self.sheets.get_all_transactions()

            if not transactions:
                return (0, 0, 0)

            df = pd.DataFrame(transactions)

            df['Amount'] = pd.to_numeric(df['Amount'], errors='coerce').fillna(0)

            total_income = df[df['Type'] == 'Income']['Amount'].sum()
            total_expense = df[df['Type'] == 'Expense']['Amount'].sum()

            balance = total_income - total_expense

            return (int(total_income), int(total_expense), int(balance))

        except Exception as e:
            print(f"Error calculating balance: {e}")
            return (0, 0, 0)

    def get_monthly_report(self, year: int, month: int) -> Dict:
        """
        Get monthly financial report.
        
        Args:
            year: Year (e.g., 2026)
            month: Month (1-12)
            
        Returns:
            Dictionary with monthly financial data
        """
        try:
            transactions = self.sheets.get_monthly_transactions(year, month)

            if not transactions:
                return {
                    'income': 0,
                    'expense': 0,
                    'net_profit': 0,
                    'month_name': datetime(year, month, 1).strftime('%B %Y')
                }

            df = pd.DataFrame(transactions)

            df['Amount'] = pd.to_numeric(df['Amount'], errors='coerce').fillna(0)

            income = df[df['Type'] == 'Income']['Amount'].sum()
            expense = df[df['Type'] == 'Expense']['Amount'].sum()
            net_profit = income - expense

            return {
                'income': int(income),
                'expense': int(expense),
                'net_profit': int(net_profit),
                'month_name': datetime(year, month, 1).strftime('%B %Y')
            }

        except Exception as e:
            print(f"Error calculating monthly report: {e}")
            return {
                'income': 0,
                'expense': 0,
                'net_profit': 0,
                'month_name': datetime(year, month, 1).strftime('%B %Y')
            }

    def get_top_income_user(self) -> Optional[Dict]:
        """
        Get the user with the highest total income.
        
        Returns:
            Dictionary with user name and total income, or None
        """
        try:
            transactions = self.sheets.get_all_transactions()

            if not transactions:
                return None

            df = pd.DataFrame(transactions)

            df['Amount'] = pd.to_numeric(df['Amount'], errors='coerce').fillna(0)

            income_df = df[df['Type'] == 'Income']

            if income_df.empty:
                return None

            user_totals = income_df.groupby('User')['Amount'].sum()

            if user_totals.empty:
                return None

            top_user = user_totals.idxmax()
            top_amount = int(user_totals.max())

            return {
                'user': top_user,
                'amount': top_amount
            }

        except Exception as e:
            print(f"Error getting top income user: {e}")
            return None


_finance_service = None


def get_finance_service() -> FinanceService:
    """Get singleton instance of FinanceService."""
    global _finance_service
    if _finance_service is None:
        _finance_service = FinanceService()
    return _finance_service
