import unittest
import analyzer

class TestAnalyzer(unittest.TestCase):

    def test_text_1(self):
        self.assertEqual(
                analyzer.start('Шла Саша по шоссе и сосала сушку.')['norm_sentence_length'],
                11
                        )
        
    def test_text_2(self):
        self.assertEqual(
                analyzer.start('Шла Саша по шоссе и сосала сушку.')['names_and_geo'],
                {'Саша'}
                )

    def test_text_3(self):
        self.assertEqual(
                analyzer.start('''Все рабочие — от доярок до сварщиков, под команды, 
                               доносившиеся из радиоприемника, дружно приседали и бегали на месте! 
                               Производственная гимнастика, как и многое в СССР, было 
                               добровольно-принудительным занятием. Перед обедом или в конце смены 
                               в течение 5-10 минут на каждом предприятии проводилась гимнастика. 
                               Рабочие, не отходя от станка, под чутким руководством инструктора 
                               выполняли физические упражнения.''')['words'],54
                               )
    def test_text_4(self):
        self.assertEqual(
            analyzer.start('384')['text_ok'], False
                        )
  
    def test_text_5(self):
        self.assertEqual(
            analyzer.start('')['text_ok'], False
                        )
    def test_text_6(self):
        self.assertEqual(
            analyzer.start('''Шла Саша по шоссе, была хорошая погода. 
                           А в тексте бывает english/vinglish''')['reading_for_detail_speed'], 1
                        )
      

if __name__ == '__main__':
    unittest.main()