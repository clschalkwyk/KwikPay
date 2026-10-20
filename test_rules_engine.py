import unittest

from rules_engine import Rule, RulesEngine


class RulesEngineTests(unittest.TestCase):
    def test_rule_and_engine_can_evaluate_percentages(self):
        rules = [
            Rule("supplier", 2),
            Rule("salaries", 3),
            Rule("maintenance", 5),
        ]

        engine = RulesEngine(rules)
        result = engine.evaluate(20)

        self.assertEqual(result["supplier"], 0.4)
        self.assertEqual(result["salaries"], 0.6)
        self.assertEqual(result["maintenance"], 1.0)
        self.assertEqual(result["profit"], 18.0)

    def test_engine_rejects_rules_that_exceed_100_percent(self):
        with self.assertRaises(ValueError):
            RulesEngine([
                Rule("supplier", 60),
                Rule("salaries", 30),
                Rule("maintenance", 20),
            ])


if __name__ == "__main__":
    unittest.main()
