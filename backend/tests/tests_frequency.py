import unittest

from app.frequency_check import FrequencyCheck
import pymystem3


class TestAnalyzer(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        mystem = pymystem3.Mystem(entire_input=False, disambiguation=True)
        cls.frequencyCheck = FrequencyCheck(mystem)

    def test_words_1(self):
        self.assertEqual(
            TestAnalyzer.frequencyCheck.start("-"),
            [{"input_error": True, "is_omonim": False, "not_in_list": False}],
        )

    def test_words_2(self):
        self.assertEqual(
            TestAnalyzer.frequencyCheck.start("котенок"),
            [
                {
                    "input_error": False,
                    "not_in_list": False,
                    "is_omonim": False,
                    "lemma": "котенок",
                    "comment_main": "частотно (ТОП-5000)",
                    "comment_child": "очень частотно (ТОП-1000)",
                    "pos": "NOUN",
                    "cefr": "B2",
                    "kelly": "A2",
                    "rnc_ipm": 14.5,
                    "detcorpus_ipm": 34.0,
                    "rufola_123_ipm": 0,
                    "det_rki_ipm": 526.07,
                    "bilingual_ipm": 493.69,
                    "native_ipm": 289.65,
                }
            ],
        )

    def test_words_3(self):
        self.assertEqual(
            TestAnalyzer.frequencyCheck.start(
                "арбуз, хурма, банан, яблоко, слива, помидор"
            ),
            [
                {
                    "input_error": False,
                    "not_in_list": False,
                    "is_omonim": False,
                    "lemma": "арбуз",
                    "comment_main": "низкочастотно (ТОП-6000)",
                    "comment_child": "очень частотно (ТОП-2000)",
                    "pos": "NOUN",
                    "cefr": "B2",
                    "kelly": "B1",
                    "rnc_ipm": 9.1,
                    "detcorpus_ipm": 20.0,
                    "rufola_123_ipm": 0,
                    "det_rki_ipm": 175.36,
                    "bilingual_ipm": 72.07,
                    "native_ipm": 83.7,
                },
                {
                    "input_error": False,
                    "not_in_list": False,
                    "is_omonim": False,
                    "lemma": "банан",
                    "comment_main": "низкочастотно (ТОП-6000)",
                    "comment_child": "очень частотно (ТОП-1000)",
                    "pos": "NOUN",
                    "cefr": "B1",
                    "kelly": "A1",
                    "rnc_ipm": 7.3,
                    "detcorpus_ipm": 12.0,
                    "rufola_123_ipm": 40,
                    "det_rki_ipm": 355.45,
                    "bilingual_ipm": 61.26,
                    "native_ipm": 19.82,
                },
                {
                    "input_error": False,
                    "not_in_list": False,
                    "is_omonim": False,
                    "lemma": "помидор",
                    "comment_main": "частотно (ТОП-5000)",
                    "comment_child": "очень частотно (ТОП-2000)",
                    "pos": "NOUN",
                    "cefr": "B1",
                    "kelly": "A1",
                    "rnc_ipm": 15.4,
                    "detcorpus_ipm": 19.0,
                    "rufola_123_ipm": 48,
                    "det_rki_ipm": 241.71,
                    "bilingual_ipm": 54.05,
                    "native_ipm": 101.32,
                },
                {
                    "input_error": False,
                    "not_in_list": False,
                    "is_omonim": False,
                    "lemma": "слива",
                    "comment_main": "низкочастотно (ТОП-7000)",
                    "comment_child": "очень частотно (ТОП-2000)",
                    "pos": "NOUN",
                    "cefr": "B2",
                    "kelly": "NO",
                    "rnc_ipm": 5.5,
                    "detcorpus_ipm": 15.0,
                    "rufola_123_ipm": 8,
                    "det_rki_ipm": 113.74,
                    "bilingual_ipm": 70.27,
                    "native_ipm": 33.04,
                },
                {
                    "input_error": False,
                    "not_in_list": False,
                    "is_omonim": False,
                    "lemma": "хурма",
                    "comment_main": "низкочастотно (ТОП-9000)",
                    "comment_child": "низкочастотно (ТОП-7000)",
                    "pos": "NOUN",
                    "cefr": "NO",
                    "kelly": "NO",
                    "rnc_ipm": 1.0,
                    "detcorpus_ipm": 0.0,
                    "rufola_123_ipm": 0,
                    "det_rki_ipm": 37.91,
                    "bilingual_ipm": 0.0,
                    "native_ipm": 0.0,
                },
            ],
        )

    def test_words_4(self):
        self.assertEqual(
            TestAnalyzer.frequencyCheck.start("прямо"),
            [
                {
                    "bilingual_ipm": 120.72,
                    "cefr": "A2",
                    "comment_child": "очень частотно (ТОП-1000)",
                    "comment_main": "очень частотно (ТОП-1000)",
                    "det_rki_ipm": 127.96,
                    "detcorpus_ipm": 281.3,
                    "input_error": False,
                    "is_omonim": True,
                    "kelly": "A2",
                    "lemma": "прямо",
                    "native_ipm": 110.13,
                    "not_in_list": False,
                    "pos": "PART",
                    "rnc_ipm": 130.3,
                    "rufola_123_ipm": 159,
                },
                {
                    "bilingual_ipm": 20.0,
                    "cefr": "A2",
                    "comment_child": "очень частотно (ТОП-2000)",
                    "comment_main": "очень частотно (ТОП-1000)",
                    "det_rki_ipm": 18.96,
                    "detcorpus_ipm": 57.15,
                    "input_error": False,
                    "is_omonim": True,
                    "kelly": "A2",
                    "lemma": "прямо",
                    "native_ipm": 19.82,
                    "not_in_list": False,
                    "pos": "ADVERB",
                    "rnc_ipm": 118.0,
                    "rufola_123_ipm": 16,
                },
            ],
        )

    def test_words_5(self):
        self.assertEqual(
            TestAnalyzer.frequencyCheck.start("#!"),
            [{"input_error": True, "is_omonim": False, "not_in_list": False}],
        )

    def test_words_6(self):
        self.assertEqual(
            TestAnalyzer.frequencyCheck.start("собака, сосиска, машина, лошадь, Иван"),
            [
                {
                    "input_error": False,
                    "not_in_list": True,
                    "is_omonim": False,
                    "lemma": "иван",
                },
                {
                    "input_error": False,
                    "not_in_list": False,
                    "is_omonim": False,
                    "lemma": "лошадь",
                    "comment_main": "очень частотно (ТОП-2000)",
                    "comment_child": "очень частотно (ТОП-1000)",
                    "pos": "NOUN",
                    "cefr": "B1",
                    "kelly": "A2",
                    "rnc_ipm": 80.9,
                    "detcorpus_ipm": 166.0,
                    "rufola_123_ipm": 191,
                    "det_rki_ipm": 127.96,
                    "bilingual_ipm": 156.76,
                    "native_ipm": 150.88,
                },
                {
                    "input_error": False,
                    "not_in_list": False,
                    "is_omonim": False,
                    "lemma": "машина",
                    "comment_main": "очень частотно (ТОП-1000)",
                    "comment_child": "очень частотно (ТОП-1000)",
                    "pos": "NOUN",
                    "cefr": "A1",
                    "kelly": "A1",
                    "rnc_ipm": 490.4,
                    "detcorpus_ipm": 557.0,
                    "rufola_123_ipm": 844,
                    "det_rki_ipm": 1047.39,
                    "bilingual_ipm": 601.8,
                    "native_ipm": 237.89,
                },
                {
                    "input_error": False,
                    "not_in_list": False,
                    "is_omonim": False,
                    "lemma": "собака",
                    "comment_main": "очень частотно (ТОП-1000)",
                    "comment_child": "очень частотно (ТОП-1000)",
                    "pos": "NOUN",
                    "cefr": "A1",
                    "kelly": "A1",
                    "rnc_ipm": 132.2,
                    "detcorpus_ipm": 310.0,
                    "rufola_123_ipm": 534,
                    "det_rki_ipm": 1118.48,
                    "bilingual_ipm": 812.61,
                    "native_ipm": 476.87,
                },
                {
                    "input_error": False,
                    "not_in_list": False,
                    "is_omonim": False,
                    "lemma": "сосиска",
                    "comment_main": "низкочастотно (ТОП-6000)",
                    "comment_child": "частотно (ТОП-3000)",
                    "pos": "NOUN",
                    "cefr": "B2",
                    "kelly": "A1",
                    "rnc_ipm": 7.5,
                    "detcorpus_ipm": 11.0,
                    "rufola_123_ipm": 16,
                    "det_rki_ipm": 18.96,
                    "bilingual_ipm": 21.62,
                    "native_ipm": 12.11,
                },
            ],
        )


if __name__ == "__main__":
    unittest.main()
