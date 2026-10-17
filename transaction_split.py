import os


class TransactionSplitter:
    # Default split percentages used when the app does not receive override values.
    DEFAULT_SPLITS = {
        "supplier": 2,
        "salaries": 3,
        "maintenance": 5,
    }

    @classmethod
    def from_environment(cls, total_amount, env=None):
        # Read the transaction rules from environment variables so the business can change
        # the split without touching application logic.
        if env is None:
            env = os.environ

        values = dict(cls.DEFAULT_SPLITS)
        values["supplier"] = float(env.get("KWIKPAY_SUPPLIER_PERCENT", values["supplier"]))
        values["salaries"] = float(env.get("KWIKPAY_SALARIES_PERCENT", values["salaries"]))
        values["maintenance"] = float(env.get("KWIKPAY_MAINTENANCE_PERCENT", values["maintenance"]))

        return cls(total_amount, **values)

    def __init__(self, total_amount, supplier=None, salaries=None, maintenance=None, env=None):
        # Keep the amount as a number so percentage math is straightforward.
        self.total_amount = float(total_amount)

        if env is None:
            env = os.environ

        # Start from default split values, then override with explicit arguments or env vars.
        values = dict(self.DEFAULT_SPLITS)
        if supplier is not None:
            values["supplier"] = float(supplier)
        else:
            values["supplier"] = float(env.get("KWIKPAY_SUPPLIER_PERCENT", values["supplier"]))

        if salaries is not None:
            values["salaries"] = float(salaries)
        else:
            values["salaries"] = float(env.get("KWIKPAY_SALARIES_PERCENT", values["salaries"]))

        if maintenance is not None:
            values["maintenance"] = float(maintenance)
        else:
            values["maintenance"] = float(env.get("KWIKPAY_MAINTENANCE_PERCENT", values["maintenance"]))

        self.distribution = values
        self._validate()

    def _validate(self):
        # Reject invalid negative sales values.
        if self.total_amount < 0:
            raise ValueError("Total amount cannot be negative.")

        # The combined split must not exceed the full transaction value.
        total_percentage = sum(self.distribution.values())
        if total_percentage > 100:
            raise ValueError("The total split percentage cannot exceed 100%.")

    def calculate(self):
        # Convert each percentage into a money value for the sale.
        allocations = {}
        for name, percentage in self.distribution.items():
            allocations[name] = self.total_amount * (percentage / 100)

        # Whatever is left after fixed allocations is the business profit.
        allocations["profit"] = self.total_amount - sum(allocations.values())
        return allocations


def split_transaction(total_amount, supplier=None, salaries=None, maintenance=None, env=None):
    """Split a transaction into supplier, salaries, maintenance, and profit.

    Percentages are read from environment variables when explicit values are not provided.
    This is the public helper used by the app to process each sale.
    """
    splitter = TransactionSplitter(
        total_amount,
        supplier=supplier,
        salaries=salaries,
        maintenance=maintenance,
        env=env,
    )
    return splitter.calculate()
