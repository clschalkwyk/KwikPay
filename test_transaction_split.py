import os
import unittest
from unittest.mock import patch

from transaction_split import split_transaction, TransactionSplitter


class TransactionSplitTests(unittest.TestCase):
    def test_split_transaction_calculates_allocations(self):
        result = split_transaction(20, supplier=2, salaries=3, maintenance=5)

        self.assertEqual(result["supplier"], 0.4)
        self.assertEqual(result["salaries"], 0.6)
        self.assertEqual(result["maintenance"], 1.0)
        self.assertEqual(result["profit"], 18.0)

    def test_splitter_rejects_percentages_over_100(self):
        with self.assertRaises(ValueError):
            TransactionSplitter(20, supplier=60, salaries=30, maintenance=20)

    def test_splitter_supports_custom_distribution(self):
        splitter = TransactionSplitter(100, supplier=10, salaries=15, maintenance=20)
        result = splitter.calculate()

        self.assertEqual(result["supplier"], 10.0)
        self.assertEqual(result["salaries"], 15.0)
        self.assertEqual(result["maintenance"], 20.0)
        self.assertEqual(result["profit"], 55.0)

    def test_environment_variables_are_used_when_no_values_are_passed(self):
        with patch.dict(
            os.environ,
            {
                "KWIKPAY_SUPPLIER_PERCENT": "10",
                "KWIKPAY_SALARIES_PERCENT": "15",
                "KWIKPAY_MAINTENANCE_PERCENT": "20",
            },
            clear=False,
        ):
            result = split_transaction(100)

            self.assertEqual(result["supplier"], 10.0)
            self.assertEqual(result["salaries"], 15.0)
            self.assertEqual(result["maintenance"], 20.0)
            self.assertEqual(result["profit"], 55.0)


if __name__ == "__main__":
    unittest.main()
