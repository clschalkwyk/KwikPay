import os
from transaction_split import TransactionSplitter


def create_sale_response(payload):
    """Create a JSON-like response for a sale transaction.

    Example payload:
        {"amount": 20}
        {"amount": 20, "supplier": 2, "salaries": 3, "maintenance": 5}
    """
    amount = float(payload.get("amount", 0))

    supplier = payload.get("supplier")
    salaries = payload.get("salaries")
    maintenance = payload.get("maintenance")

    if supplier is None and salaries is None and maintenance is None:
        splitter = TransactionSplitter.from_environment(amount, os.environ)
    else:
        splitter = TransactionSplitter(
            amount,
            supplier=supplier,
            salaries=salaries,
            maintenance=maintenance,
            env=os.environ,
        )

    split = splitter.calculate()
    return {
        "amount": amount,
        "split": split,
    }
