# Быстренько обучаем модель и анализируем входной текст
import numpy as np
import pandas as pd
import math
import nltk
from sklearn import linear_model
import re
import pymystem3
from collections import defaultdict
import statistics
from sklearn.model_selection import train_test_split
from nltk.tokenize import sent_tokenize
import logging

def load_dictionaries():
    global m
    m = pymystem3.Mystem(entire_input=False,disambiguation=True)

    global ridge
    ridge = linear_model.Ridge(alpha=0.1)

    global features
    features = pd.read_csv("data/list_of_features_1207.csv")

    global columns_needed
    columns_needed = [
        'inA2', 'kellyC2', 'simple850', 'simple1000', 'simple2000',
        'dale3000', 'infr1000', 'infr3000', 'infr5000', 'infr10000',
        'lex_abstract', 'formula_smog', 'mean_len_word', 'median_len_word',
        'median_len_sentence', 'mean_len_sentence', 'percent_of_long_words',
        'mean_punct_per_sentence', 'median_punct_per_sentence', 'tt_ratio',
        'contentPOS', 'kotoryi/words', 'modal_verbs', 'conj_adversative',
        'kotoryi/sentences', 'passive', 'A', 'ADV', 'ADVPRO', 'ANUM',
        'APRO', 'COM', 'CONJ', 'INTJ', 'NUM', 'PART', 'PR', 'S', 'SPRO',
        'V', 'наст', 'непрош', 'прош', 'вин', 'дат', 'им', 'пр', 'род',
        'твор', 'ед', 'мн', 'деепр', 'изъяв', 'инф', 'пов', 'прич', 'кр',
        'полн', 'притяж', '1-л', '2-л', '3-л', 'жен', 'муж', 'сред', 'несов',
        'сов', 'действ', 'страд', 'неод', 'од', 'нп', 'пе'
    ]

    # словники
    with open ('data/new_vocab_a1.txt','r', encoding = 'utf_8') as f:
        slovnik_A1 = f.readlines()
    global slovnik_A1_list
    slovnik_A1_list = [f.replace('\n','') for f in slovnik_A1]
    
    with open ('data/new_vocab_a2.txt','r', encoding = 'utf_8') as f:
        slovnik_A2 = f.readlines()
    global slovnik_A2_list
    slovnik_A2_list = [f.replace('\n','') for f in slovnik_A2]
    
    with open ('data/new_vocab_b1.txt','r', encoding = 'utf_8') as f:
        slovnik_B1 = f.readlines() 
    global slovnik_B1_list
    slovnik_B1_list = [f.replace('\n','') for f in slovnik_B1]
    
    with open ('data/new_vocab_b2.txt','r', encoding = 'utf_8') as f:
        slovnik_B2 = f.readlines() 
    global slovnik_B2_list
    slovnik_B2_list = [f.replace('\n','') for f in slovnik_B2]
    
    with open ('data/new_vocab_c1.txt','r', encoding = 'utf_8') as f:
        slovnik_C1 = f.readlines() 
    global slovnik_C1_list
    slovnik_C1_list = [f.replace('\n','') for f in slovnik_C1]

    # списки kelly
    with open ('data/kelly_a1.txt','r', encoding = 'utf_8') as f:
        kelly_A1 = f.readlines() 
    global kelly_A1_list
    kelly_A1_list = [f.replace('\n','') for f in kelly_A1]
    
    with open ('data/kelly_a2.txt','r', encoding = 'utf_8') as f:
        kelly_A2 = f.readlines()
    global kelly_A2_list
    kelly_A2_list = [f.replace('\n','') for f in kelly_A2]
    
    with open ('data/kelly_b1.txt','r', encoding = 'utf_8') as f:
        kelly_B1 = f.readlines()
    global kelly_B1_list
    kelly_B1_list = [f.replace('\n','') for f in kelly_B1]
    
    with open ('data/kelly_b2.txt','r', encoding = 'utf_8') as f:
        kelly_B2 = f.readlines()
    global kelly_B2_list
    kelly_B2_list = [f.replace('\n','') for f in kelly_B2]
    
    with open ('data/kelly_c1.txt','r', encoding = 'utf_8') as f:
        kelly_C1 = f.readlines()
    global kelly_C1_list
    kelly_C1_list = [f.replace('\n','') for f in kelly_C1]
    
    with open ('data/kelly_c2.txt','r', encoding = 'utf_8') as f:
        kelly_C2 = f.readlines()
    global kelly_C2_list
    kelly_C2_list = [f.replace('\n','') for f in kelly_C2]

    # списки частотных слов
    with open ('data/fr_100.txt','r', encoding = 'utf_8') as f:
        fr_100 = f.readlines()
    global fr_100_list
    fr_100_list = [f.replace('\n','') for f in fr_100]
    
    with open ('data/fr_300.txt','r', encoding = 'utf_8') as f:
        fr_300 = f.readlines()
    global fr_300_list
    fr_300_list = [f.replace('\n','') for f in fr_300]
    
    with open ('data/fr_500.txt','r', encoding = 'utf_8') as f:
        fr_500 = f.readlines()
    global fr_500_list
    fr_500_list = [f.replace('\n','') for f in fr_500]
    
    with open ('data/fr_1000.txt','r', encoding = 'utf_8') as f:
        fr_1000 = f.readlines()
    global fr_1000_list
    fr_1000_list = [f.replace('\n','') for f in fr_1000]
    
    with open ('data/fr_3000.txt','r', encoding = 'utf_8') as f:
        fr_3000 = f.readlines()
    global fr_3000_list
    fr_3000_list = [f.replace('\n','') for f in fr_3000]
    
    with open ('data/fr_5000.txt','r', encoding = 'utf_8') as f:
        fr_5000 = f.readlines()
    global fr_5000_list
    fr_5000_list = [f.replace('\n','') for f in fr_5000]
    
    with open ('data/fr_10000.txt','r', encoding = 'utf_8') as f:
        fr_10000 = f.readlines()
    global fr_10000_list
    fr_10000_list = [f.replace('\n','') for f in fr_10000]

    with open ('data/fr_more_than_5ipm.txt','r', encoding = 'utf_8') as f:
        fr_more_than_5 = f.readlines()
    global fr_more_than_5list
    fr_more_than_5list = [f.replace('\n', '') for f in fr_more_than_5]

    with open ('data/fr_spoken.txt','r', encoding = 'utf_8') as f:
        fr_spoken = f.readlines()
    global fr_spoken_list
    fr_spoken_list = [f.replace('\n', '') for f in fr_spoken]

    # списки слов
    with open ('data/SimpleRussian850.txt','r', encoding = 'utf_8') as f:
        simple_russian_850 = f.readlines()
    global simple_russian_850_list
    simple_russian_850_list = [f.replace('\n', '') for f in simple_russian_850]

    with open ('data/simple_russian.txt','r', encoding = 'utf_8') as f:
        simple_russian_1000 = f.readlines()
    global simple_russian_1000_list
    simple_russian_1000_list = [
        f.replace('\n', '') for f in simple_russian_1000
    ]

    with open ('data/SimpleRussian2000.txt','r', encoding = 'utf_8') as f:
        simple_russian_2000 = f.readlines()
    global simple_russian_2000_list
    simple_russian_2000_list = [
        f.replace('\n', '') for f in simple_russian_2000
    ]
    
    with open ('data/Brown10000.txt','r', encoding = 'utf_8') as f:
        brown_russian_10000 = f.readlines()
    global brown_russian_10000_list
    brown_russian_10000_list = [
        f.replace('\n', '') for f in brown_russian_10000
    ]

    with open ('data/DaleRussian3000.txt','r', encoding = 'utf_8') as f:
        dale_russian_3000 = f.readlines()
    global dale_russian_3000_list
    dale_russian_3000_list = [f.replace('\n', '') for f in dale_russian_3000]


    # семантические списки
    with open ('data/lex_abstract.txt','r', encoding = 'utf_8') as f:
        lex_abstract = f.readlines()
    global lex_abstract_list
    lex_abstract_list = [f.replace('\n','') for f in lex_abstract]

    global modal_words
    modal_words = [
        'хочется', 'нужно', 'надо', 'кажется', 'казаться', 'пожалуй',
        'хотеть', 'должный', 'хотеться'
    ]

    global gram_features
    gram_features = [
        'A', 'ADV', 'ADVPRO', 'ANUM', 'APRO', 'COM', 'CONJ', 'INTJ',
        'NUM', 'PART', 'PR', 'S', 'SPRO', 'V', 'непрош', 'прош',
        'им', 'пр', 'род', 'твор', 'деепр', 'изъяв','инф', 'пов',
        'прич', 'кр', 'полн', 'притяж', '1-л', 'сред', 'несов',
        'сов', 'действ', 'страд', 'неод', 'од'
    ]


