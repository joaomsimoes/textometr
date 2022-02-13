

import pymystem3
import pandas as pd

m = pymystem3.Mystem(entire_input=False, disambiguation=True)

input_text = "собакой, А, это"

all_freq_data = pd.read_csv('data/rki_unified_100001.csv', quotechar='`')

columns = ["rank", "lemma", "pos", "all_rki_ipm", "bilingual_ipm","rnc_ipm","detcorpus_ipm"]

list_of_words = m.lemmatize(input_text)

def __find_freq(words):
    result = []
    if len(words) == 0 or len(words) > 3:
        result.append("Ошибка. Вставьте от 1 до 3 русских слов.")
        return result
    for i in words:
        freq_data_dict = {}
        list_of_lemmas = list(all_freq_data['lemma'])
        if list_of_lemmas.count(i) == 0:
            freq_data_dict["rank"] = "Слово отсутсвует в частотных списках"
            result.append(freq_data_dict)
        if list_of_lemmas.count(i) == 1:
            for col in columns:
                freq_data_dict[col] = list(all_freq_data[all_freq_data['lemma'] == i][col])[0]
            result.append(freq_data_dict)
        if list_of_lemmas.count(i) > 1:
            freq_data_dict["rank"] = "Омоним"
            result.append(freq_data_dict)
            '''
            omonims = all_freq_data[all_freq_data['lemma'] == i]
            for ii in omonims:
                print(ii)
                for col in columns:
                    freq_data_dict[col] = list(ii[col])
                result.append(freq_data_dict)
                '''
    return result
__find_freq(list_of_words)

