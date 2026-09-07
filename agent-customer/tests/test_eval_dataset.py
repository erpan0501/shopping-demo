import unittest
from collections import Counter

from eval.cases import get_eval_cases


class EvaluationDatasetTests(unittest.TestCase):
    def test_dataset_has_200_unique_cases_with_expected_coverage(self) -> None:
        cases = get_eval_cases("2087106115733889025")

        self.assertEqual(len(cases), 200)
        self.assertEqual(len({case.case_id for case in cases}), 200)
        self.assertTrue(all(case.question for case in cases))
        self.assertTrue(all(case.expected_sources for case in cases))
        self.assertEqual(
            Counter(case.category for case in cases),
            {
                "order_detail": 50,
                "order_list": 40,
                "logistics": 30,
                "faq": 30,
                "handoff": 20,
                "after_sale": 20,
                "other": 10,
            },
        )


if __name__ == "__main__":
    unittest.main()
