from dataclasses import dataclass


# A single allocation rule describing how much of a sale should go to a category.
@dataclass(frozen=True)
class Rule:
    name: str
    percent: float

    def __post_init__(self):
        # Every rule must be named so the result dictionary is explicit and readable.
        if not isinstance(self.name, str) or not self.name.strip():
            raise ValueError("Rule name must be a non-empty string.")

        # Percentages are stored as floats so values like 2, 3.5, or 10 are supported.
        percent = float(self.percent)
        if percent < 0:
            raise ValueError(f"Rule '{self.name}' cannot have a negative percentage.")

        object.__setattr__(self, "percent", percent)


class RulesEngine:
    """Evaluate a set of percentage-based allocation rules."""

    def __init__(self, rules):
        # Normalize all incoming rule shapes into a consistent list of Rule objects.
        self.rules = self._normalize_rules(rules)

        # Business rule: the total allocation must never exceed 100% of the sale.
        total_percent = sum(rule.percent for rule in self.rules)
        if total_percent > 100:
            raise ValueError("The total split percentage cannot exceed 100%.")

    @staticmethod
    def _normalize_rules(rules):
        # Allow either a dict of name -> percent or a list of rules/tuples.
        if isinstance(rules, dict):
            rules = list(rules.items())

        normalized = []
        seen_names = set()

        for rule in rules:
            if isinstance(rule, Rule):
                current = rule
            elif isinstance(rule, tuple) and len(rule) == 2:
                current = Rule(rule[0], rule[1])
            else:
                raise TypeError("Each rule must be a Rule instance or a (name, percent) tuple.")

            # Prevent duplicate categories from being evaluated twice.
            if current.name in seen_names:
                raise ValueError(f"Duplicate rule name '{current.name}' is not allowed.")

            seen_names.add(current.name)
            normalized.append(current)

        return normalized

    def evaluate(self, total_amount):
        # Sales must stay non-negative for the business rules to make sense.
        total_amount = float(total_amount)
        if total_amount < 0:
            raise ValueError("Total amount cannot be negative.")

        allocations = {}
        for rule in self.rules:
            # Convert each percentage to a money value using the sale total.
            allocations[rule.name] = total_amount * (rule.percent / 100)

        # Whatever remains after the configured rules is the business profit.
        allocations["profit"] = total_amount - sum(allocations.values())
        return allocations
