
import numpy as np
import pandas as pd
import nltk
from sklearn import linear_model
import pymystem3
from collections import defaultdict
import statistics
from nltk.tokenize import sent_tokenize
import re
from joblib import dump, load


class Analyzer_foreign:
    SYLLABLES = ['а', 'е', 'ё', 'и', 'о', 'у', 'ы', 'ю', 'я', 'э']

    TWO_VOWELS = ['ия', 'ии', 'ые', 'ие', 'ио', 'ию', 'иу', 'ее', 'ею', 'ея', 'ою', 'ая', 'яя', 'ое',
                  'аю', 'аэ', 'ье', 'ья', 'еа', 'ау', 'ую', 'юю', 'эт']

    MODAL_WORDS = [
        'хочется', 'нужно', 'надо', 'кажется', 'казаться', 'пожалуй',
        'хотеть', 'должный', 'хотеться'
    ]

    COLUMNS_NEEDED = [
        'inA2', 'kellyC2', 'simple850', 'simple1000', 'simple2000',
        'dale3000', 'infr1000', 'infr3000', 'infr5000', 'infr10000',
        'lex_abstract', 'formula_smog', 'mean_len_word', 'median_len_word',
        'median_len_sentence', 'mean_len_sentence', 'percent_of_long_words',
        'mean_punct_per_sentence', 'median_punct_per_sentence',
        'contentPOS', 'kotoryi/words', 'modal_verbs', 'conj_adversative',
        'kotoryi/sentences', 'passive', 'A', 'ADV', 'ADVPRO', 'ANUM',
        'APRO', 'COM', 'CONJ', 'INTJ', 'NUM', 'PART', 'PR', 'S', 'SPRO',
        'V', 'наст', 'непрош', 'прош', 'вин', 'дат', 'им', 'пр', 'род',
        'твор', 'ед', 'мн', 'деепр', 'изъяв', 'инф', 'пов', 'прич', 'кр',
        'полн', 'притяж', '1-л', '2-л', '3-л', 'жен', 'муж', 'сред', 'несов',
        'сов', 'действ', 'страд', 'неод', 'од', 'нп', 'пе'
    ]

    COLUMNS_OUTPUT = [ 'text_ok', 'text_error_message', 'level_number', 'level_comment', 'level_int', 'words', 'sentences',
                       'unique_words', 'reading_for_detail_speed', 'skim_reading_speed', 'key_words', 'cool_words',
                       'inA1', 'not_inA1', 'inA2', 'not_inA2', 'inB1', 'not_inB1', 'inB2', 'not_inB2', 'inC1', 'not_inC1',
                       'rare_words', 'cool_but_not_in_slovnik', 'gram_complex'
    ]

    GRAM_FEATURES = [ 'A', 'ADV', 'ADVPRO', 'ANUM', 'APRO', 'COM', 'CONJ', 'INTJ',
        'NUM', 'PART', 'PR', 'S', 'SPRO', 'V', 'непрош', 'прош',
        'им', 'пр', 'род', 'твор', 'деепр', 'изъяв', 'инф', 'пов',
        'прич', 'кр', 'полн', 'притяж', '1-л', 'сред', 'несов',
        'сов', 'действ', 'страд', 'неод', 'од'
    ]

    # растянутая шкала от 0 до 10
    INTERPRETER = [("A1. Элементарный уровень.", 0, 1.4),
                   ("Начало A2. Базовый уровень.", 1.5, 1.8),
                   ("Середина A2. Базовый уровень.", 1.9, 2.2),
                   ("Конец A2. Базовый уровень.", 2.3, 2.8),
                   ("Начало B1.  I сертификационный уровень.", 2.9, 3.5),
                   ("Середина B1. I сертификационный уровень.", 3.6, 4.9),
                   ("Конец B1. I сертификационный уровень.", 5, 6),
                   ("Начало B2. II сертификационный уровень.", 6.1, 6.3),
                   ("Середина B2. II сертификационный уровень.", 6.4, 7.7),
                   ("Конец B2. II сертификационный уровень.", 7.8, 8.1),
                   ("Начало C1. III сертификационный уровень.", 8.2, 8.5),
                   ("Середина C1. III сертификационный уровень.", 8.6, 8.9),
                   ("Конец C1. III сертификационный уровень.", 9, 9.2),
                   ("C2, уровень носителя. IV сертификационный уровень.", 9.3, 9.5),
                   ("ой-ой-ой, этот текст сложный даже для носителя", 9.5, 10)]

    # Список потенциально сложных тем
    GR_FEATURES = [
        'A', 'ADV', 'ADVPRO', 'ANUM', 'APRO',
        'NUM', 'SPRO', 'им', 'пр', 'род', 'твор', 'деепр', 'пов',
        'прич', 'кр', 'полн', 'притяж', 'несов',
        'сов', 'modal_verbs', 'passive'
    ]

    GR_FEATURES_NAMES = [
        'Прилагательные', 'Наречия', 'Наречия',
        'Порядковые числительные', 'Прилагательные',
        'Числительные', 'Местоимения', 'Именительный падеж',
        'Предложный падеж', 'Родительный падеж',
        'Творительный падеж', 'Деепричастия',
        'Повелительное наклонение', 'Причастия',
        'Краткие формы прилагательных и причастий',
        'Краткие формы прилагательных и причастий',
        'Притяжательные местоимения', 'Вид глагола',
        'Вид глагола', 'Модальные глаголы', 'Пассивные формы'
    ]

    READING_FOR_DETAIL_SPEED_NORM = [10, 30, 50, 50, 100, 120, 120, 120]

    SKIM_READING_SPEED_NORM = [20, 50, 100, 300, 400, 500, 500, 500]

    def __init__(self):

        print('Init Analyzer_foreign')

        self.mystem = pymystem3.Mystem(entire_input=False, disambiguation=True)

        self.ridge = linear_model.Ridge(alpha=0.1)

        self.features = pd.read_csv('data/list_of_features_1207.csv')

        # словники
        self.slovnik_A1_list = self.__load('data/new_vocab_a1.txt')
        self.slovnik_A2_list = self.__load('data/new_vocab_a2.txt')
        self.slovnik_B1_list = self.__load('data/new_vocab_b1.txt')
        self.slovnik_B2_list = self.__load('data/new_vocab_b2.txt')
        self.slovnik_C1_list = self.__load('data/new_vocab_c1.txt')

        # списки kelly
        self.kelly_A1_list = self.__load('data/kelly_a1.txt')
        self.kelly_A2_list = self.__load('data/kelly_a2.txt')
        self.kelly_B1_list = self.__load('data/kelly_b1.txt')
        self.kelly_B2_list = self.__load('data/kelly_b2.txt')
        self.kelly_C1_list = self.__load('data/kelly_c1.txt')
        self.kelly_C2_list = self.__load('data/kelly_c2.txt')

        # списки частотных слов
        self.fr_100_list = self.__load('data/fr_100.txt')
        self.fr_300_list = self.__load('data/fr_300.txt')
        self.fr_500_list = self.__load('data/fr_500.txt')
        self.fr_1000_list = self.__load('data/fr_1000.txt')
        self.fr_3000_list = self.__load('data/fr_3000.txt')
        self.fr_5000_list = self.__load('data/fr_5000.txt')
        self.fr_10000_list = self.__load('data/fr_10000.txt')
        self.fr_more_than_5list = self.__load('data/fr_more_than_5ipm.txt')
        self.fr_spoken_list = self.__load('data/fr_spoken.txt')

        # списки слов
        self.simple_russian_850_list = self.__load('data/SimpleRussian850.txt')
        self.simple_russian_1000_list = self.__load('data/simple_russian.txt')
        self.simple_russian_2000_list = self.__load('data/SimpleRussian2000.txt')
        self.brown_russian_10000_list = self.__load('data/Brown10000.txt')
        self.dale_russian_3000_list = self.__load('data/DaleRussian3000.txt')
        self.stop_list = self.__load('data/stop_list.txt')

        # семантические списки
        self.lex_abstract_list = self.__load('data/lex_abstract.txt')

        # считали датафрейм
        self.corpus_rnc = pd.read_csv('data/freq_rnc.csv', quotechar='`')
        self.lemmas_list_rnc = list(self.corpus_rnc['lemma'])

        # создаем словарь и будем в него все складывать
        self.data_about_text = {}
        self.whole_lemmas_list = []
        self.noun_list = []
        self.bastard_list = []
        self.geo_imen_list = []
        self.conj_adversative_list = []  # противительные союзы
        self.modal_words_list = []
        self.words_length_list = []
        self.number_of_syllables_list = []
        self.long_words_list = []  # слова более чем из 4 слогов
        self.long_words_len_list = []
        self.count_kotoryi = []
        self.count_content_pos = []
        self.count_passive = []

        # Обучаем модель
        # x_train, y_train = self.features[Analyzer_foreign.COLUMNS_NEEDED], self.features['level']
        # self.ridge.fit(x_train, y_train)
        # dump(self.ridge, 'data/model.joblib')
        
        # Загружаем уже обученную модель
        self.ridge = load('data/model.joblib')


    # считаем слоги и буквы
    def __count_syllables(self, element):
        i_text = element.get('text')
        i_text_syl_counter = 0
        for ii in i_text:
            if ii in Analyzer_foreign.SYLLABLES:
                # print('marker')
                i_text_syl_counter += 1
        for i in Analyzer_foreign.TWO_VOWELS:
            if i_text.find(i) != -1:
                # print('two')
                i_text_syl_counter -= 1
        if i_text == 'его':
            i_text_syl_counter == 1
        if i_text_syl_counter == 0:
            i_text_syl_counter == 1
        self.number_of_syllables_list.append(i_text_syl_counter)
        self.words_length_list.append(len(i_text))
        if i_text_syl_counter >= 4:
            self.long_words_len_list.append(i_text_syl_counter)
            self.long_words_list.append(i_text)
        return True

    # чистимся от имен, геообъектов и бастардов
    def __clean_from_name_geo_bastard(self, element):
        self.whole_lemmas_list.append(element.get('analysis')[0]['lex'])
        gr_info = element.get('analysis')[0]['gr']
        if 'qual' in element.get('analysis')[0]:
            if element.get('analysis')[0]['qual'] == 'bastard':
                self.bastard_list.append(element.get('text'))
        if gr_info.find('имя') > 0 or gr_info.find('гео') > 0:
            self.geo_imen_list.append(element.get('analysis')[0]['lex'])
        if gr_info.find('фам') > 0 or gr_info.find('отч') > 0:
            self.geo_imen_list.append(element.get('analysis')[0]['lex'])
        if (
                element.get('analysis')[0]['lex'] == 'но' or
                element.get('analysis')[0]['lex'] == 'а' or
                element.get('analysis')[0]['lex'] == 'однако' or
                element.get('analysis')[0]['lex'] == 'зато'
        ):
            self.conj_adversative_list.append(element.get('analysis')[0]['lex'])
        if element.get('analysis')[0]['lex'] in Analyzer_foreign.MODAL_WORDS:
            self.modal_words_list.append(element.get('analysis')[0]['lex'])
        if element.get('analysis')[0]['lex'] == 'который':
            self.count_kotoryi.append(element.get('analysis')[0]['lex'])
        return True

    # подсчет грам. информации
    def __count_gram(self, element):
        gr_info = element.get('analysis')[0]['gr']
        gr_info = gr_info.replace(',', '<b>')
        gr_info = gr_info.replace('=', '<b>')
        gr_info = gr_info.split('<b>')
        for i in Analyzer_foreign.GRAM_FEATURES:
            if i in gr_info:
                self.dict_of_features[i] += 1
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

    # считаем пунктуацию по предложениям
    def __punctuation_per_sentence(self, element):
        list_punctuation_score = []
        punctuation = [',', '-', ':', ';', '—']
        for i in self.sentences:
            counter = 0
            for ii in i:
                if ii in punctuation:
                    counter += 1
            list_punctuation_score.append(counter)
        return list_punctuation_score

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
            percent = len(known_words) / len(element)
            return percent

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

    # Изучающее чтение текста должно занять m мин
    def __output_of_min(self, element):
        if element >= 1:
            output_int = round(element)
            output_str = str(output_int) + ' мин.'
        else:
            output_sek = (round(element * 6) * 10) + 10
            output_str = str(output_sek) + ' сек.'
        return output_str

    def start(self, raw_text):

        print('Start Analyzer_foreign')

        # создаем словарь и будем в него все складывать
        self.data_about_text = {}
        self.whole_lemmas_list = []
        self.noun_list = []
        self.bastard_list = []
        self.geo_imen_list = []
        self.conj_adversative_list = []  # противительные союзы
        self.modal_words_list = []
        self.words_length_list = []
        self.number_of_syllables_list = []
        self.long_words_list = []  # слова более чем из 4 слогов
        self.long_words_len_list = []
        self.count_kotoryi = []
        self.count_content_pos = []
        self.count_passive = []

        text = self.__clean_text(raw_text)

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

        # создаем словарь со всеми данными из текста
        self.dict_of_features = defaultdict(int)

        for i in Analyzer_foreign.GRAM_FEATURES:
            self.dict_of_features[i] = 0

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

        # меняем значения в словаре с простых счетчиков на процент
        # встречаемости в тексте
        for i in Analyzer_foreign.GRAM_FEATURES:
            self.dict_of_features[i] = self.dict_of_features[i] / len(self.whole_lemmas_list)

        clean_lemmas_list = [
            f for f in self.whole_lemmas_list if
            f not in self.geo_imen_list and f not in self.bastard_list and f not in self.stop_list
        ]

        self.__set_numbers_about_text(clean_lemmas_list)

        self.whole_analyzed_text.clear()
        analyzed_bigrams.clear()

        # из словаря признаков делаем список
        features_for_test_text = []
        for ii in Analyzer_foreign.COLUMNS_NEEDED:
            # словарь с признаками
            features_for_test_text.append(self.dict_of_features[ii])

        test_features_array = np.array(features_for_test_text)
        test_features_array = test_features_array.reshape(1, -1)

        prediction = self.__predict(test_features_array)

        self.__tell_me_about_text(prediction, clean_lemmas_list)

        return self.data_about_text


    # Собираем цифры про текст в словарь, который потом подадим модели.
    def __set_numbers_about_text(self, clean_lemmas_list):
        all_words = len(self.whole_analyzed_text)
        all_len_words = [len(f) for f in self.whole_lemmas_list]
        all_syllables = sum(self.number_of_syllables_list)
        all_len_sentences = [len(f.split(' ')) for f in self.sentences]
        all_sentences = len(self.sentences)
        long_words = len(self.long_words_list)
        unique_lemmas_list = list(set(self.whole_lemmas_list))

        noun_unique_list = list(set(self.noun_list))  # список уникальных сущ.

        # всего слов в тексте
        self.dict_of_features['words'] = (len(self.whole_analyzed_text))
        # всего предложений в тексте
        self.dict_of_features['sentences'] = (len(self.sentences))
        # средняя длина слова в тексте
        self.dict_of_features['mean_len_word'] = (sum(self.words_length_list)) / all_words
        self.dict_of_features['median_len_word'] = statistics.median(all_len_words)
        self.dict_of_features['median_len_sentence'] = statistics.median(all_len_sentences)

        # средняя длина предложения в тексте
        self.dict_of_features['mean_len_sentence'] = all_words / all_sentences
        self.dict_of_features['mean_len_word_in_syllables'] = all_syllables / all_words
        self.dict_of_features['percent_of_long_words'] = long_words / all_words

        # type-token ratio - number of types and the number of tokens -
        # lexical variety
        self.dict_of_features['tt_ratio'] = (len(unique_lemmas_list) / len(self.whole_lemmas_list))

        # Среднее количество модальных глаголов и противительных союзов
        # на предложение
        self.dict_of_features['conj_adversative'] = (
                len(self.conj_adversative_list) / all_sentences
        )
        self.dict_of_features['modal_verbs'] = len(self.modal_words_list) / all_words
        self.dict_of_features['kotoryi/words'] = (
                len(self.count_kotoryi) / len(self.whole_lemmas_list)
        )
        self.dict_of_features['kotoryi/sentences'] = len(self.count_kotoryi) / all_sentences
        self.dict_of_features['contentPOS'] = (
                len(self.count_content_pos) / len(self.whole_lemmas_list)
        )
        self.dict_of_features['passive'] = len(self.count_passive)

        # формулы читабельности (адаптированные, из Бегтина)
        self.dict_of_features['formula_smog'] = (30 * (long_words / all_sentences)) ** 0.5

        # Доля слов, входящих в лексические минимумы
        self.dict_of_features['inA1'] = self.__percent_of_known_words(
            clean_lemmas_list,
            self.slovnik_A1_list
        )
        self.dict_of_features['inA2'] = self.__percent_of_known_words(
            clean_lemmas_list,
            self.slovnik_A2_list
        )
        self.dict_of_features['inB1'] = self.__percent_of_known_words(
            clean_lemmas_list,
            self.slovnik_B1_list
        )
        self.dict_of_features['inB2'] = self.__percent_of_known_words(
            clean_lemmas_list, self.slovnik_B2_list
        )
        self.dict_of_features['inC1'] = self.__percent_of_known_words(
            clean_lemmas_list, self.slovnik_C1_list
        )

        # Доля слов, входящих в списки Kelly
        self.dict_of_features['kellyA1'] = self.__percent_of_known_words(
            clean_lemmas_list, self.kelly_A1_list
        )
        self.dict_of_features['kellyA2'] = self.__percent_of_known_words(
            clean_lemmas_list, self.kelly_A2_list
        )
        self.dict_of_features['kellyB1'] = self.__percent_of_known_words(
            clean_lemmas_list, self.kelly_B1_list
        )
        self.dict_of_features['kellyB2'] = self.__percent_of_known_words(
            clean_lemmas_list, self.kelly_B2_list
        )
        self.dict_of_features['kellyC1'] = self.__percent_of_known_words(
            clean_lemmas_list, self.kelly_C1_list
        )
        self.dict_of_features['kellyC2'] = self.__percent_of_known_words(
            clean_lemmas_list, self.kelly_C2_list
        )

        # Доля слов, входящих в частотные списки
        self.dict_of_features['infr100'] = self.__percent_of_known_words(
            clean_lemmas_list, self.fr_100_list
        )
        self.dict_of_features['infr300'] = self.__percent_of_known_words(
            clean_lemmas_list, self.fr_300_list
        )
        self.dict_of_features['infr500'] = self.__percent_of_known_words(
            clean_lemmas_list, self.fr_500_list
        )
        self.dict_of_features['infr1000'] = self.__percent_of_known_words(
            clean_lemmas_list, self.fr_1000_list
        )
        self.dict_of_features['infr3000'] = self.__percent_of_known_words(
            clean_lemmas_list, self.fr_3000_list
        )
        self.dict_of_features['infr5000'] = self.__percent_of_known_words(
            clean_lemmas_list, self.fr_5000_list
        )
        self.dict_of_features['infr10000'] = self.__percent_of_known_words(
            clean_lemmas_list, self.fr_10000_list
        )
        self.dict_of_features['infr_more_than_5'] = self.__percent_of_known_words(
            clean_lemmas_list, self.fr_more_than_5list
        )
        self.dict_of_features['infr_spoken'] = self.__percent_of_known_words(
            clean_lemmas_list, self.fr_spoken_list
        )

        # Доля слов, которую покрывает Simple Russian
        self.dict_of_features['simple850'] = self.__percent_of_known_words(
            clean_lemmas_list, self.simple_russian_850_list
        )
        self.dict_of_features['simple1000'] = self.__percent_of_known_words(
            clean_lemmas_list, self.simple_russian_1000_list
        )
        self.dict_of_features['simple2000'] = self.__percent_of_known_words(
            clean_lemmas_list, self.simple_russian_2000_list
        )
        self.dict_of_features['dale3000'] = self.__percent_of_known_words(
            clean_lemmas_list, self.dale_russian_3000_list
        )
        self.dict_of_features['brown10000'] = self.__percent_of_known_words(
            clean_lemmas_list, self.brown_russian_10000_list
        )

        # Доля абстрактных/конкретных сущ. от всех сущ.
        self.dict_of_features['lex_abstract'] = self.__percent_of_known_words(
            noun_unique_list, self.lex_abstract_list
        )

        self.dict_of_features['unique_words'] = len(unique_lemmas_list)

        # Доля названий и бастардов
        self.dict_of_features['lex_names_and_geo'] = len(self.geo_imen_list)
        self.dict_of_features['lex_bastards'] = len(self.bastard_list)

        # Среднее количество модальных глаголов и противительных
        # союзов на предложение
        self.dict_of_features['conj_adversative'] = (
                len(self.conj_adversative_list) / len(self.sentences)
        )
        self.dict_of_features['modal_verbs'] = len(self.modal_words_list) / all_words
        self.dict_of_features['kotoryi/words'] = (
                len(self.count_kotoryi) / len(self.whole_lemmas_list)
        )
        self.dict_of_features['kotoryi/sentences'] = len(self.count_kotoryi) / len(self.sentences)
        self.dict_of_features['contentPOS'] = (
                len(self.count_content_pos) / len(self.whole_lemmas_list)
    )
   
    # Делаем предсказание
    def __predict(self, y):
        prediction = self.ridge.predict(y)
        if prediction < 0:
            prediction = 0
        return prediction

    # Принимает на вход уровень текста и выдает статистику
    def __tell_me_about_text(self, element, clean_lemmas_list):

        prediction = element

        if prediction > 0:
            prediction = round(prediction[0], 1)
        if prediction < 0:
            prediction = 0
        if prediction > 7:
            prediction = 7

        # округленный до целых уровень, чтобы потом анализировать по
        # средним значениям для этого уровня
        level_int = round(prediction)
        if level_int > 6:
            level_int = 6

        level_comment = ''
        # уровень * 1.4, чтобы растянуть шкалу
        level_for_scale = round((prediction * 1.4), 1)

        for i in Analyzer_foreign.INTERPRETER:
            if i[1] <= level_for_scale <= i[2]:
                level_comment = i[0]

        self.data_about_text['level_number'] = prediction
        self.data_about_text['level_comment'] = level_comment
        self.data_about_text['level_int'] = level_int
        f_by_levels = [
            self.features.iloc[:, :][self.features['level'] == 0],
            self.features.iloc[:, :][self.features['level'] == 1],
            self.features.iloc[:, :][self.features['level'] == 2],
            self.features.iloc[:, :][self.features['level'] == 3],
            self.features.iloc[:, :][self.features['level'] == 4],
            self.features.iloc[:, :][self.features['level'] == 5],
            self.features.iloc[:, :][self.features['level'] == 6]
        ]

        slovnik_by_levels = [
            self.slovnik_A1_list, self.slovnik_A2_list, self.slovnik_B1_list,
            self.slovnik_B2_list, self.slovnik_C1_list
        ]
        kelly_by_levels = [
            self.kelly_A1_list, self.kelly_A2_list, self.kelly_B1_list,
            self.kelly_B2_list, self.kelly_C1_list
        ]

        # Начинаем анализ
        # Слов в тексте
        self.data_about_text['words'] = self.dict_of_features['words']

        # Предложений
        self.data_about_text['sentences'] = self.dict_of_features['sentences']

        self.data_about_text['unique_words'] = self.dict_of_features['unique_words']


        # Изучающее чтение текста должно занять m мин
        self.data_about_text['reading_for_detail_speed'] = self.__output_of_min(
            self.dict_of_features['words'] / Analyzer_foreign.READING_FOR_DETAIL_SPEED_NORM[level_int]
        )

        # Просмотровое чтение текста должно занять m мин
        self.data_about_text['skim_reading_speed'] = self.__output_of_min(
            self.dict_of_features['words'] / Analyzer_foreign.SKIM_READING_SPEED_NORM[level_int])

        # Блок лексики:
        # 1. Считаем ключевые слова по tf/idf

        bag_tf_idf = dict()
        # берем только основные части речи
        for item in self.count_content_pos:
            if (
                    item not in self.bastard_list and
                    item not in self.geo_imen_list and
                    item not in self.slovnik_A1_list and
                    self.whole_lemmas_list.count(item) > 1
            ):
                if item in self.lemmas_list_rnc:
                    # если омонимы, берем cамый частотный
                    if self.lemmas_list_rnc.count(item) > 1:
                        idf = float(list(self.corpus_rnc[self.corpus_rnc['lemma'] == item]['idf'])[0])
                    else:
                        idf = float(self.corpus_rnc[self.corpus_rnc['lemma'] == item]['idf'])
                else:
                    idf = 0
                bag_tf_idf[item] = (
                        (self.whole_lemmas_list.count(item) / len(self.whole_lemmas_list)) / (0.00001 + idf))
        sorted_bag = (sorted(bag_tf_idf.items(), key=lambda x: x[1], reverse=True))

        self.data_about_text['key_words'] = [f[0] for f in sorted_bag[:5] if len(f[0]) > 2]

        # Списки с минимумов
        self.data_about_text['inA1'] = round(self.dict_of_features['inA1'] * 100)
        self.data_about_text['not_inA1'] = list(set([
            f for f in clean_lemmas_list if f not in self.slovnik_A1_list]))

        self.data_about_text['inA2'] = round(self.dict_of_features['inA2'] * 100)
        self.data_about_text['not_inA2'] = list(set([
            f for f in clean_lemmas_list if f not in self.slovnik_A2_list]))

        self.data_about_text['inB1'] = round(self.dict_of_features['inB1'] * 100)
        self.data_about_text['not_inB1'] = list(set([
            f for f in clean_lemmas_list if f not in self.slovnik_B1_list]))

        self.data_about_text['inB2'] = round(self.dict_of_features['inB2'] * 100)
        self.data_about_text['not_inB2'] = list(set([
            f for f in clean_lemmas_list if f not in self.slovnik_B2_list]))

        self.data_about_text['inC1'] = round(self.dict_of_features['inC1'] * 100)
        self.data_about_text['not_inC1'] = list(set([
            f for f in clean_lemmas_list if f not in self.slovnik_C1_list]))

        # Можем работать с лексическими списками только до 4 уровня,
        # дальше их не существует
        self.data_about_text['cool_words'] = []
        self.data_about_text['rare_words'] = []
        self.data_about_text['cool_but_not_in_slovnik'] = []

        if level_int < 4:

            # Самые полезные слова
            cool_words = list(set(
                [
                    f for f in clean_lemmas_list
                    if f not in slovnik_by_levels[(level_int - 1)]
                       and (f in self.fr_3000_list
                            or f in kelly_by_levels[level_int]
                            or self.whole_lemmas_list.count(f) > 2)
                ]
            ))
            self.data_about_text['cool_words'] = cool_words

            # Избавиться от этих слов
            self.data_about_text['rare_words'] = list(set(
                [
                    f for f in clean_lemmas_list
                    if (
                        f not in cool_words
                        and f not in slovnik_by_levels[level_int]
                        and f not in kelly_by_levels[level_int]
                        and f not in self.data_about_text['key_words']
                        and (f not in self.fr_10000_list
                             or f in self.bastard_list)
                )
                ]
            ))

            # нет в словнике есть в Келли
            self.data_about_text['cool_but_not_in_slovnik'] = list(set(
                [
                    f for f in clean_lemmas_list
                    if (
                        f not in slovnik_by_levels[level_int]
                        and f in kelly_by_levels[level_int]
                        and f in self.fr_3000_list
                )
                ]
            ))

        else:
            # Самые полезные слова
            cool_words_more_4 = list(set(
                [
                    f for f in clean_lemmas_list
                    if (f not in slovnik_by_levels[3]
                        and (f in slovnik_by_levels[4]
                             or f in self.fr_5000_list
                             or f in kelly_by_levels[4]
                             or self.whole_lemmas_list.count(f) > 3))
                ]
            ))
            self.data_about_text['cool_words'] = cool_words_more_4

            # Избавиться от этих слов
            rare_words_more_4 = list(set(
                [
                    f for f in clean_lemmas_list
                    if (
                        f not in cool_words_more_4
                        and f not in slovnik_by_levels[4]
                        and f not in self.data_about_text['key_words']
                        and (f not in self.fr_10000_list
                             or f in self.bastard_list)
                )
                ]
            ))
            self.data_about_text['rare_words'] = rare_words_more_4

        gram_complex = []

        for i in Analyzer_foreign.GR_FEATURES:
            compare = self.dict_of_features[i] / (np.mean(f_by_levels[level_int][i] + 0.00000001))
            if compare > 2:
                gram_complex.append(Analyzer_foreign.GR_FEATURES_NAMES[Analyzer_foreign.GR_FEATURES.index(i)])

        self.data_about_text['gram_complex'] = list(set(gram_complex))

        return True