def get_gr_info(element):
    gr_info = element.get('analysis')[0]['gr']
    gr_info = gr_info.replace(',', '<b>')
    gr_info = gr_info.replace('=', '<b>')
    gr_info = gr_info.split('<b>')
    return gr_info

# считаем слоги и буквы
def count_syllables(element):
    i_text = element.get('text')
    i_text_syl_counter = 0
    syllables = ['а', 'е', 'ё', 'и', 'о', 'у', 'ы', 'ь']
    for ii in i_text:
        if ii in syllables:
            i_text_syl_counter += 1
    if i_text_syl_counter == 0:
        i_text_syl_counter += 1
    number_of_syllables_list.append(i_text_syl_counter)
    words_length_list.append(len(i_text))
    if i_text_syl_counter >= 4:
        long_words_list.append(i_text_syl_counter)
    return True

# чистимся от имен, геообъектов и бастардов
def clean_from_name_geo_bastard(element):
    whole_lemmas_list.append(element.get('analysis')[0]['lex'])
    gr_info = element.get('analysis')[0]['gr']
    if 'qual' in element.get('analysis')[0]:
        if element.get('analysis')[0]['qual'] == 'bastard':
            bastard_list.append(element.get('text'))
    if (gr_info.find('имя') > 0 or gr_info.find('гео') > 0):
        geo_imen_list.append(element.get('analysis')[0]['lex'])
    if (gr_info.find('фам') > 0 or gr_info.find('отч') > 0):
        geo_imen_list.append(element.get('analysis')[0]['lex'])
    if (element.get('analysis')[0]['lex'] == 'но' or
        element.get('analysis')[0]['lex'] == 'а' or
        element.get('analysis')[0]['lex'] == 'однако' or
        element.get('analysis')[0]['lex'] == 'зато'):
        conj_adversative_list.append(element.get('analysis')[0]['lex'])
    if (element.get('analysis')[0]['lex'] in modal_words):
        modal_words_list.append(element.get('analysis')[0]['lex'])
    if element.get('analysis')[0]['lex'] == 'который':
        count_kotoryi.append(element.get('analysis')[0]['lex'])
    return True

