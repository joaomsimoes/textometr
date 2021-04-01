import unittest

from app.analyzer_2000 import Analyzer


class TestAnalyzer(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text_analyzer = Analyzer()

    def test_text_1(self):
        self.assertEqual(
            TestAnalyzer.text_analyzer.start_native(
                "Шла Саша по шоссе и сосала сушку."
            )["sentences"],
            1,
        )

    def test_text_2(self):
        self.assertEqual(
            TestAnalyzer.text_analyzer.start_native(
                "Трудно найти подходящее место для гнезда, трудно выкормить птенцов и т. п."
            )["sentences"],
            1,
        )

    def test_text_3(self):
        self.assertEqual(
            TestAnalyzer.text_analyzer.start_native(
                "Реальные вещества всегда содержат какие-то примеси, даже лекарственные вещества (например, "
                "аспирин - рис. 1-2), к чистоте которых предъявляются особые требования"
            )["sentences"],
            1,
        )

    def test_text_4(self):
        self.assertEqual(
            TestAnalyzer.text_analyzer.start_native(
                "Первое предложение.Второе сразу, без пробела."
            )["sentences"],
            2,
        )

    def test_text_5(self):
        self.assertEqual(
            TestAnalyzer.text_analyzer.start_native(
                "Самая большая лисица достигает 55 см. в длину с размахом крыльев до 1,8 м. Есть свои лилипуты и "
                "великаны и в растительном мире."
            )["sentences"],
            2,
        )

    def test_text_6(self):
        self.assertEqual(
            TestAnalyzer.text_analyzer.start_native(
                "Длина капсулы равна 0,1 мм, ширина 0.08 мм. А в 2010 году"
            )["sentences"],
            2,
        )

    def test_text_7(self):
        self.assertEqual(
            TestAnalyzer.text_analyzer.start_native(
                "И этот загадочный персонаж ногозначительно помолчал..."
            )["sentences"],
            1,
        )

    def test_text_8(self):
        self.assertEqual(
            TestAnalyzer.text_analyzer.start_native(
                "Бывает и такое многоточие… А потом новое предложение."
            )["sentences"],
            2,
        )

    def test_text_9(self):
        self.assertEqual(
            TestAnalyzer.text_analyzer.start_native(
                "А в 2010 году в г. Дубае состоялось торжественное открытие самого высокого здания в "
                "мире – небоскрёба Бурдж-Халифа."
            )["sentences"],
            1,
        )

    def test_text_10(self):
        self.assertEqual(
            TestAnalyzer.text_analyzer.start_native(
                "В 1821 году С.В. Морозов заплатил своему помещику Рюмину за выход на волю."
            )["sentences"],
            1,
        )

    def test_text_11(self):
        self.assertEqual(
            TestAnalyzer.text_analyzer.start_native(
                "Походка министра, таким образом, в 4.7-6.7 раза более дурацкая, чем обычная."
            )["sentences"],
            1,
        )

    def test_text_12(self):
        self.assertEqual(
            TestAnalyzer.text_analyzer.start_native("И вы вырастили мух?- Нет пока.")[
                "sentences"
            ],
            2,
        )

    def test_text_13(self):
        self.assertEqual(
            TestAnalyzer.text_analyzer.start_native(
                "Пока приезжий господин осматривал свою комнату, внесены были его пожитки: прежде всего чемодан из "
                "белой кожи, несколько поистасканный, показывавший, что был не в первый раз в дороге. Чемодан внесли "
                "кучер Селифан, низенький человек в тулупчике, и лакей Петрушка, малый лет тридцати, в просторном "
                "подержанном сюртуке, как видно с барского плеча, малый немного суровый на взгляд, с очень крупными "
                "губами и носом. Вслед за чемоданом внесен был небольшой ларчик красного дерева с штучными "
                "выкладками из карельской березы, сапожные колодки и завернутая в синюю бумагу жареная курица. Когда "
                "все это было внесено, кучер Селифан отправился на конюшню возиться около лошадей, а лакей Петрушка "
                "стал устроиваться в маленькой передней, очень темной конурке, куда уже успел притащить свою шинель "
                "и вместе с нею какой-то свой собственный запах, который был сообщен и принесенному вслед за тем "
                "мешку с разным лакейским туалетом."
            )["structure_complex"],
            "9 из 10",
        )

    def test_text_14(self):
        self.assertEqual(
            TestAnalyzer.text_analyzer.start_native(
                "Пока приезжий господин осматривал свою комнату, внесены были его пожитки: прежде всего чемодан из "
                "белой кожи, несколько поистасканный, показывавший, что был не в первый раз в дороге. Чемодан "
                "внесли кучер Селифан, низенький человек в тулупчике, и лакей Петрушка, малый лет тридцати, в "
                "просторном подержанном сюртуке, как видно с барского плеча, малый немного суровый на взгляд, с "
                "очень крупными губами и носом. Вслед за чемоданом внесен был небольшой ларчик красного дерева с "
                "штучными выкладками из карельской березы, сапожные колодки и завернутая в синюю бумагу жареная "
                "курица. Когда все это было внесено, кучер Селифан отправился на конюшню возиться около лошадей, "
                "а лакей Петрушка стал устроиваться в маленькой передней, очень темной конурке, куда уже успел "
                "притащить свою шинель и вместе с нею какой-то свой собственный запах, который был сообщен и "
                "принесенному вслед за тем мешку с разным лакейским туалетом."
            )["lexical_complex"],
            "6 из 10",
        )

    def test_text_15(self):
        self.assertEqual(
            TestAnalyzer.text_analyzer.start_native(
                "Пока приезжий господин осматривал свою комнату, внесены были его пожитки: прежде всего чемодан "
                "из белой кожи, несколько поистасканный, показывавший, что был не в первый раз в дороге. Чемодан "
                "внесли кучер Селифан, низенький человек в тулупчике, и лакей Петрушка, малый лет тридцати, в "
                "просторном подержанном сюртуке, как видно с барского плеча, малый немного суровый на взгляд, с "
                "очень крупными губами и носом. Вслед за чемоданом внесен был небольшой ларчик красного дерева с "
                "штучными выкладками из карельской березы, сапожные колодки и завернутая в синюю бумагу жареная "
                "курица. Когда все это было внесено, кучер Селифан отправился на конюшню возиться около лошадей, "
                "а лакей Петрушка стал устроиваться в маленькой передней, очень темной конурке, куда уже успел "
                "притащить свою шинель и вместе с нею какой-то свой собственный запах, который был сообщен и "
                "принесенному вслед за тем мешку с разным лакейским туалетом."
            )["formula_pushkin"],
            6.9,
        )

    def test_text_16(self):
        self.assertEqual(
            TestAnalyzer.text_analyzer.start_native(
                "Договор аренды квартиры — документ подтверждающий предоставление собственником квартиры "
                "(арендодателем) другой стороне (арендатору) жилого помещения за определенную плату во владение "
                "и пользование с ограниченным сроком по времени и другими условиями. Нотариальное заверение "
                "договора аренды не требуется и обязательной нотариальной формы такого договора законодательством "
                "не предусмотрено, однако по желанию - стороны вправе предусмотреть его нотариальное удостоверение."
            )["structure_complex"],
            "10 из 10",
        )

    def test_text_17(self):
        self.assertEqual(
            TestAnalyzer.text_analyzer.start_native(
                "Договор аренды квартиры — документ подтверждающий предоставление собственником квартиры "
                "(арендодателем) другой стороне (арендатору) жилого помещения за определенную плату во владение и "
                "пользование с ограниченным сроком по времени и другими условиями. Нотариальное заверение договора "
                "аренды не требуется и обязательной нотариальной формы такого договора законодательством не "
                "предусмотрено, однако по желанию - стороны вправе предусмотреть его нотариальное удостоверение."
            )["lexical_complex"],
            "9 из 10",
        )

    def test_text_18(self):
        self.assertEqual(
            TestAnalyzer.text_analyzer.start_native(
                "Это мой одноклассник Миша. Он глупый и некрасивый: глаза маленькие, рот большой, нос картошкой. "
                "Он думает, он сильный."
            )["lexical_complex_rki"],
            "3 из 10",
        )

    def test_text_19(self):
        self.assertEqual(
            TestAnalyzer.text_analyzer.start_native(
                "Как хороша эта маленькая белокаменная церковь! Одиноко стоит она возле вязовой рощи на небольшом "
                "холмике у тихого озерца."
            )["description"],
            "9 из 10",
        )

    def test_text_20(self):
        self.assertEqual(
            TestAnalyzer.text_analyzer.start_native(
                "Меня зовут Тоня. Это мой стол. Его зовут Леша. Это его стол."
            )["formula_pushkin"],
            1,
        )

    def test_text_21(self):
        self.assertEqual(
            TestAnalyzer.text_analyzer.start_native("384")["text_ok"], False
        )

    def test_text_22(self):
        self.assertEqual(TestAnalyzer.text_analyzer.start_native("")["text_ok"], False)

    def test_text_23(self):
        self.assertEqual(
            TestAnalyzer.text_analyzer.start_native("Шла Саша по шоссе.")[
                "text_error_message"
            ],
            "Введите текст на русском языке не менее 5 слов.",
        )

    def test_text_24(self):
        self.assertEqual(
            TestAnalyzer.text_analyzer.start_native(
                "Шла Саша по шоссе, была хорошая погода. А в тексте бывает english/vinglish"
            )["words"],
            13,
        )

    def test_text_25(self):
        self.assertEqual(
            TestAnalyzer.text_analyzer.start_native(
                "Сестра Криса Фармера Пенни стала журналисткой. "
                "Когда брата убили, ей было 17 лет.В 2015 году — "
                "через два года после смерти отца — Пенни Фармер "
                "решила попытаться найти предполагаемого убийцу "
                "брата в фейсбуке. У нее получилось моментально; "
                "кроме того, она нашла двух сыновей мужчины и одну "
                "из его жен. Она разослала всем им сообщения — и "
                "обратилась в полицию Манчестера."
            )["text_ok"],
            True,
        )

    def test_text_26(self):
        self.assertEqual(
            TestAnalyzer.text_analyzer.start_native(
                "Из детских стихов всем известно, что в Африке всегда жарко, "
                "что там живут акулы, гориллы и злые крокодилы…А что же такое Африка "
                "на самом деле? Так называется один из континентов. На большей его части "
                "действительно всегда жарко. Но есть места, где жарко и сухо, очень редко "
                "идёт дождь (порой даже один раз в несколько лет), мало растений и животных. "
                "Это жаркие пустыни — царство солнца и песка. Самая знаменитая африканская "
                "пустыня — Сахара.А есть места, где жарко и очень влажно, потому что там "
                "каждый день идёт дождь. Это тропические леса, где очень много растений, "
                "самые знаменитые из которых — длинные и сильные лианы. Здесь множество "
                "ярких бабочек, шумных попугаев, юрких обезьянок и других животных. "
            )["level_comment"],
            "19 баллов из 100. Очень простой текст, подойдет для возраста 7-8 лет (1-2 класс).",
        )

    def test_text_27(self):
        self.assertEqual(
            TestAnalyzer.text_analyzer.start_native(
                "Когда произошла эта история, Сева жил у бабушки в деревне. "
                "Лето уже близилось  к концу. Сева радовался, что скоро увидит "
                "школьных друзей, расскажет им про жизнь в  деревне и покажет подарок "
                "бабушки – настоящий бинокль. А пока он был один, сидел на  скамейке "
                "у дома и разглядывал в бинокль окрестности. В поле зрения попадало всё то, "
                "что  давно было знакомо: то забор, то большая липа, то соседский дом, то "
                "сам сосед с сумкой.  Вдруг Сева заметил птицу, но вот только летела она "
                "почему-то не вверх, а вниз!  “Неужели птица упала на землю?” - "
                "поразился Сева и бросился в ту сторону. И правда, за  забором на куче сухой "
                "травы Сева нашёл маленькую птичку. Она бессильно раскинула  крылья и слегка "
                "шевелила головой."
            )["level_comment"],
            "24 балла из 100. Простой текст, подойдет для возраста 9-10 лет (3-4 класс).",
        )

    def test_text_28(self):
        self.assertEqual(
            TestAnalyzer.text_analyzer.start_native(
                "Мистер и миссис Дурсль проживали в доме номер четыре по Тисовой "
                "улице и всегда с гордостью заявляли, что они, слава богу, "
                "абсолютно нормальные люди. Уж от кого-кого, а от них никак нельзя "
                "было ожидать, чтобы они попали в какую-нибудь странную или загадочную "
                "ситуацию. Мистер и миссис Дурсль весьма неодобрительно относились к "
                "любым странностям, загадкам и прочей ерунде. Мистер Дурсль возглавлял "
                "фирму под названием «Граннингс», которая специализировалась на "
                "производстве дрелей. Это был полный мужчина с очень пышными усами и "
                "очень короткой шеей. Что же касается миссис Дурсль, она была тощей "
                "блондинкой с шеей почти вдвое длиннее, чем положено при ее росте. "
                "Однако этот недостаток пришелся ей весьма кстати, поскольку большую "
                "часть времени миссис Дурсль следила за соседями и подслушивала их разговоры. "
                "А с такой шеей, как у нее, было очень удобно заглядывать за чужие заборы. "
                "У мистера и миссис Дурсль был маленький сын по имени Дадли, и, по их мнению, "
                "он был самым чудесным ребенком на свете."
            )["level_comment"],
            "40 баллов из 100. Простой текст, подойдет для возраста 9-10 лет (3-4 класс).",
        )

    def test_text_29(self):
        self.assertEqual(
            TestAnalyzer.text_analyzer.start_native(
                "Почему перелетные птицы возвращаются весной обратно? "
                "В жизни птиц можно выделить несколько периодов. Они повторяются каждый год, "
                "поэтому обычно говорят о годовом цикле. В типичном случае годовой цикл "
                "выглядит так: гнездование, линька, осенняя миграция, зимовка, "
                "весенняя миграция, снова гнездование и далее «по списку». "
                "Все названные периоды важны, но особое значение имеет гнездовой. "
                "В это время птицы выводят потомство, от них требуется масса дополнительных "
                "затрат — как времени, так и энергии. Поэтому успешно размножаются лишь "
                "те особи, которые делают это в благоприятных для них местах, к "
                "которым они лучше всего приспособлены."
            )["level_comment"],
            "49 баллов из 100. Достаточно простой текст, подойдет для возраста 11-12 лет (5-6 класс).",
        )

    def test_text_30(self):
        self.assertEqual(
            TestAnalyzer.text_analyzer.start_native(
                "Палеография – специальная наука, которая исследует памятники древней письменности. "
                "Термин ”палеография“ появился в XVII веке. Он греческого происхождения. "
                "Первоначально в палеографии изучались те памятники письменности, текст "
                "которых был написан от руки красящим веществом (чернилами, красками), "
                "особыми орудиями письма (пером, заострённой палочкой) на специально "
                "подготовленной мягкой поверхности."
            )["level_comment"],
            "75 баллов из 100. Текст подойдет для возраста 13-15 лет (7-9 класс).",
        )

    def test_text_31(self):
        self.assertEqual(
            TestAnalyzer.text_analyzer.start_native(
                "«Министерство дурацких походок» (также распространен перевод "
                "«Министерство глупых походок») — один из самых известных комедийных "
                "скетчей не только в «Летающем цирке Монти Пайтона», но и во всей "
                "классической британской комедии вообще. Он рассказывает о выдуманном "
                "британском министерстве, которое занимается развитием дурацких походок. "
                "По своей сути скетч — сатирический: он высмеивает бюрократизм и непроходимость "
                "системы британского правительства и то, что правительства, по большому счету, "
                "порой тратят деньги на ерунду."
            )["level_comment"],
            "76 баллов из 100. Текст подойдет для возраста 16-17 лет (10-11 класс).",
        )

    def test_text_32(self):
        self.assertEqual(
            TestAnalyzer.text_analyzer.start_native(
                "Договор аренды квартиры — документ подтверждающий предоставление "
                "собственником квартиры (арендодателем) другой стороне (арендатору) "
                "жилого помещения за определенную плату во владение и пользование с "
                "ограниченным сроком по времени и другими условиями. Нотариальное "
                "заверение договора аренды не требуется и обязательной нотариальной формы "
                "такого договора законодательством не предусмотрено, однако по желанию - "
                "стороны вправе предусмотреть его нотариальное удостоверение. "
            )["level_comment"],
            "99 баллов из 100. Очень сложный текст, подойдет для выпускника ВУЗа и старше",
        )

    def test_text_33(self):
        self.assertEqual(
            TestAnalyzer.text_analyzer.start_native(
                "Мы едем, едем, едем в далёкие далёкие края. Веселые соседи и добрые друзья."
            )["frequency_bag"],
            [
                ("ехать", 3),
                ("далекий", 2),
                ("в", 1),
                ("веселый", 1),
                ("добрый", 1),
                ("друг", 1),
                ("и", 1),
                ("край", 1),
                ("мы", 1),
                ("сосед", 1),
            ],
        )

    def test_text_34(self):
        self.assertEqual(
            TestAnalyzer.text_analyzer.start_native(
                "- Ай - ай - ай! - и бегом в сторону. - Ай! Ой! - закричали ребята.Эй! Мяу! му - му, гав - гав и "
                "ку - ку."
            )["laposhina_list"],
            "95 %",
        )

    def test_text_35(self):
        self.assertEqual(
            TestAnalyzer.text_analyzer.start_native(
                "- Ай - ай - ай! - и бегом в сторону. - Ай! Ой! - закричали ребята.Эй! Мяу! му - му, гав - гав "
                "и ку - ку."
            )["level_comment"],
            "1 балл из 100. Очень простой текст, подойдет для возраста 7-8 лет (1-2 класс).",
        )


if __name__ == "__main__":
    unittest.main()
