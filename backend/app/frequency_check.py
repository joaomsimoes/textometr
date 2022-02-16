import pymystem3
import pandas as pd


class FrequencyCheck:

    COLUMNS = [
        "lemma",
        "comment_main",
        "comment_child",
        "pos",
        "cefr",
        "kelly",
        "rnc_ipm",
        "detcorpus_ipm",
        "rufola_123_ipm",
        "det_rki_ipm",
        "bilingual_ipm",
        "native_ipm",
    ]

    def __init__(self):
        self.mystem = pymystem3.Mystem(entire_input=False, disambiguation=True)
        self.all_freq_data = pd.read_csv("data/freq_all.csv", quotechar="`")

    def start(self, row_words):
        lem_words = self.mystem.lemmatize(row_words)
        lem_str = ",".join(lem_words)
        lem_str = lem_str.replace("печение", "печенье")
        lem_str = lem_str.replace("варение", "варенье")
        lem_str = lem_str.replace("воскресение", "воскресенье")
        lem_str = lem_str.replace("счастие", "счастье")
        lem_str = lem_str.replace("несчастие", "несчастье")
        lem_words_list = lem_str.split(",")
        words = list(sorted(lem_words_list))
        result = []
        freq_data_dict = {
            "input_error": False,
            "not_in_list": False,
            "is_omonim": False,
        }
        if len(words) == 0 or len(words) > 3:
            freq_data_dict["input_error"] = True
            result.append(freq_data_dict)
            return result
        for i in words:
            freq_data_dict = {
                "input_error": False,
                "not_in_list": False,
                "is_omonim": False,
            }
            list_of_lemmas = list(self.all_freq_data["lemma"])
            count_lemmas = list_of_lemmas.count(i)
            if count_lemmas == 0:
                freq_data_dict["not_in_list"] = True
                result.append(freq_data_dict)
            if count_lemmas == 1:
                for col in self.COLUMNS:
                    freq_data_dict[col] = list(
                        self.all_freq_data[self.all_freq_data["lemma"] == i][col]
                    )[0]
                result.append(freq_data_dict)
            if count_lemmas > 1:
                freq_data_dict["is_omonim"] = True
                omonims = self.all_freq_data[self.all_freq_data["lemma"] == i]
                for row in omonims.iterrows():
                    for col in self.COLUMNS:
                        freq_data_dict[col] = row[1][col]
                    result.append(freq_data_dict)
        print(result)
        return result