# подсчет грам. информации
def count_gram(element):
    gr_info = element.get('analysis')[0]['gr']
    gr_info = gr_info.replace(',','<b>')
    gr_info = gr_info.replace('=','<b>')
    gr_info = gr_info.split('<b>')
    for i in gram_features:
        if i in gr_info:
            dict_of_features[i] += 1
    if 'S' in gr_info:
        noun_list.append(element.get('analysis')[0]['lex'])
    if 'S' in gr_info or 'V' in gr_info or 'A' in gr_info or 'ADV' in gr_info:
        count_content_pos.append(element.get('analysis')[0]['lex'])
    return True

def count_passive_form(element):
    if element[0].get('analysis') and element[1].get('analysis'):
        element0_gr = get_gr_info(element[0])
        element1_gr = get_gr_info(element[1])
        if (element[0].get('analysis')[0]['lex'] == 'быть'
            and 'прош' in element0_gr):
                if 'прич' in element1_gr:
                    count_passive.append(element[1].get('text'))
    return True

# считаем пунктуацию по предложениям
def punctuation_per_sentence(element):
    list_punctuation_score = []
    punctuation = [',','-',':',';','—']
    for i in sentences:
        counter = 0
        for ii in i:
            if ii in punctuation:
                counter += 1
        list_punctuation_score.append(counter)
    return list_punctuation_score

