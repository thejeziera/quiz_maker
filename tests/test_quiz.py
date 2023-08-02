import unittest
import pandas as pd
from quiz_maker.main import get_next_question


class TestMain(unittest.TestCase):
    def test_get_next_question(self):
        df = pd.DataFrame({'Chapter': ['chap1', 'chap1', 'chap2', 'chap2'],
                           'Question': ['q1', 'q2', 'q3', 'q4'],
                           'Options': ['o1', 'o2', 'o3', 'o4'],
                           'Correct': ['1,0', '0,1', '1,0', '0,1']})
        progress = {0: {'correct': 3}, 1: {'correct': 0}, 2: {'correct': 3}, 3: {'correct': 0}}
        correct_threshold = 3
        chap_vars = {'chap1': 1, 'chap2': 0}

        question = get_next_question(df, progress, correct_threshold, chap_vars)
        self.assertIn(question, [1])


if __name__ == '__main__':
    unittest.main()
