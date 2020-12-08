# Быстренько обучаем модель и анализируем входной текст
import nltk
import pymystem3
import statistics
from nltk.tokenize import sent_tokenize
import re

class Analyzer_native:

    SYLLABLES = ['а', 'е', 'ё', 'и', 'о', 'у', 'ы', 'ю', 'я', 'э']

    TWO_VOWELS = ['ия', 'ии', 'ые', 'ие', 'ио', 'ию', 'иу', 'ее', 'ею', 'ея', 'ою', 'ая', 'яя', 'ое',
                  'аю', 'аэ', 'ье', 'ья', 'еа', 'ау', 'ую', 'юю', 'эт']

    COLUMNS_NEEDED = ['words', 'unique_words', 'sentences', 'mean_len_word' , 'mean_len_sentence',
                      'formula_flesh_oborneva', 'formula_flesh_kinc_oborneva' , 'formula_pushkin',
                      'level_comment','structure_complex', 'lexical_complex', 'narrativity','description',
                      'tt_ratio', 'lex_density','lexical_complex_rki',
                      'laposhina_list','detcorpus_5000', 'rki_children_list','rare_words']

    GRAM_FEATURES = [
        'A', 'ADV', 'ADVPRO', 'ANUM', 'APRO', 'COM', 'CONJ', 'INTJ',
        'NUM', 'PART', 'PR', 'S', 'SPRO', 'V', 'непрош', 'прош',
        'им', 'пр', 'род', 'твор', 'деепр', 'изъяв', 'инф', 'пов',
        'прич', 'кр', 'полн', 'притяж', '1-л', 'сред', 'несов',
        'сов', 'действ', 'страд', 'неод', 'од'
    ]

    # шкала сложности, высчитывается от 0 до 10, примерно соответствует классу
    INTERPRETER = [("7-8 лет.", 0, 2),
                   ("9-10 лет.", 2.1, 4),
                   ("11-12 лет.", 4.1, 6),
                   ("13-14 лет.", 6.1, 8),
                   ("15-17 лет.", 8.1, 9),
                   ("выпускник старшей школы.", 9.1, 10)]

    def __init__(self):

        print('Init Analyzer_native')

        self.mystem = pymystem3.Mystem(entire_input=False, disambiguation=True)

        # списки слов
        self.fr_10000_list = self.__load('data/fr_10000.txt')
        self.laposhina_list = self.__load('data/laposhina_list_from_formula.txt')
        self.detcorpus_list = self.__load('data/detcorpus_5000.txt')
        self.rki_children_list = self.__load('data/rki_children_list.txt')
        self.united_list = self.__load('data/united_simple_list.txt')
        self.stop_list = self.__load('data/stop_list.txt')


    # считаем слоги и буквы
    def __count_syllables(self, element):
        i_text = element.get('text')
        i_text_syl_counter = 0
        for ii in i_text:
            if ii in Analyzer_native.SYLLABLES:
                # print('marker')
                i_text_syl_counter += 1
        for i in Analyzer_native.TWO_VOWELS:
            if i_text.find(i) != -1:
                # print('two')
                i_text_syl_counter -= 1
        if i_text == 'его':
            i_text_syl_counter = 1
        if i_text_syl_counter == 0:
            i_text_syl_counter = 1
        self.number_of_syllables_list.append(i_text_syl_counter)
        self.words_length_list.append(len(i_text))
        if i_text_syl_counter >= 4:
            self.long_words_list.append(i_text)
        return True

    # чистимся от имен, геообъектов и бастардов
    def __clean_from_name_geo_bastard(self, element):
        self.whole_lemmas_list.append(element.get('analysis')[0]['lex'])
        gr_info = element.get('analysis')[0]['gr']
        if 'qual' in element.get('analysis')[0]:
            if element.get('analysis')[0]['qual'] == 'bastard':
                self.bastard_list.append(element.get('text'))
        if (gr_info.find('имя') > 0 or gr_info.find('гео') > 0):
            self.geo_imen_list.append(element.get('analysis')[0]['lex'])
        if (gr_info.find('фам') > 0 or gr_info.find('отч') > 0):
            self.geo_imen_list.append(element.get('analysis')[0]['lex'])
        if (
                element.get('analysis')[0]['lex'] == 'но' or
                element.get('analysis')[0]['lex'] == 'а' or
                element.get('analysis')[0]['lex'] == 'однако' or
                element.get('analysis')[0]['lex'] == 'зато'
        ):
            self.conj_adversative_list.append(element.get('analysis')[0]['lex'])
        return True

    # подсчет грам. информации
    def __count_gram(self, element):
        gr_info = element.get('analysis')[0]['gr']
        gr_info = gr_info.replace(',', '<b>')
        gr_info = gr_info.replace('=', '<b>')
        gr_info = gr_info.split('<b>')
        for i in Analyzer_native.GRAM_FEATURES:
            if i in gr_info:
                self.data_about_text_store[i] += 1
        if 'S' in gr_info:
            self.noun_list.append(element.get('analysis')[0]['lex'])
        if 'S' in gr_info or 'V' in gr_info or 'A' in gr_info or 'ADV' in gr_info:
            self.count_content_pos.append(element.get('analysis')[0]['lex'])
        return True

    def __count_passive_form(self, element):
        if element[0].get('analysis') and element[1].get('analysis'):
            element0_gr = self.__get_gr_info(element[0])
            element1_gr = self.__get_gr_info(element[1])
            if (element[0].get('analysis')[0]['lex'] == 'быть'
                    and 'прош' in element0_gr):
                if 'прич' in element1_gr:
                    self.count_passive.append(element[1].get('text'))
        return True

    def __load(self, file_name):
        f = open(file_name, 'r', encoding='utf_8')
        lines = f.readlines()
        f.close()
        return [l.replace('\n', '') for l in lines]

    def __get_gr_info(self, element):
        gr_info = element.get('analysis')[0]['gr']
        gr_info = gr_info.replace(',', '<b>')
        gr_info = gr_info.replace('=', '<b>')
        gr_info = gr_info.split('<b>')
        return gr_info

        # Общий цикл просмотра анализа слов

    def __gram_analyze(self, element):
        for i in element:
            self.__count_syllables(i)
            if len(i.get('analysis')) > 0:
                self.__clean_from_name_geo_bastard(i)
                self.__count_gram(i)
        return True

        # Вычисляем процент слов из разных словников и частотных списков

    def __percent_of_known_words(self, element, list_of_words):
        if len(list_of_words) == 0 or len(element) == 0:
            return 0
        else:
            known_words = [w for w in element if w in list_of_words]
            percent = (len(known_words) / len(element)) * 100
            return round(percent)

    def __clean_text(self, input_text):
        new_text = input_text.replace('­\n', '')
        new_text = new_text.replace('\n', ' ')
        new_text = new_text.replace('•', '')
        new_text = new_text.replace('…', '.')
        new_text = new_text.replace('...', '.')
        new_text = new_text.replace('..', '.')
        new_text = new_text.replace('?.', '?')
        new_text = new_text.replace('!.', '!')
        new_text = new_text.replace('_', '')
        new_text = new_text.replace('!—', '! —')
        new_text = new_text.replace('?—', '? —')
        new_text = new_text.replace('\xad', '')
        return new_text


    # делим текст на предложения
    def __sent_tokenize_plus(self, this_text):
        new_text = this_text.replace('(с.', '(стр ')
        new_text = new_text.replace('на с.', 'на стр')
        new_text = new_text.replace('.—', '. —')
        new_text = re.sub(r'([a-zа-я1-9])\.([A-ZА-Я])', '\\1. \\2', new_text)
        new_text = re.sub(r'([a-zа-я1-9])\!([A-ZА-Я])', '\\1! \\2', new_text)
        new_text = re.sub(r'([a-zа-я1-9])\?([A-ZА-Я])', '\\1? \\2', new_text)
        new_text = re.sub(r'(рис. )([1-9])', 'рис \\2', new_text)
        # В г. Смоленске
        new_text = re.sub(r'( г. )([A-ZА-Я]{1})', ' г<dot> \\2', new_text)
        # С.В. Морозов
        new_text = re.sub(r'([А-Я]{1}\.[А-Я]{1})\. ([A-ZА-Я]{1}[a-zа-я]+)', '\\1<dot> \\2', new_text)
        # достигает 55 см. в длину
        new_text = re.sub(r'( см. )([a-zа-я1-9])', ' см<dot> \\2', new_text)

        sentences = sent_tokenize(new_text)

        new_sentences = []
        for i in sentences:
            # У лисички длина 3 м. А у котика - 2.
            if re.findall(r'([a-zа-я1-9])\. ([А-Я]{1})', i):
                i_new = re.sub(r'([a-zа-я1-9])\. ([А-Я]{1})', '\\1.<stop>\\2', i)
                i_split = i_new.split("<stop>")
                for ii in i_split:
                    new_sentences.append(ii)
                continue
            # И вы вырастили мух?- Нет пока.
            if re.findall(r'([a-zа-я1-9]\.|\?|\!)(- [А-Я]{1})', i):
                i_new = re.sub(r'([a-zа-я1-9]\.|\?|\!)(- [А-Я]{1})', '\\1<stop>\\2', i)
                i_split = i_new.split("<stop>")
                for ii in i_split:
                    new_sentences.append(ii)
                continue
            if re.findall(r'[а-яА-ЯёЁ]+', i):
                new_sentences.append(i)

        for i in new_sentences:
            i = i.replace('<dot>', '.')
        return new_sentences

    # начало цикла анализа этого текста
    def start(self, raw_text):

        print('Start Analyzer_native')

        text = self.__clean_text(raw_text)
        # создаем словарь и будем в него все складывать
        self.data_about_text_store = {}

        #чистый финальный списочек параметров
        self.data_about_text = {}

        # первая проверка текста - не слишком маленький
        if len(text) < 10:
            self.data_about_text['text_ok'] = False
            self.data_about_text['text_error_message'] = ('Введите текст на'
                                                     ' русском языке не менее 5 слов.')
            return self.data_about_text

        # Вторая проверка текста - не слишком большой
        if len(text) > 10000:
            self.data_about_text['text_ok'] = False
            self.data_about_text['text_error_message'] = ('Введите текст не '
                                                     'более 10 000 знаков.')
            return self.data_about_text

        self.sentences = self.__sent_tokenize_plus(text)
        self.whole_analyzed_text = self.mystem.analyze(text)  # весь текст одним списком
        analyzed_bigrams = list(nltk.bigrams(self.whole_analyzed_text))  # биграммочки

        self.whole_lemmas_list = []

        self.noun_list = []

        self.bastard_list = []

        self.geo_imen_list = []

        self.conj_adversative_list = []  # противительные союзы

        self.modal_words_list = []

        self.words_length_list = []

        self.number_of_syllables_list = []

        self.long_words_list = []  # слова более чем из 4 слогов

        self.count_kotoryi = []

        self.count_content_pos = []

        self.count_passive = []


        for i in Analyzer_native.GRAM_FEATURES:
            self.data_about_text_store[i] = 0

        # запускаем функцию со всеми грам. анализами
        self.__gram_analyze(self.whole_analyzed_text)

        for i in analyzed_bigrams:
            self.__count_passive_form(i)

        if len(self.whole_lemmas_list) < 5:
            self.data_about_text['text_ok'] = False
            self.data_about_text['text_error_message'] = ('Введите текст на'
                                                 ' русском языке не менее 5 слов.')
            return self.data_about_text

        self.data_about_text['text_ok'] = True
        self.data_about_text['text_error_message'] = ('')

        clean_lemmas_list = [
            f for f in self.whole_lemmas_list if
            f not in self.geo_imen_list and f not in self.bastard_list and f not in self.stop_list
        ]

        all_words = len(self.whole_analyzed_text)
        all_sentences = len(self.sentences)
        all_syllables = sum(self.number_of_syllables_list)

        all_len_words = [len(f) for f in self.whole_lemmas_list]
        all_len_sentences = [len(f.split(' ')) for f in self.sentences]

        long_words = len(self.long_words_list)
        whole_lemmas_minus_stop = [f for f in self.whole_lemmas_list if f not in self.stop_list]
        unique_lemmas_list = list(set(whole_lemmas_minus_stop))
        noun_unique_list = list(set(self.noun_list))  # список уникальных сущ.

        # Цифры про текст:
        # всего слов в тексте
        self.data_about_text_store['words'] = (len(self.whole_analyzed_text))
        self.data_about_text_store['syllables'] = all_syllables
        self.data_about_text_store['unique_words'] = len(unique_lemmas_list)
        # всего предложений в тексте
        self.data_about_text_store['sentences'] = all_sentences
        # средняя длина слова в тексте
        self.data_about_text_store['mean_len_word'] = round(((sum(self.words_length_list)) / all_words), 1)
        self.data_about_text_store['median_len_word'] = statistics.median(all_len_words)
        self.data_about_text_store['median_len_sentence'] = statistics.median(
            all_len_sentences
        )

        # средняя длина предложения в тексте
        self.data_about_text_store['mean_len_sentence'] = round((all_words / all_sentences), 1)
        self.data_about_text_store['mean_len_word_in_syllables'] = all_syllables / all_words
        self.data_about_text_store['percent_of_long_words'] = long_words / all_words

        # lexical density - лексическая плотность, соотношение смысловых и служебных
        # частей речи: чем она выше, тем считается что текст сложнее
        self.data_about_text_store['lex_density'] = f"{round((len(self.count_content_pos) / len(self.whole_lemmas_list)) * 10)} из 10"

        # type-token ratio (lexical diversity) - number of types/the number of tokens:
        # чем выше, тем лексика в тексте "однотипнее"
        # потом попробовать sttr: то же самое на отрезках в 1000 слов.
        # standardised type/token ratio
        self.data_about_text_store['tt_ratio'] = f"{round((len(unique_lemmas_list) / len(self.whole_lemmas_list)) * 10)} из 10"

        self.data_about_text_store['passive'] = len(self.count_passive)

        ##формулы читабельности (адаптированные, из диссера Оборневой)##
        formula_f_oborneva = round(206.835 - (60.1 * (all_syllables / all_words)) - (1.3 * (all_words / all_sentences)))
        formula_f_k_oborneva = round(0.5 * (all_words / all_sentences) + 8.4 * (all_syllables / all_words) - 15.59)

        self.data_about_text_store['formula_flesh_oborneva'] = f"{formula_f_oborneva} из 100 (чем больше - тем текст легче)"
        self.data_about_text_store['formula_flesh_kinc_oborneva'] = f"{formula_f_k_oborneva} (примерно должна соответствовать классу)"

        in_laposhina_list = self.__percent_of_known_words(self.whole_lemmas_list, self.laposhina_list)

        self.data_about_text_store['laposhina_list'] = f"{in_laposhina_list} %"

        in_detcorpus_5000 = self.__percent_of_known_words(
           self.whole_lemmas_list, self.detcorpus_list)

        self.data_about_text_store['detcorpus_5000'] = f"{in_detcorpus_5000} %"

        in_rki_children = self.__percent_of_known_words(
            self.whole_lemmas_list, self.rki_children_list)

        self.data_about_text_store['rki_children_list'] = f"{in_rki_children} %"

        in_united_simple_list = self.__percent_of_known_words(
            self.whole_lemmas_list, self.united_list)

        self.data_about_text_store['united_simple_list'] = f"{in_united_simple_list} %"

        self.data_about_text_store['rare_words'] = list(set([f for f in clean_lemmas_list if
                                                             f not in self.detcorpus_list and f not in self.fr_10000_list]))

        structure_complex = round(
            (100 - formula_f_oborneva + self.data_about_text_store['прич'] + self.data_about_text_store['страд'] + self.data_about_text_store[
                'passive']) / 10)

        if structure_complex > 10:
            structure_complex = 10
        if structure_complex < 0:
            structure_complex = 0

        self.data_about_text_store['structure_complex'] = f"{structure_complex} из 10"

        lexical_complex = round(10 - ((((in_detcorpus_5000 - 50) * 2) + 7) / 10))
        if lexical_complex > 10:
            lexical_complex = 10
        if lexical_complex < 0:
            lexical_complex = 0

        self.data_about_text_store['lexical_complex'] = f"{lexical_complex} из 10"

        lexical_complex_rki = round(10 - ((((in_rki_children - 60) * 2)) / 10))

        if lexical_complex_rki > 10:
            lexical_complex_rki = 10
        if lexical_complex_rki < 0:
            lexical_complex_rki = 0

        self.data_about_text_store['lexical_complex_rki'] = f'{lexical_complex_rki} из 10'

        formula_pushkin = round(((structure_complex + lexical_complex) / 2), 1)

        self.data_about_text_store['formula_pushkin'] = round(formula_pushkin)

        for i in Analyzer_native.INTERPRETER:
            if i[1] <= formula_pushkin <= i[2]:
                self.data_about_text_store['level_comment'] = f"{round(formula_pushkin)} из 10, {i[0]}"

        narrativity = round(10 - 2 * (self.data_about_text_store['S'] / (self.data_about_text_store['V'] + 1)))

        if narrativity < 0:
            narrativity = 0

        self.data_about_text_store['narrativity'] = f"{narrativity} из 10"

        description = round(3 * (self.data_about_text_store['A'] / all_sentences))

        if description > 10:
            description = 10

        self.data_about_text_store['description'] = f"{description} из 10"

        for i in self.data_about_text_store:
            if i in Analyzer_native.COLUMNS_NEEDED:
                self.data_about_text[i] = self.data_about_text_store[i]

        print(self.data_about_text)
        return self.data_about_text