# Вычисляем процент слов из разных словников и частотных списков
def percent_of_known_words(element, list_of_words):
    known_words = [w for w in element if w in list_of_words]
    unknown_words = [f for f in element if f not in list_of_words]
    percent = len(known_words)/len(element)
    return percent


# общий цикл просмотра анализа слов
def gram_analyze(element):
    for i in element:
        count_syllables(i)
        if len(i.get('analysis')) > 0:
            clean_from_name_geo_bastard(i)
            count_gram(i)
    return True

    

# начало цикла анализа этого текста
def start(this_text):

    # создаем словарь и будем в него все складывать
    data_about_text = {}

    # первая проверка текста - не слишком маленький
    if len(this_text) < 10:
        data_about_text['text_ok'] = False
        data_about_text['text_error_message'] = ('Ошибка! Введите текст на'
            ' русском языке не менее 5 слов.')
        logging.debug(data_about_text)
        return data_about_text
    
    # Вторая проверка текста - не слишком большой
    if len(this_text) > 3000:
        data_about_text['text_ok'] = False
        data_about_text['text_error_message'] = ('Ошибка! Введите текст не '
            'более 3 000 слов.')
        logging.debug(data_about_text)
        return data_about_text
    
    load_dictionaries()

    global sentences
    sentences = sent_tokenize(this_text)
    whole_analyzed_text = m.analyze(this_text) # весь текст одним списком
    analyzed_bigrams = list(nltk.bigrams(whole_analyzed_text)) # биграммочки
    global whole_lemmas_list
    whole_lemmas_list = []
    global noun_list
    noun_list = []
    global bastard_list
    bastard_list = []
    global geo_imen_list
    geo_imen_list = []
    global conj_adversative_list
    conj_adversative_list = [] # противительные союзы
    global modal_words_list
    modal_words_list = []
    global words_length_list
    words_length_list = []
    global number_of_syllables_list
    number_of_syllables_list = []
    global long_words_list
    long_words_list = [] # слова более чем из 4 слогов
    global count_kotoryi
    count_kotoryi = []
    global count_content_pos
    count_content_pos = []
    global count_passive
    count_passive = []

    # создаем словарь со всеми данными из текста
    global dict_of_features
    dict_of_features = defaultdict(int)

    for i in gram_features:
        dict_of_features[i] = 0
    
    # запускаем функцию со всеми грам. анализами
    gram_analyze(whole_analyzed_text)

    for i in analyzed_bigrams:
        count_passive_form(i)
        
    # третья проверка текста, что в нем более 5 русских слов. Если он не 
    #подходит - мы не запускаем анализ.
    def check_input_text(): 
        if len(whole_lemmas_list) < 5: 
            return False
        return True
  
    data_about_text['text_ok'] = check_input_text()
    data_about_text['text_error_message'] = ('Ошибка! Введите текст на'
        ' русском языке не менее 5 слов.')

    if data_about_text['text_ok'] == False:
        logging.debug(data_about_text)
        return data_about_text    

    # меняем значения в словаре с простых счетчиков на процент
    # встречаемости в тексте
    for i in gram_features:
        dict_of_features[i] = dict_of_features[i] / len(whole_lemmas_list)

    clean_lemmas_list = [
        f for f in whole_lemmas_list if f not in geo_imen_list
            and f not in bastard_list
    ]
    noun_unic_list = list(set(noun_list)) # список уникальных сущ.
    
    
    all_words = len(whole_analyzed_text)
    all_sentences = len(sentences)
    all_syllables = sum(number_of_syllables_list)
    long_words = len(long_words_list)
    all_len_words = [len(f) for f in whole_lemmas_list]
    all_len_sentences = [len(f.split(' ')) for f in sentences]

    # Цифры про текст:
    # всего слов в тексте
    dict_of_features['words'] = (len(whole_analyzed_text))
    # всего предложений в тексте
    dict_of_features['sentences'] = (len(sentences))
    # средняя длина слова в тексте
    dict_of_features['mean_len_word'] = (sum(words_length_list))/all_words
    dict_of_features['median_len_word'] = statistics.median(all_len_words)
    dict_of_features['median_len_sentence'] = statistics.median(
        all_len_sentences
    )
    # средняя длина предложения в тексте
    dict_of_features['mean_len_sentence'] = all_words/all_sentences
    dict_of_features['mean_len_word_in_syllables'] = all_syllables/all_words
    dict_of_features['percent_of_long_words'] = long_words/all_words

    # type-token ratio - number of types and the number of tokens -
    # lexical variety
    dict_of_features['tt_ratio'] = (
        len(whole_lemmas_list)/len(set(whole_lemmas_list))
    )
    

    # Среднее количество модальных глаголов и противительных союзов
    # на предложение
    dict_of_features['conj_adversative'] = (
        len(conj_adversative_list)/all_sentences
    )
    dict_of_features['modal_verbs'] = len(modal_words_list)/all_words
    dict_of_features['kotoryi/words'] = (
        len(count_kotoryi)/len(whole_lemmas_list)
    )
    dict_of_features['kotoryi/sentences'] = len(count_kotoryi)/all_sentences
    dict_of_features['contentPOS'] = (
        len(count_content_pos)/len(whole_lemmas_list)
    )
    dict_of_features['passive'] = len(count_passive)

    # формулы читабельности (адаптированные, из Бегтина)
    dict_of_features['formula_smog'] = (30*(long_words/all_sentences))**0.5

    # Доля слов, входящих в лексические минимумы
    dict_of_features['inA1'] = percent_of_known_words(
        clean_lemmas_list,
        slovnik_A1_list
    )
    dict_of_features['inA2'] = percent_of_known_words(
        clean_lemmas_list,
        slovnik_A2_list
    )
    dict_of_features['inB1'] = percent_of_known_words(
        clean_lemmas_list,
        slovnik_B1_list
    )
    dict_of_features['inB2'] = percent_of_known_words(
        clean_lemmas_list, slovnik_B2_list
    )
    dict_of_features['inC1'] = percent_of_known_words(
        clean_lemmas_list, slovnik_C1_list
    )

    # Доля слов, входящих в списки Kelly
    dict_of_features['kellyA1'] = percent_of_known_words(
        clean_lemmas_list, kelly_A1_list
    )
    dict_of_features['kellyA2'] = percent_of_known_words(
        clean_lemmas_list, kelly_A2_list
    )
    dict_of_features['kellyB1'] = percent_of_known_words(
        clean_lemmas_list, kelly_B1_list
    )
    dict_of_features['kellyB2'] = percent_of_known_words(
        clean_lemmas_list, kelly_B2_list
    )
    dict_of_features['kellyC1'] = percent_of_known_words(
        clean_lemmas_list, kelly_C1_list
    )
    dict_of_features['kellyC2'] = percent_of_known_words(
        clean_lemmas_list, kelly_C2_list
    )

    # Доля слов, входящих в частотные списки
    dict_of_features['infr100'] = percent_of_known_words(
        clean_lemmas_list, fr_100_list
    )
    dict_of_features['infr300'] = percent_of_known_words(
        clean_lemmas_list, fr_300_list
    )
    dict_of_features['infr500'] = percent_of_known_words(
        clean_lemmas_list, fr_500_list
    )
    dict_of_features['infr1000'] = percent_of_known_words(
        clean_lemmas_list, fr_1000_list
    )
    dict_of_features['infr3000'] = percent_of_known_words(
        clean_lemmas_list, fr_3000_list
    )
    dict_of_features['infr5000'] = percent_of_known_words(
        clean_lemmas_list, fr_5000_list
    )
    dict_of_features['infr10000'] = percent_of_known_words(
        clean_lemmas_list, fr_10000_list
    )
    dict_of_features['infr_more_than_5'] = percent_of_known_words(
        clean_lemmas_list, fr_more_than_5list
    )
    dict_of_features['infr_spoken'] = percent_of_known_words(
        clean_lemmas_list, fr_spoken_list
    )


    # Доля слов, которую покрывает Simple Russian
    dict_of_features['simple850'] = percent_of_known_words(
        clean_lemmas_list, simple_russian_850_list
    )
    dict_of_features['simple1000'] = percent_of_known_words(
        clean_lemmas_list, simple_russian_1000_list
    )
    dict_of_features['simple2000'] = percent_of_known_words(
        clean_lemmas_list, simple_russian_2000_list
    )
    dict_of_features['dale3000'] = percent_of_known_words(
        clean_lemmas_list, dale_russian_3000_list
    )
    dict_of_features['brown10000'] = percent_of_known_words(
        clean_lemmas_list, brown_russian_10000_list
    )

    # Доля абстрактных/конкретных сущ. от всех сущ.
    dict_of_features['lex_abstract'] = percent_of_known_words(
        noun_unic_list, lex_abstract_list
    )

    # Доля названий и бастардов
    dict_of_features['lex_names_and_geo'] = len(geo_imen_list)
    dict_of_features['lex_bastards'] = len(bastard_list)


    # Среднее количество модальных глаголов и противительных
    # союзов на предложение
    dict_of_features['conj_adversative'] = (
        len(conj_adversative_list)/len(sentences)
    )
    dict_of_features['modal_verbs'] = len(modal_words_list)/all_words
    dict_of_features['kotoryi/words'] = (
        len(count_kotoryi)/len(whole_lemmas_list)
    )
    dict_of_features['kotoryi/sentences'] = len(count_kotoryi)/len(sentences)
    dict_of_features['contentPOS'] = (
        len(count_content_pos)/len(whole_lemmas_list)
    )

    # грам. значения на предложение
    # медианное пунктуации на предложение
    dict_of_features['median_punct_per_sentence'] = statistics.median(
        punctuation_per_sentence(sentences)
    )
    dict_of_features['mean_punct_per_sentence'] = sum(
        punctuation_per_sentence(sentences))/len(sentences
    )
    
    
    whole_analyzed_text.clear()
    analyzed_bigrams.clear()
    
    # из словаря признаков делаем список
    features_for_test_text = []
    for ii in columns_needed:
        # словарь с признаками
        features_for_test_text.append(dict_of_features[ii]) 
    test_features_array = np.array(features_for_test_text)
    test_features_array = test_features_array.reshape(1, -1)

    x_train, y_train = features[columns_needed], features['level']
    
    # Основная функция, где обучаем модель на полученных признаках и
    # делаем предсказание
    def fit_and_predict(y):
        ridge.fit(x_train,y_train)
        prediction = ridge.predict(y)
        if prediction < 0:
            prediction = 0
        return prediction
        
    prediction = fit_and_predict(test_features_array)
    
    interpreter = [("A0, самое начало",-10,0.2),
                ("A1",0.2,1),
                ("начало A2", 1, 1.3), 
                ("середина A2", 1.3, 1.6),
                ("конец A2", 1.6, 2),
                ("начало B1", 2, 2.3), 
                ("середина B1", 2.3, 2.6),
                ("конец B1", 2.6, 3),
                ("начало B2", 3, 3.3), 
                ("середина B2", 3.3, 3.6),
                ("конец B2", 3.6, 4),
                ("начало C1", 4, 4.3), 
                ("середина C1", 4.3, 4.6),
                ("конец C1", 4.6, 5),
                ("C2, уровень носителя", 5, 6), 
                ("ой-ой-ой, этот текст сложный даже для носителя", 6, 20)]
                
    # Принимает на вход уровень текста и выдает статистику.
    def tell_me_about_text(element):
         # округленный до целых уровень, чтобы потом анализировать по
         # средним значениям для этого уровня
        if element == 0:
            level_int = 0
        else:
            level_int = int(round(list(element)[0]))
        if level_int > 6:
            level_int = 6
        level_comment = ''
        for i in interpreter:
            if i[1] < element < i[2]:
                level_comment = i[0]

        data_about_text['level_number'] = '%.1f' % element
        data_about_text['level_comment'] = level_comment
        # служебный атрибут для Тони
        data_about_text['level_int'] = level_int
        
        
        # Ищем средние значения по уровням
        f_by_levels = [features.iloc[:,:][features["level"] == 0], 
                    features.iloc[:,:][features["level"] == 1], 
                    features.iloc[:,:][features["level"] == 2],
                    features.iloc[:,:][features["level"] == 3],
                    features.iloc[:,:][features["level"] == 4],
                    features.iloc[:,:][features["level"] == 5],
                    features.iloc[:,:][features["level"] == 6]]
                    
        slovnik_by_levels = [
            slovnik_A1_list, slovnik_A2_list, slovnik_B1_list,
            slovnik_B2_list, slovnik_C1_list
        ]
        kelly_by_levels = [
            kelly_A1_list, kelly_A2_list, kelly_B1_list,
            kelly_B2_list, kelly_C1_list
        ]

        reading_for_detail_speed_norm = [10, 30, 50, 50, 100, 120, 120, 120]
        skim_reading_speed_norm = [20, 50, 100, 300, 400, 500, 500, 500]
        
        # Начинаем анализ
        # Слов в тексте
        data_about_text['words'] = dict_of_features['words']
        
        # Предложений
        data_about_text['sentences'] = dict_of_features['sentences']
        
        # Знаков
        data_about_text['characters'] = len(this_text)
        
        # Изучающее чтение текста должно занять m мин		
        data_about_text['reading_for_detail_speed'] = int(
            dict_of_features['words']/reading_for_detail_speed_norm[level_int]
        )

        # Просмотровое чтение текста должно занять m мин
        data_about_text['skim_reading_speed'] = int(
            dict_of_features['words']/skim_reading_speed_norm[level_int]
        )
        
        #Блок лексики:
        
        # Можем работать с лексическими списками только до 4 уровня,
        # дальше их не существует
        if level_int < 4:
            
            # Самые полезные слова
            data_about_text['cool_words'] = list(set(
                    [
                    f for f in clean_lemmas_list
                        if f not in slovnik_by_levels[(level_int-1)]
                            and (f in fr_3000_list
                            or f in kelly_by_levels[level_int]
                            or whole_lemmas_list.count(f) > 2)
                ]
            ))
                    
            # Избавиться от этих слов
            
            data_about_text['bad_words'] = list(set(
                [
                    f for f in clean_lemmas_list
                        if (
                            f not in slovnik_by_levels[level_int]
                            and f not in kelly_by_levels[level_int]
                            and (f not in fr_10000_list
                            or f in bastard_list)
                        )
                ]
            ))
            
            #Служебный
            data_about_text['not_in_slovnik_by_levels'] = list(set(
                [
                    f for f in clean_lemmas_list
                        if (
                            f not in slovnik_by_levels[level_int])
                ]))       
                    
            #Служебный  
            data_about_text['in_kelly'] = list(set(
                [
                    f for f in clean_lemmas_list
                        if f not in slovnik_by_levels[level_int]
                        and f in kelly_by_levels[level_int]
                ]))
                
                    
            # Служебный: новые частотные слова (объяснить в первую очередь):
            data_about_text['new_and_frequent'] = list(set(
                [
                    f for f in clean_lemmas_list
                        if (
                            f not in slovnik_by_levels[(level_int-1)]
                            and f in slovnik_by_levels[level_int]
                            and f in fr_3000_list
                        )
                ]
            ))
            
            # нет в словнике есть в Келли
            data_about_text['cool_but_not_in_slovnik'] = list(set(
                [
                    f for f in clean_lemmas_list
                        if (
                            f not in slovnik_by_levels[level_int]
                            and f in kelly_by_levels[level_int]
                            and f in fr_3000_list
                        )
                ]
            ))
                
        else:
          # Самые полезные слова
            data_about_text['cool_words'] = list(set(
                    [
                    f for f in clean_lemmas_list
                        if (f not in slovnik_by_levels[3] 
                        and (f in slovnik_by_levels[4]
                            or f in fr_5000_list
                            or f in kelly_by_levels[4]
                            or whole_lemmas_list.count(f) > 3))
                ]
            ))
                    
            # Избавиться от этих слов
            
            data_about_text['bad_words'] = list(set(
                [
                    f for f in clean_lemmas_list
                        if (
                            f not in slovnik_by_levels[4]
                            and (f not in fr_10000_list
                            or f in bastard_list)
                        )
                ]
            ))  
                    
        # Имена героев и гео-названия
        geo_imen_list_title = [ f.title() for f in geo_imen_list ]
        data_about_text['names_and_geo'] = list(set(geo_imen_list_title))
            
         # Служебный - эти слова я не понял, может, опечатка? 
        data_about_text['bastards'] = list(set(bastard_list))
            
            
        # Блок Грамматика.
        
        # Слишком длинное предложение, лучше разбить на несколько
        data_about_text['too_long_sentence'] = [
            f for f in sentences
                if (
                    len(f.split(' '))
                    - (
                        np.mean(f_by_levels[level_int]['mean_len_sentence'])
                        + 10
                    )
                    > 0
                )
        ]
                    
                    
        
        # Список потенциально сложных тем
        gr_features = ['A', 'ADV', 'ADVPRO', 'ANUM', 'APRO',
        'NUM', 'SPRO', 'им', 'пр', 'род', 'твор', 'деепр', 'пов',
        'прич', 'кр', 'полн', 'притяж', 'несов',
        'сов','modal_verbs','passive']
        gr_features_names = ['Прилагательные', 'Наречия', 'Наречия', 
                           'Порядковые числительные', 'Прилагательные',
                           'Числительные', 'Местоимения', 'Именительный падеж',
                           'Предложный падеж', 'Родительный падеж', 
                           'Творительный падеж', 'Деепричастия', 
                           'Повелительное наклонение', 'Причастия', 
                           'Краткие формы прилагательных и причастий', 
                           'Краткие формы прилагательных и причастий', 
                           'Притяжательные местоимения', 'Вид глагола',
                           'Вид глагола','Модальные глаголы','Пассивные формы']
        
        gram_complex = []
        
        for i in gr_features:
            compare = dict_of_features[i]/(np.mean(f_by_levels[level_int][i] + 0.00000001))
            if  compare > 2:
                gram_complex.append(gr_features_names[gr_features.index(i)])
                #Служебный
                data_about_text[('gram_complex_'+i)] = compare
        
        data_about_text['gram_complex'] = list(set(gram_complex))
        
        return True

    tell_me_about_text(prediction)

    logging.debug(data_about_text)
    
    return data_about_text

