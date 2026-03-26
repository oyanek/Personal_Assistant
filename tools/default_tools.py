from typing import List, Dict, Any


def get_transactions(month: str) -> List[Dict[str, Any]]:
    # placeholder: replace with DB query from MemoryStore
    return [
        {"date": f"2026-{month}-01", "amount": -45.99, "category": "food", "description": "Groceries"},
        {"date": f"2026-{month}-15", "amount": 1200.00, "category": "salary", "description": "Paycheck"},
    ]


def analyze_stock(ticker: str) -> str:
    # placeholder analysis
    return f"Stock analysis for {ticker}: bull trend indicated with moderate risk and long-term potential."


def summarize_text(text: str) -> str:
    if not text:
        return "No text provided to summarize."
    return f"Summary: {text[:120]}{'...' if len(text) > 120 else ''}"


def add_transaction(date: str, amount: float, category: str, description: str) -> Dict[str, Any]:
    return {
        "message": "Transaction added (simulated).",
        "data": {"date": date, "amount": amount, "category": category, "description": description},
    }


def list_transactions() -> List[Dict[str, Any]]:
    return [
        {"date": "2026-01-01", "amount": -65.0, "category": "utilities", "description": "Electricity"},
        {"date": "2026-01-04", "amount": -15.0, "category": "food", "description": "Lunch"},
    ]
