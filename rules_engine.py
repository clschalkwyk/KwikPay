from dataclasses import dataclass


@dataclass(frozen=True)
class Rule:
    name: str
    percent: float

    def __post_init__(self):
        if not isinstance(self.name, str) or not self.name.strip():
            raise ValueError("Rule name must be a non-empty string.")

        percent = float(self.percent)
        if percent < 0:
            raise ValueError(f"Rule '{self.name}' cannot have a negative percentage.")

        object.__setattr__(self, "percent", percent)


class RulesEngine:
    """Evaluate a set of percentage-based allocation rules."""

    def __init__(self, rules):
        self.rules = self._normalize_rules(rules)
        total_percent = sum(rule.percent for rule in self.rules)
        if total_percent > 100:
            raise ValueError("The total split percentage cannot exceed 100%.")

    @staticmethod
    def _normalize_rules(rules):
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

            if current.name in seen_names:
                raise ValueError(f"Duplicate rule name '{current.name}' is not allowed.")

            seen_names.add(current.name)
            normalized.append(current)

        return normalized

    def evaluate(self, total_amount):
        total_amount = float(total_amount)
        if total_amount < 0:
            raise ValueError("Total amount cannot be negative.")

        allocations = {}
        for rule in self.rules:
            allocations[rule.name] = total_amount * (rule.percent / 100)

        allocations["profit"] = total_amount - sum(allocations.values())
        return allocations
