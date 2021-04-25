# Объединенный файл из двух аналайзеров, для РКИ и для родного.

import re
import statistics
from collections import defaultdict

import nltk
import numpy as np
import pandas as pd
import pymystem3
from joblib import load
from nltk.tokenize import sent_tokenize
from sklearn import linear_model


class Analyzer:
    SYLLABLES = ["а", "е", "ё", "и", "о", "у", "ы", "ю", "я", "э"]

    TWO_VOWELS = [
        "ия",
        "ии",
        "ые",
        "ие",
        "ио",
        "ию",
        "иу",
        "ее",
        "ею",
        "ея",
        "ою",
        "ая",
        "яя",
        "ое",
        "аю",
        "аэ",
        "ье",
        "ья",
        "еа",
        "ау",
        "ую",
        "юю",
        "эт",
    ]

    MODAL_WORDS = [
        "хочется",
        "нужно",
        "надо",
        "кажется",
        "казаться",
        "пожалуй",
        "хотеть",
        "должный",
        "хотеться",
    ]

    COLUMNS_NEEDED_FOREIGN = [
        "inA2",
        "kellyC2",
        "simple850",
        "simple1000",
        "simple2000",
        "dale3000",
        "infr1000",
        "infr3000",
        "infr5000",
        "infr10000",
        "lex_abstract",
        "formula_smog",
        "mean_len_word",
        "median_len_word",
        "median_len_sentence",
        "mean_len_sentence",
        "percent_of_long_words",
        "mean_punct_per_sentence",
        "median_punct_per_sentence",
        "contentPOS",
        "kotoryi/words",
        "modal_verbs",
        "conj_adversative",
        "kotoryi/sentences",
        "passive",
        "A",
        "ADV",
        "ADVPRO",
        "ANUM",
        "APRO",
        "COM",
        "CONJ",
        "INTJ",
        "NUM",
        "PART",
        "PR",
        "S",
        "SPRO",
        "V",
        "наст",
        "непрош",
        "прош",
        "вин",
        "дат",
        "им",
        "пр",
        "род",
        "твор",
        "ед",
        "мн",
        "деепр",
        "изъяв",
        "инф",
        "пов",
        "прич",
        "кр",
        "полн",
        "притяж",
        "1-л",
        "2-л",
        "3-л",
        "жен",
        "муж",
        "сред",
        "несов",
        "сов",
        "действ",
        "страд",
        "неод",
        "од",
        "нп",
        "пе",
    ]

    COLUMNS_NEEDED_NATIVE = [
        "words",
        "unique_words",
        "sentences",
        "mean_len_word",
        "mean_len_sentence",
        "formula_flesh_oborneva",
        "formula_flesh_kinc_oborneva",
        "formula_pushkin",
        "formula_pushkin_100",
        "level_comment",
        "structure_complex",
        "lexical_complex",
        "narrativity",
        "description",
        "tt_ratio",
        "lex_density",
        "lexical_complex_rki",
        "laposhina_list",
        "detcorpus_5000",
        "rki_children_list",
        "rare_words",
        "frequency_bag",
    ]

    COLUMNS_OUTPUT = [
        "text_ok",
        "text_error_message",
        "level_number",
        "level_comment",
        "level_int",
        "words",
        "sentences",
        "unique_words",
        "tt_ratio",
        "reading_for_detail_speed",
        "skim_reading_speed",
        "key_words",
        "cool_words",
        "inA1",
        "not_inA1",
        "inA2",
        "not_inA2",
        "inB1",
        "not_inB1",
        "inB2",
        "not_inB2",
        "inC1",
        "not_inC1",
        "infr5000",
        "rare_words",
        "cool_but_not_in_slovnik",
        "gram_complex",
        "frequency_bag",
    ]

    GRAM_FEATURES = [
        "A",
        "ADV",
        "ADVPRO",
        "ANUM",
        "APRO",
        "COM",
        "CONJ",
        "INTJ",
        "NUM",
        "PART",
        "PR",
        "S",
        "SPRO",
        "V",
        "непрош",
        "прош",
        "им",
        "пр",
        "род",
        "твор",
        "деепр",
        "изъяв",
        "инф",
        "пов",
        "прич",
        "кр",
        "полн",
        "притяж",
        "1-л",
        "сред",
        "несов",
        "сов",
        "действ",
        "страд",
        "неод",
        "од",
    ]

    # Список потенциально сложных тем
    DIFFICULT_GRAM = [
        "A",
        "ADV",
        "ADVPRO",
        "ANUM",
        "APRO",
        "NUM",
        "SPRO",
        "им",
        "пр",
        "род",
        "твор",
        "деепр",
        "пов",
        "прич",
        "кр",
        "полн",
        "притяж",
        "несов",
        "сов",
        "modal_verbs",
        "passive",
    ]

    GR_FEATURES_NAMES = [
        "Прилагательные",
        "Наречия",
        "Наречия",
        "Порядковые числительные",
        "Прилагательные",
        "Числительные",
        "Местоимения",
        "Именительный падеж",
        "Предложный падеж",
        "Родительный падеж",
        "Творительный падеж",
        "Деепричастия",
        "Повелительное наклонение",
        "Причастия",
        "Краткие формы прилагательных и причастий",
        "Краткие формы прилагательных и причастий",
        "Притяжательные местоимения",
        "Вид глагола",
        "Вид глагола",
        "Модальные глаголы",
        "Пассивные формы",
    ]

    READING_FOR_DETAIL_SPEED_NORM = [10, 30, 50, 50, 100, 120, 120, 120]

    SKIM_READING_SPEED_NORM = [20, 50, 100, 300, 400, 500, 500, 500]

    # растянутая шкала от 0 до 10
    INTERPRETER_FOREIGN = [
        ("A1. Элементарный уровень.", 0, 1.4),
        ("Начало A2. Базовый уровень.", 1.4, 1.8),
        ("Середина A2. Базовый уровень.", 1.8, 2.2),
        ("Конец A2. Базовый уровень.", 2.2, 2.8),
        ("Начало B1.  I сертификационный уровень.", 2.8, 3.5),
        ("Середина B1. I сертификационный уровень.", 3.5, 4.9),
        ("Конец B1. I сертификационный уровень.", 4.9, 6),
        ("Начало B2. II сертификационный уровень.", 6, 6.3),
        ("Середина B2. II сертификационный уровень.", 6.3, 7.7),
        ("Конец B2. II сертификационный уровень.", 7.7, 8.1),
        ("Начало C1. III сертификационный уровень.", 8.1, 8.5),
        ("Середина C1. III сертификационный уровень.", 8.5, 8.9),
        ("Конец C1. III сертификационный уровень.", 8.9, 9.2),
        ("C2, уровень носителя. IV сертификационный уровень.", 9.2, 9.5),
        ("ой-ой-ой, этот текст сложный даже для носителя", 9.5, 10),
    ]

    # шкала сложности, высчитывается от 0 до 10, примерно соответствует классу
    INTERPRETER_NATIVE = [
        ("Очень простой текст, подойдет для возраста 7-8 лет (1-2 класс).", 0, 20),
        ("Простой текст, подойдет для возраста 9-10 лет (3-4 класс).", 20, 40),
        (
            "Достаточно простой текст, подойдет для возраста 11-12 лет (5-6 класс).",
            40,
            60,
        ),
        ("Текст подойдет для возраста 13-15 лет (7-9 класс).", 60, 75),
        ("Текст подойдет для возраста 16-17 лет (10-11 класс).", 75, 85),
        ("Сложный текст, подойдет для студента ВУЗа и старше", 85, 91),
        ("Очень сложный текст, подойдет для выпускника ВУЗа и старше", 91, 100),
    ]

    def __init__(self):
        self.mystem = pymystem3.Mystem(entire_input=False, disambiguation=True)

        self.ridge = linear_model.Ridge(alpha=0.1)

        self.features = pd.read_csv("data/list_of_features_1207.csv")

        # словники
        self.slovnik_A1_list = self.__load("data/new_vocab_a1.txt")
        self.slovnik_A2_list = self.__load("data/new_vocab_a2.txt")
        self.slovnik_B1_list = self.__load("data/new_vocab_b1.txt")
        self.slovnik_B2_list = self.__load("data/new_vocab_b2.txt")
        self.slovnik_C1_list = self.__load("data/new_vocab_c1.txt")

        # списки kelly
        self.kelly_A1_list = self.__load("data/kelly_a1.txt")
        self.kelly_A2_list = self.__load("data/kelly_a2.txt")
        self.kelly_B1_list = self.__load("data/kelly_b1.txt")
        self.kelly_B2_list = self.__load("data/kelly_b2.txt")
        self.kelly_C1_list = self.__load("data/kelly_c1.txt")
        self.kelly_C2_list = self.__load("data/kelly_c2.txt")

        # списки частотных слов
        self.fr_100_list = self.__load("data/fr_100.txt")
        self.fr_300_list = self.__load("data/fr_300.txt")
        self.fr_500_list = self.__load("data/fr_500.txt")
        self.fr_1000_list = self.__load("data/fr_1000.txt")
        self.fr_3000_list = self.__load("data/fr_3000.txt")
        self.fr_5000_list = self.__load("data/fr_5000.txt")
        self.fr_10000_list = self.__load("data/fr_10000.txt")
        self.fr_more_than_5list = self.__load("data/fr_more_than_5ipm.txt")
        self.fr_spoken_list = self.__load("data/fr_spoken.txt")

        # списки слов
        self.simple_russian_850_list = self.__load("data/SimpleRussian850.txt")
        self.simple_russian_1000_list = self.__load("data/simple_russian.txt")
        self.simple_russian_2000_list = self.__load("data/SimpleRussian2000.txt")
        self.brown_russian_10000_list = self.__load("data/Brown10000.txt")
        self.dale_russian_3000_list = self.__load("data/DaleRussian3000.txt")
        self.stop_list = self.__load("data/stop_list.txt")

        # семантические списки
        self.lex_abstract_list = self.__load("data/lex_abstract.txt")

        # списки слов для родного
        self.laposhina_list = self.__load("data/laposhina_list_from_formula.txt")
        self.detcorpus_list = self.__load("data/detcorpus_5000.txt")
        self.rki_children_list = self.__load("data/rki_children_list.txt")
        self.united_list = self.__load("data/united_simple_list.txt")

        # считали датафрейм
        self.corpus_rnc = pd.read_csv("data/freq_rnc.csv", quotechar="`")
        self.lemmas_list_rnc = list(self.corpus_rnc["lemma"])

        # создаем словарь и будем в него все складывать
        self.data_about_text = {}
        self.whole_lemmas_list = []
        self.noun_list = []
        self.bastard_list = []
        self.names_list = []
        self.geo_name_list = []
        self.conj_adversative_list = []  # противительные союзы
        self.modal_words_list = []
        self.words_length_list = []
        self.number_of_syllables_list = []
        self.long_words_list = []  # слова более чем из 4 слогов
        self.long_words_len_list = []
        self.count_kotoryi = []
        self.count_content_pos = []
        self.count_passive = []
        self.whole_lemmas_minus_geo_and_stop = []

        # Обучаем модель
        # x_train, y_train = self.features[Analyzer_foreign.COLUMNS_NEEDED], self.features["level"]
        # self.ridge.fit(x_train, y_train)
        # dump(self.ridge, "data/model.joblib")

        # Загружаем уже обученную модель
        self.ridge = load("data/model.joblib")

    # считаем слоги и буквы
    def __count_syllables(self, element):
        i_text = element.get("text")
        i_text_syl_counter = 0
        for ii in i_text:
            if ii in Analyzer.SYLLABLES:
                i_text_syl_counter += 1
        for i in Analyzer.TWO_VOWELS:
            if i_text.find(i) != -1:
                i_text_syl_counter -= 1
        if i_text == "его":
            i_text_syl_counter = 1
        if i_text_syl_counter == 0:
            i_text_syl_counter = 1
        self.number_of_syllables_list.append(i_text_syl_counter)
        self.words_length_list.append(len(i_text))
        if i_text_syl_counter >= 4:
            self.long_words_len_list.append(i_text_syl_counter)
            self.long_words_list.append(i_text)
        return True

    # чистимся от имен, геообъектов и бастардов
    def __clean_from_name_geo_bastard(self, element):
        self.whole_lemmas_list.append(element.get("analysis")[0]["lex"])
        gr_info = element.get("analysis")[0]["gr"]
        if "qual" in element.get("analysis")[0]:
            if element.get("analysis")[0]["qual"] == "bastard":
                self.bastard_list.append(element.get("text"))
        if gr_info.find("гео") > 0:
            self.geo_name_list.append(element.get("analysis")[0]["lex"])
        if (
            gr_info.find("имя") > 0
            or gr_info.find("фам") > 0
            or gr_info.find("отч") > 0
        ):
            self.names_list.append(element.get("analysis")[0]["lex"])
        if (
            element.get("analysis")[0]["lex"] == "но"
            or element.get("analysis")[0]["lex"] == "а"
            or element.get("analysis")[0]["lex"] == "однако"
            or element.get("analysis")[0]["lex"] == "зато"
        ):
            self.conj_adversative_list.append(element.get("analysis")[0]["lex"])
        if element.get("analysis")[0]["lex"] in Analyzer.MODAL_WORDS:
            self.modal_words_list.append(element.get("analysis")[0]["lex"])
        if element.get("analysis")[0]["lex"] == "который":
            self.count_kotoryi.append(element.get("analysis")[0]["lex"])
        return True

    # подсчет грам. информации
    def __count_gram(self, element):
        gr_info = element.get("analysis")[0]["gr"]
        gr_info = gr_info.replace(",", "<b>")
        gr_info = gr_info.replace("=", "<b>")
        gr_info = gr_info.split("<b>")
        for i in Analyzer.GRAM_FEATURES:
            if i in gr_info:
                self.dict_of_features[i] += 1
        if "S" in gr_info:
            self.noun_list.append(element.get("analysis")[0]["lex"])
        if "S" in gr_info or "V" in gr_info or "A" in gr_info or "ADV" in gr_info:
            self.count_content_pos.append(element.get("analysis")[0]["lex"])
        return True

    def __count_passive_form(self, element):
        if element[0].get("analysis") and element[1].get("analysis"):
            element0_gr = self.__get_gr_info(element[0])
            element1_gr = self.__get_gr_info(element[1])
            if element[0].get("analysis")[0]["lex"] == "быть" and "прош" in element0_gr:
                if "прич" in element1_gr:
                    self.count_passive.append(element[1].get("text"))
        return True

    # считаем пунктуацию по предложениям
    def __punctuation_per_sentence(self, element):
        list_punctuation_score = []
        punctuation = [",", "-", ":", ";", "—"]
        for i in self.sentences:
            counter = 0
            for ii in i:
                if ii in punctuation:
                    counter += 1
            list_punctuation_score.append(counter)
        return list_punctuation_score

    def __load(self, file_name):
        f = open(file_name, "r", encoding="utf_8")
        lines = f.readlines()
        f.close()
        return [line.replace("\n", "") for line in lines]

    def __get_gr_info(self, element):
        gr_info = element.get("analysis")[0]["gr"]
        gr_info = gr_info.replace(",", "<b>")
        gr_info = gr_info.replace("=", "<b>")
        gr_info = gr_info.split("<b>")
        return gr_info

    # Общий цикл просмотра анализа слов
    def __gram_analyze(self, element):
        for i in element:
            self.__count_syllables(i)
            if len(i.get("analysis")) > 0:
                self.__clean_from_name_geo_bastard(i)
                self.__count_gram(i)
        return True

    # Вычисляем процент слов из разных словников и частотных списков
    # todo: когда буду переписывать модель, унифицировать везде процент! Оставить тот который _100
    def __percent_of_known_words(self, element, list_of_words):
        if len(list_of_words) == 0 or len(element) == 0:
            return 0
        else:
            known_words = [w for w in element if w in list_of_words]
            percent = round((len(known_words) / len(element)), 2)
            return percent

    def __percent_of_known_words_100(self, element, list_of_words):
        if len(list_of_words) == 0 or len(element) == 0:
            return 0
        else:
            known_words = [w for w in element if w in list_of_words]
            percent = round((len(known_words) / len(element)) * 100)
            return percent

    def __count_freq_by_rnc(self, element):
        if element in self.lemmas_list_rnc:
            # если омонимы, берем cамый частотный
            if self.lemmas_list_rnc.count(element) > 1:
                idf = float(
                    list(self.corpus_rnc[self.corpus_rnc["lemma"] == element]["idf"])[0]
                )
            else:
                idf = float(self.corpus_rnc[self.corpus_rnc["lemma"] == element]["idf"])
        else:
            idf = 0
        return idf

    def __get_frequency_bag(self, element):
        frequency_bag = dict()
        unique_lemmas = sorted(list(set(element)))
        for i in unique_lemmas:
            frequency_bag[i] = element.count(i)
        sorted_fr_bag = sorted(frequency_bag.items(), key=lambda x: x[1], reverse=True)
        return sorted_fr_bag

    def __clean_text(self, input_text):
        new_text = input_text.replace("­\n", "")
        new_text = new_text.replace("\n", " ")
        new_text = new_text.replace("•", "")
        new_text = new_text.replace("…", ".")
        new_text = new_text.replace("...", ".")
        new_text = new_text.replace("..", ".")
        new_text = new_text.replace("?.", "?")
        new_text = new_text.replace("!.", "!")
        new_text = new_text.replace("_", "")
        new_text = new_text.replace("!—", "! —")
        new_text = new_text.replace("?—", "? —")
        new_text = new_text.replace("\xad", "")
        return new_text

    # делим текст на предложения
    def __sent_tokenize_plus(self, this_text):
        new_text = this_text.replace("(с.", "(стр ")
        new_text = new_text.replace("на с.", "на стр")
        new_text = new_text.replace(".—", ". —")
        new_text = re.sub(r"([a-zа-я1-9])\.([A-ZА-Я])", "\\1. \\2", new_text)
        new_text = re.sub(r"([a-zа-я1-9])\!([A-ZА-Я])", "\\1! \\2", new_text)
        new_text = re.sub(r"([a-zа-я1-9])\?([A-ZА-Я])", "\\1? \\2", new_text)
        new_text = re.sub(r"(рис. )([1-9])", "рис \\2", new_text)
        # В г. Смоленске
        new_text = re.sub(r"( г. )([A-ZА-Я]{1})", " г<dot> \\2", new_text)
        # С.В. Морозов
        new_text = re.sub(
            r"([А-Я]{1}\.[А-Я]{1})\. ([A-ZА-Я]{1}[a-zа-я]+)", "\\1<dot> \\2", new_text
        )
        # достигает 55 см. в длину
        new_text = re.sub(r"( см. )([a-zа-я1-9])", " см<dot> \\2", new_text)

        sentences = sent_tokenize(new_text)

        new_sentences = []
        for i in sentences:
            # У лисички длина 3 м. А у котика - 2.
            if re.findall(r"([a-zа-я1-9])\. ([А-Я]{1})", i):
                i_new = re.sub(r"([a-zа-я1-9])\. ([А-Я]{1})", "\\1.<stop>\\2", i)
                i_split = i_new.split("<stop>")
                for ii in i_split:
                    new_sentences.append(ii)
                continue
            # И вы вырастили мух?- Нет пока.
            if re.findall(r"([a-zа-я1-9]\.|\?|\!)(- [А-Я]{1})", i):
                i_new = re.sub(r"([a-zа-я1-9]\.|\?|\!)(- [А-Я]{1})", "\\1<stop>\\2", i)
                i_split = i_new.split("<stop>")
                for ii in i_split:
                    new_sentences.append(ii)
                continue
            if re.findall(r"[а-яА-ЯёЁ]+", i):
                new_sentences.append(i)

        for i in new_sentences:
            i = i.replace("<dot>", ".")
        return new_sentences

    # Изучающее чтение текста должно занять m мин
    def __output_of_min(self, element):
        if element >= 1:
            output_int = round(element)
            output_str = str(output_int) + " мин."
        else:
            output_sek = round(element * 6) * 10
            if output_sek < 30:
                output_sek += 10
            output_str = str(output_sek) + " сек."
        return output_str

    def __output_ballov(self, element):
        ball_str = ""
        if element < 10:
            last_number = element
            if last_number == 1:
                ball_str = "балл"
            if 2 <= last_number <= 4:
                ball_str = "балла"
            if 5 <= last_number <= 9:
                ball_str = "баллов"
        else:
            last_number = element % 10
            if last_number == 1:
                ball_str = "балл"
            if 2 <= last_number <= 4:
                ball_str = "балла"
            if 5 <= last_number <= 9 or last_number == 0:
                ball_str = "баллов"
        return ball_str

    def __clear_fields(self):

        self.data_about_text = {}
        self.whole_lemmas_list = []
        self.noun_list = []
        self.bastard_list = []
        self.names_list = []
        self.geo_name_list = []
        self.conj_adversative_list = []  # противительные союзы
        self.modal_words_list = []
        self.words_length_list = []
        self.number_of_syllables_list = []
        self.long_words_list = []  # слова более чем из 4 слогов
        self.long_words_len_list = []
        self.count_kotoryi = []
        self.count_content_pos = []
        self.count_passive = []
        self.whole_lemmas_minus_geo_and_stop = []
        return True

    def __first_check_len_text(self, element):

        # первая проверка текста - не слишком маленький
        if len(element) < 10:
            self.data_about_text["text_ok"] = False
            self.data_about_text[
                "text_error_message"
            ] = "Введите текст на русском языке не менее 5 слов."
            return self.data_about_text

        # Вторая проверка текста - не слишком большой
        if len(element) > 10000:
            self.data_about_text["text_ok"] = False
            self.data_about_text[
                "text_error_message"
            ] = "Введите текст не более 10 000 знаков."
            return self.data_about_text

        self.data_about_text["text_ok"] = True
        self.data_about_text["text_error_message"] = ""

        return self.data_about_text

    def __second_check_len_text(self, element):
        if len(element) < 5:
            self.data_about_text["text_ok"] = False
            self.data_about_text[
                "text_error_message"
            ] = "Введите текст на русском языке не менее 5 слов."
            return self.data_about_text

        self.data_about_text["text_ok"] = True
        self.data_about_text["text_error_message"] = ""
        return self.data_about_text

    def __set_numbers_about_foreign_text(self, clean_lemmas_list):
        self.all_words = len(self.whole_analyzed_text)
        self.all_len_words = [len(f) for f in self.whole_lemmas_list]
        self.all_syllables = sum(self.number_of_syllables_list)
        self.all_len_sentences = [len(f.split(" ")) for f in self.sentences]
        self.all_sentences = len(self.sentences)
        self.long_words = len(self.long_words_list)
        self.unique_lemmas_list = list(set(self.whole_lemmas_list))

        self.noun_unique_list = list(set(self.noun_list))  # список уникальных сущ.

        self.whole_lemmas_minus_geo_and_stop = [
            f
            for f in self.whole_lemmas_list
            if f not in self.geo_name_list
            and f not in self.names_list
            and f not in self.stop_list
        ]

        # всего слов в тексте
        self.dict_of_features["words"] = len(self.whole_analyzed_text)
        # всего предложений в тексте
        self.dict_of_features["sentences"] = len(self.sentences)
        # средняя длина слова в тексте
        self.dict_of_features["mean_len_word"] = round(
            ((sum(self.words_length_list)) / self.all_words), 1
        )
        self.dict_of_features["median_len_word"] = statistics.median(self.all_len_words)
        self.dict_of_features["median_len_sentence"] = statistics.median(
            self.all_len_sentences
        )

        # средняя длина предложения в тексте
        self.dict_of_features["mean_len_sentence"] = round(
            (self.all_words / self.all_sentences), 1
        )
        self.dict_of_features["mean_len_word_in_syllables"] = round(
            (self.all_syllables / self.all_words), 1
        )
        self.dict_of_features["percent_of_long_words"] = round(
            (self.long_words / self.all_words), 2
        )

        # type-token ratio - number of types and the number of tokens -
        # lexical variety
        self.dict_of_features["tt_ratio"] = round(
            ((len(self.unique_lemmas_list) / len(self.whole_lemmas_list))), 2
        )

        # Среднее количество модальных глаголов и противительных союзов
        # на предложение
        self.dict_of_features["conj_adversative"] = (
            len(self.conj_adversative_list) / self.all_sentences
        )
        self.dict_of_features["modal_verbs"] = (
            len(self.modal_words_list) / self.all_words
        )
        self.dict_of_features["kotoryi/words"] = len(self.count_kotoryi) / len(
            self.whole_lemmas_list
        )
        self.dict_of_features["kotoryi/sentences"] = (
            len(self.count_kotoryi) / self.all_sentences
        )
        self.dict_of_features["contentPOS"] = round(
            (len(self.count_content_pos) / len(self.whole_lemmas_list)), 2
        )
        self.dict_of_features["passive"] = len(self.count_passive)

        # формулы читабельности (адаптированные, из Бегтина)
        self.dict_of_features["formula_smog"] = round(
            ((30 * (self.long_words / self.all_sentences)) ** 0.5), 2
        )

        self.dict_of_features["unique_words"] = len(self.unique_lemmas_list)

        # Доля названий и бастардов
        self.dict_of_features["lex_names_and_geo"] = len(self.names_list) + len(
            self.geo_name_list
        )
        self.dict_of_features["lex_bastards"] = len(self.bastard_list)

        LEXICAL_LISTS = {
            "inA1": self.slovnik_A1_list,
            "inA2": self.slovnik_A2_list,
            "inB1": self.slovnik_B1_list,
            "inB2": self.slovnik_B2_list,
            "inC1": self.slovnik_C1_list,
            "kellyA1": self.kelly_A1_list,
            "kellyA2": self.kelly_A2_list,
            "kellyB1": self.kelly_B1_list,
            "kellyB2": self.kelly_B2_list,
            "kellyC1": self.kelly_C1_list,
            "kellyC2": self.kelly_C2_list,
            "infr1000": self.fr_1000_list,
            "infr3000": self.fr_3000_list,
            "infr5000": self.fr_5000_list,
            "infr10000": self.fr_10000_list,
            "infr_more_than_5": self.fr_more_than_5list,
            "infr_spoken": self.fr_spoken_list,
            "simple850": self.simple_russian_850_list,
            "simple1000": self.simple_russian_1000_list,
            "simple2000": self.simple_russian_2000_list,
            "dale3000": self.dale_russian_3000_list,
        }

        # Доля слов, входящих в различные лексические списки
        for i in LEXICAL_LISTS:
            new_key = self.__percent_of_known_words(
                self.whole_lemmas_minus_geo_and_stop, LEXICAL_LISTS[i]
            )
            self.dict_of_features[i] = new_key

        # Доля абстрактных/конкретных сущ. от всех сущ.
        self.dict_of_features["lex_abstract"] = self.__percent_of_known_words(
            self.noun_unique_list, self.lex_abstract_list
        )

        return self.dict_of_features

    def start_foreign(self, raw_text):
        self.__clear_fields()

        text = self.__clean_text(raw_text)

        # первая проверка текста на длину
        self.data_about_text = self.__first_check_len_text(text)

        if self.data_about_text["text_ok"] is False:
            return self.data_about_text

        self.sentences = self.__sent_tokenize_plus(text)
        self.whole_analyzed_text = self.mystem.analyze(text)  # весь текст одним списком
        analyzed_bigrams = list(nltk.bigrams(self.whole_analyzed_text))  # биграммочки

        # создаем словарь со всеми данными из текста
        self.dict_of_features = defaultdict(int)

        for i in Analyzer.GRAM_FEATURES:
            self.dict_of_features[i] = 0

        # запускаем функцию со всеми грам. анализами
        self.__gram_analyze(self.whole_analyzed_text)

        # подсчитываем пассивные формы
        for i in analyzed_bigrams:
            self.__count_passive_form(i)

        # вторая проверка, не менее 5 слов
        self.data_about_text = self.__second_check_len_text(self.whole_lemmas_list)
        if self.data_about_text["text_ok"] is False:
            return self.data_about_text

        # меняем значения в словаре с простых счетчиков на процент
        # встречаемости в тексте
        for i in Analyzer.GRAM_FEATURES:
            self.dict_of_features[i] = round(
                (self.dict_of_features[i] / len(self.whole_lemmas_list)), 2
            )

        self.clean_lemmas_list = [
            f
            for f in self.whole_lemmas_list
            if f not in self.geo_name_list
            and f not in self.names_list
            and f not in self.bastard_list
            and f not in self.stop_list
        ]

        self.__set_numbers_about_foreign_text(self.clean_lemmas_list)

        self.whole_analyzed_text.clear()
        analyzed_bigrams.clear()

        # из словаря признаков делаем список
        features_for_test_text = []
        for ii in Analyzer.COLUMNS_NEEDED_FOREIGN:
            # словарь с признаками
            features_for_test_text.append(self.dict_of_features[ii])

        test_features_array = np.array(features_for_test_text)
        test_features_array = test_features_array.reshape(1, -1)

        prediction = self.__predict(test_features_array)

        self.__tell_me_about_text(prediction)

        return self.data_about_text

    # Делаем предсказание
    def __predict(self, y):
        prediction = self.ridge.predict(y)
        if prediction < 0:
            prediction = 0
        return prediction

    # Принимает на вход уровень текста и выдает статистику
    def __tell_me_about_text(self, element):

        prediction = element

        if prediction > 0:
            prediction = round(prediction[0], 1)
        if prediction < 0.5:
            prediction = 0.5
        if prediction > 7:
            prediction = 7

        # округленный до целых уровень, чтобы потом анализировать по
        # средним значениям для этого уровня
        level_int = round(prediction)
        if level_int > 6:
            level_int = 6

        level_comment = ""

        # уровень * 1.4, чтобы растянуть шкалу
        level_for_scale = round((prediction * 1.4), 1)

        for i in Analyzer.INTERPRETER_FOREIGN:
            if i[1] < level_for_scale <= i[2]:
                level_comment = i[0]

        self.data_about_text["level_number"] = prediction
        self.data_about_text["level_comment"] = level_comment
        self.data_about_text["level_int"] = level_int

        f_by_levels = [
            self.features.iloc[:, :][self.features["level"] == 0],
            self.features.iloc[:, :][self.features["level"] == 1],
            self.features.iloc[:, :][self.features["level"] == 2],
            self.features.iloc[:, :][self.features["level"] == 3],
            self.features.iloc[:, :][self.features["level"] == 4],
            self.features.iloc[:, :][self.features["level"] == 5],
            self.features.iloc[:, :][self.features["level"] == 6],
        ]

        slovnik_by_levels = [
            self.slovnik_A1_list,
            self.slovnik_A2_list,
            self.slovnik_B1_list,
            self.slovnik_B2_list,
            self.slovnik_C1_list,
        ]
        kelly_by_levels = [
            self.kelly_A1_list,
            self.kelly_A2_list,
            self.kelly_B1_list,
            self.kelly_B2_list,
            self.kelly_C1_list,
        ]

        # начинаем анализ
        # слов в тексте
        self.data_about_text["words"] = self.dict_of_features["words"]

        # предложений
        self.data_about_text["sentences"] = self.dict_of_features["sentences"]

        self.data_about_text["unique_words"] = self.dict_of_features["unique_words"]

        self.data_about_text["tt_ratio"] = self.dict_of_features["tt_ratio"]

        # изучающее чтение текста должно занять m мин
        self.data_about_text["reading_for_detail_speed"] = self.__output_of_min(
            self.dict_of_features["words"]
            / Analyzer.READING_FOR_DETAIL_SPEED_NORM[level_int]
        )

        # просмотровое чтение текста должно занять m мин
        self.data_about_text["skim_reading_speed"] = self.__output_of_min(
            self.dict_of_features["words"] / Analyzer.SKIM_READING_SPEED_NORM[level_int]
        )

        # частотный словарь по тексту
        self.data_about_text["frequency_bag"] = self.__get_frequency_bag(
            self.whole_lemmas_list
        )

        # 1. Считаем ключевые слова по tf/idf
        bag_tf_idf = dict()
        # берем только основные части речи
        for item in self.count_content_pos:
            if (
                len(item) > 2
                and item not in self.bastard_list
                and item not in self.names_list
                # вернуть если поедут ключевые слова and item not in self.slovnik_A1_list
                and self.whole_lemmas_list.count(item) > 1
            ):
                idf = self.__count_freq_by_rnc(item)
                bag_tf_idf[item] = self.whole_lemmas_list.count(item) - (20 * idf)

        sorted_bag = sorted(bag_tf_idf.items(), key=lambda x: x[1], reverse=True)

        self.data_about_text["key_words"] = [f[0] for f in sorted_bag[:10]]

        # Списки с минимумов
        self.data_about_text["inA1"] = round(self.dict_of_features["inA1"] * 100)
        self.data_about_text["not_inA1"] = list(
            set(
                [
                    f
                    for f in self.clean_lemmas_list
                    if len(f) > 1
                    and f not in self.stop_list
                    and f not in self.slovnik_A1_list
                ]
            )
        )

        self.data_about_text["inA2"] = round(self.dict_of_features["inA2"] * 100)
        self.data_about_text["not_inA2"] = list(
            set(
                [
                    f
                    for f in self.clean_lemmas_list
                    if len(f) > 1
                    and f not in self.stop_list
                    and f not in self.slovnik_A2_list
                ]
            )
        )

        self.data_about_text["inB1"] = round(self.dict_of_features["inB1"] * 100)
        self.data_about_text["not_inB1"] = list(
            set(
                [
                    f
                    for f in self.clean_lemmas_list
                    if len(f) > 1
                    and f not in self.stop_list
                    and f not in self.slovnik_B1_list
                ]
            )
        )

        self.data_about_text["inB2"] = round(self.dict_of_features["inB2"] * 100)
        self.data_about_text["not_inB2"] = list(
            set(
                [
                    f
                    for f in self.clean_lemmas_list
                    if len(f) > 1
                    and f not in self.stop_list
                    and f not in self.slovnik_B2_list
                ]
            )
        )

        self.data_about_text["inC1"] = round(self.dict_of_features["inC1"] * 100)
        self.data_about_text["not_inC1"] = list(
            set(
                [
                    f
                    for f in self.clean_lemmas_list
                    if len(f) > 1
                    and f not in self.stop_list
                    and f not in self.slovnik_C1_list
                ]
            )
        )

        # Если уровень высокий, не выводим слова, не входящие в списки низких уровней: это примерно все:)

        if level_for_scale >= 3:
            self.data_about_text["not_inA1"] = ""
        if level_for_scale >= 6:
            self.data_about_text["not_inA2"] = ""
        if level_for_scale >= 8:
            self.data_about_text["not_inB1"] = ""

        self.data_about_text["infr5000"] = round(
            self.dict_of_features["infr5000"] * 100
        )

        # Можем работать с лексическими списками только до 4 уровня,
        # дальше их не существует
        self.data_about_text["cool_words"] = []
        self.data_about_text["rare_words"] = []
        self.data_about_text["cool_but_not_in_slovnik"] = []

        if level_int < 4:

            # Самые полезные слова
            cool_words = list(
                set(
                    [
                        f
                        for f in self.clean_lemmas_list
                        if f not in slovnik_by_levels[(level_int - 1)]
                        and (
                            f in self.fr_3000_list
                            or f in kelly_by_levels[level_int]
                            or self.whole_lemmas_list.count(f) > 2
                        )
                    ]
                )
            )

            if len(cool_words) > 20:
                bag_cool_words = {}
                for item in cool_words:
                    idf = self.__count_freq_by_rnc(item)
                    bag_cool_words[item] = idf
                sorted_cool_bag = sorted(
                    bag_cool_words.items(), key=lambda x: x[1], reverse=True
                )
                cool_words = [f[0] for f in sorted_cool_bag[:20]]

            self.data_about_text["cool_words"] = cool_words

            # Избавиться от этих слов
            self.data_about_text["rare_words"] = list(
                set(
                    [
                        f
                        for f in self.clean_lemmas_list
                        if (
                            f not in cool_words
                            and f not in self.geo_name_list
                            and f not in self.names_list
                            and f not in slovnik_by_levels[level_int]
                            and f not in kelly_by_levels[level_int]
                            and f not in self.data_about_text["key_words"]
                            and (f not in self.fr_10000_list or f in self.bastard_list)
                        )
                    ]
                )
            )

            # нет в словнике есть в Келли
            self.data_about_text["cool_but_not_in_slovnik"] = list(
                set(
                    [
                        f
                        for f in self.clean_lemmas_list
                        if (
                            f not in slovnik_by_levels[level_int]
                            and f in kelly_by_levels[level_int]
                            and f in self.fr_3000_list
                        )
                    ]
                )
            )

        else:
            # Самые полезные слова
            cool_words_more_4 = list(
                set(
                    [
                        f
                        for f in self.clean_lemmas_list
                        if (
                            f not in slovnik_by_levels[3]
                            and (
                                f in slovnik_by_levels[4]
                                or f in self.fr_5000_list
                                or f in kelly_by_levels[4]
                                or self.whole_lemmas_list.count(f) > 3
                            )
                        )
                    ]
                )
            )

            if len(cool_words_more_4) > 20:
                bag_cool_words_more_4 = {}
                for item in cool_words_more_4:
                    idf = self.__count_freq_by_rnc(item)
                    bag_cool_words_more_4[item] = idf
                sorted_cool_bag_more_4 = sorted(
                    bag_cool_words_more_4.items(), key=lambda x: x[1], reverse=True
                )
                cool_words_more_4 = [f[0] for f in sorted_cool_bag_more_4[:20]]

            self.data_about_text["cool_words"] = cool_words_more_4

            # Избавиться от этих слов
            rare_words_more_4 = list(
                set(
                    [
                        f
                        for f in self.clean_lemmas_list
                        if (
                            f not in cool_words_more_4
                            and f not in self.geo_name_list
                            and f not in self.names_list
                            and f not in slovnik_by_levels[4]
                            and f not in self.data_about_text["key_words"]
                            and (f not in self.fr_10000_list or f in self.bastard_list)
                        )
                    ]
                )
            )
            self.data_about_text["rare_words"] = rare_words_more_4

        gram_complex = []

        for i in Analyzer.DIFFICULT_GRAM:
            compare = self.dict_of_features[i] / (
                np.mean(f_by_levels[level_int][i] + 0.00000001)
            )
            if compare > 2:
                gram_complex.append(
                    Analyzer.GR_FEATURES_NAMES[Analyzer.DIFFICULT_GRAM.index(i)]
                )

        self.data_about_text["gram_complex"] = list(set(gram_complex))

        # вывод всех полей как они идут на сервисе
        # print(self.data_about_text)

        return self.data_about_text

    def start_native(self, raw_text):
        self.__clear_fields()

        text = self.__clean_text(raw_text)

        # создаем словарь и будем в него все складывать
        self.dict_of_features = {}

        # чистый финальный списочек параметров
        self.data_about_text = {}

        # первая проверка текста на длину
        self.data_about_text = self.__first_check_len_text(text)

        if self.data_about_text["text_ok"] is False:
            return self.data_about_text

        self.sentences = self.__sent_tokenize_plus(text)
        self.whole_analyzed_text = self.mystem.analyze(text)  # весь текст одним списком
        analyzed_bigrams = list(nltk.bigrams(self.whole_analyzed_text))  # биграммочки

        for i in Analyzer.GRAM_FEATURES:
            self.dict_of_features[i] = 0

        # запускаем функцию со всеми грам. анализами
        self.__gram_analyze(self.whole_analyzed_text)

        for i in analyzed_bigrams:
            self.__count_passive_form(i)

        # вторая проверка, не менее 5 слов
        self.data_about_text = self.__second_check_len_text(self.whole_lemmas_list)
        if self.data_about_text["text_ok"] is False:
            return self.data_about_text

        self.clean_lemmas_list = [
            f
            for f in self.whole_lemmas_list
            if f not in self.geo_name_list
            and f not in self.names_list
            and f not in self.bastard_list
            and f not in self.stop_list
        ]

        all_words = len(self.whole_analyzed_text)
        all_sentences = len(self.sentences)
        all_syllables = sum(self.number_of_syllables_list)

        all_len_words = [len(f) for f in self.whole_lemmas_list]
        all_len_sentences = [len(f.split(" ")) for f in self.sentences]

        long_words = len(self.long_words_list)
        whole_lemmas_minus_stop = [
            f for f in self.whole_lemmas_list if f not in self.stop_list
        ]
        unique_lemmas_list = list(set(whole_lemmas_minus_stop))

        # Частотник по тексту
        self.dict_of_features["frequency_bag"] = self.__get_frequency_bag(
            self.whole_lemmas_list
        )

        # Цифры про текст:
        # всего слов в тексте
        self.dict_of_features["words"] = len(self.whole_analyzed_text)
        self.dict_of_features["syllables"] = all_syllables
        self.dict_of_features["unique_words"] = len(unique_lemmas_list)
        # всего предложений в тексте
        self.dict_of_features["sentences"] = all_sentences
        # средняя длина слова в тексте
        self.dict_of_features["mean_len_word"] = round(
            ((sum(self.words_length_list)) / all_words), 1
        )
        self.dict_of_features["median_len_word"] = statistics.median(all_len_words)
        self.dict_of_features["median_len_sentence"] = statistics.median(
            all_len_sentences
        )

        # средняя длина предложения в тексте
        self.dict_of_features["mean_len_sentence"] = round(
            (all_words / all_sentences), 1
        )
        self.dict_of_features["mean_len_word_in_syllables"] = all_syllables / all_words
        self.dict_of_features["percent_of_long_words"] = long_words / all_words

        # lexical density - лексическая плотность, соотношение смысловых и служебных
        # частей речи: чем она выше, тем считается что текст сложнее
        self.dict_of_features[
            "lex_density"
        ] = f"{round((len(self.count_content_pos) / len(self.whole_lemmas_list)) * 10)} из 10"

        # type-token ratio (lexical diversity) - number of types/the number of tokens:
        # чем выше, тем лексика в тексте "однотипнее"
        # потом попробовать sttr: то же самое на отрезках в 1000 слов.
        # standardised type/token ratio
        self.dict_of_features[
            "tt_ratio"
        ] = f"{round((len(unique_lemmas_list) / len(self.whole_lemmas_list)) * 10)} из 10"

        self.dict_of_features["passive"] = len(self.count_passive)

        # формулы читабельности (адаптированные, из диссера Оборневой)##
        formula_f_oborneva_genuine = round(
            206.835
            - (60.1 * (all_syllables / all_words))
            - (1.3 * (all_words / all_sentences))
        )

        formula_f_oborneva = formula_f_oborneva_genuine

        if formula_f_oborneva > 100:
            formula_f_oborneva = 100
        if formula_f_oborneva < 0:
            formula_f_oborneva = 0

        self.dict_of_features[
            "formula_flesh_oborneva"
        ] = f"{formula_f_oborneva} из 100 (чем больше - тем текст легче)"

        formula_f_k_oborneva = round(
            0.5 * (all_words / all_sentences)
            + 8.4 * (all_syllables / all_words)
            - 15.59
        )

        if formula_f_k_oborneva < 0:
            formula_f_k_oborneva = 0

        self.dict_of_features["formula_flesh_kinc_oborneva"] = (
            f"{formula_f_k_oborneva} (примерно должна "
            "соответствовать школьному классу)"
        )

        in_laposhina_list = self.__percent_of_known_words_100(
            self.whole_lemmas_list, self.laposhina_list
        )

        self.dict_of_features["laposhina_list"] = f"{in_laposhina_list} %"

        in_detcorpus_5000 = self.__percent_of_known_words_100(
            self.whole_lemmas_list, self.detcorpus_list
        )

        self.dict_of_features["detcorpus_5000"] = f"{in_detcorpus_5000} %"

        in_rki_children = self.__percent_of_known_words_100(
            self.whole_lemmas_list, self.rki_children_list
        )

        self.dict_of_features["rki_children_list"] = f"{in_rki_children} %"

        in_united_simple_list = self.__percent_of_known_words_100(
            self.whole_lemmas_list, self.united_list
        )

        self.dict_of_features["united_simple_list"] = f"{in_united_simple_list} %"

        self.dict_of_features["rare_words"] = list(
            set(
                [
                    f
                    for f in self.clean_lemmas_list
                    if f not in self.detcorpus_list and f not in self.fr_10000_list
                ]
            )
        )

        structure_complex_genuine = round(
            (
                100
                - formula_f_oborneva_genuine
                + self.dict_of_features["прич"]
                + self.dict_of_features["страд"]
                + self.dict_of_features["passive"]
            )
            / 10
        )

        structure_complex = structure_complex_genuine

        if structure_complex < 0:
            structure_complex = 0
        if structure_complex > 10:
            structure_complex = 10

        self.dict_of_features["structure_complex"] = f"{structure_complex} из 10"

        lexical_complex_genuine = round(10 - (((in_laposhina_list - 50) * 2) / 10))

        lexical_complex = lexical_complex_genuine

        if lexical_complex > 10:
            lexical_complex = 10
        if lexical_complex < 0:
            lexical_complex = 0

        self.dict_of_features["lexical_complex"] = f"{lexical_complex} из 10"

        lexical_complex_rki = round(10 - ((((in_detcorpus_5000 - 60) * 2)) / 10))

        if lexical_complex_rki > 10:
            lexical_complex_rki = 10
        if lexical_complex_rki < 0:
            lexical_complex_rki = 0

        self.dict_of_features["lexical_complex_rki"] = f"{lexical_complex_rki} из 10"

        narrativity = round(
            10 - 2 * (self.dict_of_features["S"] / (self.dict_of_features["V"] + 1))
        )

        if narrativity < 0:
            narrativity = 0

        self.dict_of_features["narrativity"] = f"{narrativity} из 10"

        description = round(3 * (self.dict_of_features["A"] / all_sentences))

        if description > 10:
            description = 10

        self.dict_of_features["description"] = f"{description} из 10"

        formula_pushkin_100 = round(
            (((structure_complex_genuine + lexical_complex_genuine) * 5) - narrativity),
            1,
        )

        if formula_pushkin_100 > 100:
            formula_pushkin_100 = 99
        if formula_pushkin_100 < 1:
            formula_pushkin_100 = 1

        self.dict_of_features["formula_pushkin_100"] = round(formula_pushkin_100)

        self.dict_of_features["formula_pushkin"] = round((formula_pushkin_100 / 10), 1)

        if self.dict_of_features["formula_pushkin"] < 1:
            self.dict_of_features["formula_pushkin"] = 1

        ball = self.__output_ballov(formula_pushkin_100)

        for i in Analyzer.INTERPRETER_NATIVE:
            if i[1] < formula_pushkin_100 <= i[2]:
                self.dict_of_features[
                    "level_comment"
                ] = f"{round(formula_pushkin_100)} {ball} из 100. {i[0]}"

        for i in self.dict_of_features:
            if i in Analyzer.COLUMNS_NEEDED_NATIVE:
                self.data_about_text[i] = self.dict_of_features[i]

        return self.data_about_text
