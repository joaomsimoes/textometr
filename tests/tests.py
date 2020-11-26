import unittest
from analyzer import Analyzer

class TestAnalyzer(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.text_analyzer = Analyzer()

    def test_text_1(self):
        self.assertEqual(
            TestAnalyzer.text_analyzer.start('Шла Саша по шоссе и сосала сушку.')['sentences'],
            1
        )
        
    def test_text_2(self):
        self.assertEqual(
            TestAnalyzer.text_analyzer.start('Шла Саша по шоссе и сосала сушку.')['names_and_geo'],
            ['Саша']
        )

    def test_text_3(self):
        self.assertEqual(
            TestAnalyzer.text_analyzer.start('Все рабочие — от доярок до сварщиков, под команды,'
                ' доносившиеся из радиоприемника, дружно приседали и бегали'
                ' на месте! Производственная гимнастика, как и многое в СССР,'
                ' было добровольно-принудительным занятием. Перед обедом или'
                ' в конце смены в течение 5-10 минут на каждом предприятии'
                ' проводилась гимнастика. Рабочие, не отходя от станка, под'
                ' чутким руководством инструктора выполняли физические'
                ' упражнения.')['words'],
            54
        )

    def test_text_4(self):
        self.assertEqual(
            TestAnalyzer.text_analyzer.start('384')['text_ok'],
            False
        )

    def test_text_5(self):
        self.assertEqual(
            TestAnalyzer.text_analyzer.start('')['text_ok'],
            False
        )

    def test_text_6(self):
        self.assertEqual(
            TestAnalyzer.text_analyzer.start('Шла Саша по шоссе, была хорошая погода. А в тексте'
                ' бывает english/vinglish')['words'],
            13
        )

    def test_text_7(self):
        self.assertEqual(
            TestAnalyzer.text_analyzer.start('Сестра Криса Фармера Пенни стала журналисткой. '
                           'Когда брата убили, ей было 17 лет.В 2015 году — '
                           'через два года после смерти отца — Пенни Фармер '
                           'решила попытаться найти предполагаемого убийцу '
                           'брата в фейсбуке. У нее получилось моментально; '
                           'кроме того, она нашла двух сыновей мужчины и одну '
                           'из его жен. Она разослала всем им сообщения — и '
                           'обратилась в полицию Манчестера. Вскоре выяснилось'
                           ', что в Сакраменто заново открыли дело об исчезно'
                           'вении третьей жены Бостона.Полиция допросила сынов'
                           'ей мужчины. Они рассказали, что всегда знали, что '
                           'Бостон убил их мать (именно его третья жена родила'
                           'обоих). Кроме того, они рассказали, что находились'
                           'на лодке, когда Бостон убил Криса Фармера и Пету '
                           'Фрэмптон. По их словам, они сразу рассказали об эт'
                           'ом следователям — однако те почему-то не предприня'
                           'ли никаких действий.')['text_ok'],True
        )

    def test_text_8(self):
        self.assertEqual(
            TestAnalyzer.text_analyzer.start('Я считаю справедливым ввести новые.')['text_ok'],
            True
        )

if __name__ == '__main__':
    unittest.main()