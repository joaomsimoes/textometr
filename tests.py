import unittest
import analyzer

class TestAnalyzer(unittest.TestCase):

    def test_text_1(self):
        self.assertEqual(analyzer.start('Ночь.')['level_comment'], 'A0, самое начало')

    def test_text_2(self):
        self.assertEqual(analyzer.start('Шла Саша по шоссе и сосала сушку.')['level_comment'], 'середина B2')

if __name__ == '__main__':
    unittest.main()