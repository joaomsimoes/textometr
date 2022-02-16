import unittest

from app.frequency_check import FrequencyCheck


class TestAnalyzer(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.frequencyCheck = FrequencyCheck()

    def test_words_1(self):
        self.assertEqual(
            TestAnalyzer.frequencyCheck.start("собака, сосиска, машина, лошадь, Иван"),
            1,
        )


if __name__ == "__main__":
    unittest.main()
