import unittest

import pymystem3
from app.analyzer import Analyzer


class TestAnalyzer(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        mystem = pymystem3.Mystem(entire_input=False, disambiguation=True)
        cls.text_analyzer = Analyzer(mystem)

    def test_text_1(self):
        self.assertEqual(
            TestAnalyzer.text_analyzer.start_foreign(
                "Шла Саша по шоссе и сосала сушку."
            )["sentences"],
            1,
        )

    def test_text_2(self):
        self.assertEqual(
            TestAnalyzer.text_analyzer.start_foreign(
                "Шла Саша по шоссе и сосала сушку."
            )["words"],
            7,
        )

    def test_text_3(self):
        self.assertEqual(
            TestAnalyzer.text_analyzer.start_foreign(
                "Все рабочие — от доярок до сварщиков, под команды, "
                "доносившиеся из радиоприемника, дружно приседали и бегали "
                "на месте! Производственная гимнастика, как и многое в СССР, "
                "было добровольно-принудительным занятием. Перед обедом или "
                "в конце смены в течение 5-10 минут на каждом предприятии "
                "проводилась гимнастика. Рабочие, не отходя от станка, под "
                "чутким руководством инструктора выполняли физические "
                "упражнения."
            )["words"],
            54,
        )

    def test_text_4(self):
        self.assertEqual(
            TestAnalyzer.text_analyzer.start_foreign("384")["text_ok"], False
        )

    def test_text_5(self):
        self.assertEqual(TestAnalyzer.text_analyzer.start_foreign("")["text_ok"], False)

    def test_text_6(self):
        self.assertEqual(
            TestAnalyzer.text_analyzer.start_foreign(
                "Шла Саша по шоссе, была хорошая погода. А в тексте бывает english/vinglish"
            )["words"],
            13,
        )

    def test_text_7(self):
        self.assertEqual(
            TestAnalyzer.text_analyzer.start_foreign(
                "Минобороны Азербайджана впервые опубликовало данные о военных потерях в ходе конфликта "
                "в Карабахе.\n\n   "
                "По информации ведомства, погибли 2783 военнослужащих. Еще более ста считаются "
                "пропавшими без вести. \t   "
                "В госпиталях находятся 1245 военных."
            )["text_ok"],
            True,
        )

    def test_text_8(self):
        self.assertEqual(
            TestAnalyzer.text_analyzer.start_foreign(
                "Сестра Криса Фармера Пенни стала журналисткой. Когда брата убили, ей было 17 лет.В 2015 году — "
                "через два года после смерти отца — Пенни Фармер "
                "решила попытаться найти предполагаемого убийцу "
                "брата в фейсбуке. У нее получилось моментально; "
                "кроме того, она нашла двух сыновей мужчины и одну "
                "из его жен. Она разослала всем им сообщения — и "
                "обратилась в полицию Манчестера. Вскоре выяснилось, "
                "что в Сакраменто заново открыли дело об исчезновении "
                "третьей жены Бостона.Полиция допросила сыновей "
                "мужчины. Они рассказали, что всегда знали, что "
                "Бостон убил их мать (именно его третья жена родила "
                "обоих). Кроме того, они рассказали, что находились "
                "на лодке, когда Бостон убил Криса Фармера и Пету Фрэмптон."
            )["text_ok"],
            True,
        )

    def test_text_9(self):
        self.assertEqual(
            TestAnalyzer.text_analyzer.start_foreign(
                "Это мой друг. Это моя подруга. Это мой дом. Это мое место. Это моя комната. Это моё окно. "
                "Это мой город."
            )["inA1"],
            100,
        )

    def test_text_10(self):
        self.assertEqual(
            TestAnalyzer.text_analyzer.start_foreign(
                "Договор аренды квартиры — документ подтверждающий предоставление собственником квартиры "
                "(арендодателем) другой стороне (арендатору) жилого помещения за определенную плату во владение "
                "и пользование с ограниченным сроком по времени и другими условиями. Нотариальное заверение "
                "договора аренды не требуется и обязательной нотариальной формы такого договора законодательством "
                "не предусмотрено, однако по желанию - стороны вправе предусмотреть его нотариальное удостоверение. "
                "Арендодатель подтверждает, что он получил согласие всех совершеннолетних лиц, зарегистрированных "
                "по данному адресу, или владеющих совместно с ним данной жилплощадью, на сдачу данной квартиры в "
                "аренду. Арендодатель подтверждает, что на момент подписания настоящего Договора аренды данная "
                "квартира не продана, не подарена, не является предметом судебного спора, не находится под залогом, "
                "арестом, не сдана внаем. Дом на период аренды квартиры не подлежит сносу или капитальному ремонту с "
                "отселением. Арендодатель имеет право посещать Арендатора только с предварительным уведомлением. "
                "Арендодатель последствия аварий и повреждений, происшедших не по вине Арендатора, устраняет своими "
                "силами. Арендодатель оплачивает: эксплуатационные расходы, центральное отопление, коммунальные "
                "услуги, телефон (абонентская ежемесячная плата)."
            )["inB1"],
            49,
        )

    # проверяем, отфильтровали ли лишние параметры. Если нет, то должна вылезти ошибка.
    def test_text_11(self):
        with self.assertRaises(KeyError):
            TestAnalyzer.text_analyzer.start_foreign(
                "Договор аренды квартиры — документ подтверждающий предоставление собственником квартиры "
                "(арендодателем) другой стороне (арендатору) жилого помещения за определенную плату во "
                "владение и пользование с ограниченным сроком по времени и другими условиями."
            )["деепр"]

    def test_text_12(self):
        self.assertEqual(
            TestAnalyzer.text_analyzer.start_foreign(
                "Это моя одноклассница Лена. Она глупая и некрасивая: глаза круглые, уши большие, "
                "нос курносый, характер ужасный. Она думает, она самая умная, потому что учится хорошо. "
                "А я знаю: она учится хорошо, потому что уроки делает три часа в день! Она не знает, "
                "как называются динозавры, какие бывают автомобили. И она не играет в футбол!"
            )["level_int"],
            2,
        )

    def test_text_13(self):
        self.assertEqual(
            TestAnalyzer.text_analyzer.start_foreign(
                "Мария шла домой с работы. Около дома она увидела Андрея. Раньше они часто встречались,гуляли, "
                "ходили в кино, им нравилось быть вместе. Но однажды Мария и Андрей поссорились и вот уже 4 месяца "
                "не видели друг друга. Андрей не приходил, не звонил, и Мария подумала, что у него есть другая "
                "девушка. Мария жила одна. Дома ее ждала только рыжая собака Бимка. Она всегда была рада, когда "
                "Мария приходила домой с работы. Девушка нашла собаку зимой на улице 3 месяца назад. Сначала "
                "Бимка ничего не ела, лежала и грустно смотрела на нее. Потом привыкла, начала есть, Мария ей "
                "понравилась. Девушка хотела узнать, чья это собака, но никто не мог сказать, кто ее хозяин. Андрей "
                "стоял около дома и ждал Марию. Он мечтал встретить ее. - Здравствуй Маша! - Здравствуй, Андрей! "
                "Как дела? - Все нормально.- Что ты здесь делаешь? – Мария не понимала, почему Андрей "
                "пришел сюда.- Я ищу свою собаку Ладу. 4 месяца назад зимой Лада гуляла одна на улице и не пришла "
                "домой. Я ищу ее все это время, но не могу найти. Я подумал, может быть, ты видела ее?- Твоя собака "
                "рыжая?- Да, рыжая.- Тогда пойдем ко мне. Я знаю, где твоя собака. Когда Мария и Андрей вошли в "
                "квартиру, Бимка побежала не к ней, а к Андрею. Хозяин и собака были очень рады друг другу.- Я не "
                "знала, что у тебя есть собака, что это твоя собака, - сказала Мария.- Я купил ее, потому что мне "
                "было плохо, когда мы поссорились, - ответил Андрей.- Наконец, ты нашел свою Ладу, а я звала ее "
                "Бимка, - грустно сказала Мария, - теперь вы можете идти домой. Андрей ничего не ответил. Он понял, "
                "что пришел к Марии не потому, что искал собаку, а потому, что любит ее. Он не хотел уходить. "
                "А Лада-Бимка сидела, смотрела на них и тоже нехотела уходить. Она мечтала, чтобы ее старый "
                "хозяин и новая хозяйка были вместе."
            )["level_int"],
            1,
        )

    def test_text_14(self):
        self.assertEqual(
            TestAnalyzer.text_analyzer.start_foreign(
                "Я иду на урок. Он говорит по-русски. Я еду на машине."
            )["level_int"],
            1,
        )

    def test_text_15(self):
        self.assertEqual(
            TestAnalyzer.text_analyzer.start_foreign(
                "Конечно, жизнь женщины трудна, часто очень трудна, и всё-таки никто не может "
                "лишить её права заниматься любимым делом. Я считаю, что государство должно "
                "помнить: женщина нуждается в заботе и помощи». Шократ Тадыров, работающий "
                "в Академии наук в Туркмении: «Я хочу поговорить о воспитании детей. "
                "Ответственность мужчин в этом вопросе неможет равняться с ответственностью женщин. "
                "Воспитание детей должнобыть главной задачей женщины. И, конечно, забота о доме "
                "и о муже. Ведь муж зарабатывает деньги на содержание своей семьи и, естественно, "
                "нуждается во внимании жены. Работающие женщины — вот главная причина того, что во "
                "многих странах теперь рождается так мало детей. Кроме того, работающая женщина "
                "становится материально самостоятельной, поэтому родители часто расходятся, "
                "и дети растут без отца». Эльвира Новикова, депутат Государственной Думы: "
                "«У женщины должен быть выбор: где, сколько и как работать и работать ли вообще. "
                "Пусть свою судьбу выбирают сами женщины в зависимости от того, что для них главное — "
                "дом, работа или и то и другое вместе. Не нужно искать один вариант счастья для всех, "
                "ведь у каждой женщины свои представления о счастье. И государство должно принимать "
                "свои решения, заботясь о работающих женщинах и их детях». Алексей Петрович Николаев, "
                "пенсионер: «Время очень изменило женщин. Или, лучше сказать, женщина сама изменилась. "
                "Мы уже привыклик тому, что нас учат и лечат женщины, что среди инженеров, "
                "экономистов, юристов много женщин. Сегодня мы нередко встречаем женщин-милиционеров, "
                "политиков и даже лётчиц. Женщина овладела, кажется, всеми мужскими профессиями. "
                "А вы знаете, о чём мечтают такие женщины? Они мечтают о букете цветов и не "
                "хотят потерять право на внимание мужчин». Александр Данверский, журналист: «До сих пор все войны, "
                "катастрофы, социальные эксперименты происходили потому, что решения принимали мужчины. Женщин, "
                "к сожалению, не приглашали обсуждать важные проблемы.В последние годы социологи всё чаще говорят, "
                "что XXI век будет веком женщины, потому что так называемые «мужские ценности» (личный успех, решение "
                "проблем с позиции силы) уступят место «женским ценностям»: заботе о мире и общем благополучии. "
                "Если мы хотим, чтобы положение изменилось, мы, мужчины, должны помочь женщинам занять в обществе "
                "достойное место."
            )["level_int"],
            3,
        )

    def test_text_16(self):
        self.assertEqual(
            TestAnalyzer.text_analyzer.start_foreign(
                "В исторической науке и обществознании уже давно идет спор о том, "
                "движется ли мир к единой цивилизации, ценности которой станут достоянием "
                "всего человечества, или сохранится и даже усилится тенденция к "
                "культурно-историческому многообразию и человеческое общество будет представлять "
                "собой ряд самостоятельно развивающихся цивилизаций. Сторонники второй из указанных "
                "позиций подчеркивают ту бесспорную мысль, что в основе развития любого "
                "жизнеспособного организма ( и в том числе общества людей) лежит разнообразие."
            )["level_int"],
            6,
        )

    def test_text_17(self):
        self.assertEqual(
            TestAnalyzer.text_analyzer.start_foreign(
                "Мы живём в эпоху чудовищной потери смысла. Сегодня России предложено, "
                "прямо скажем, относительно сытное существование. Многие кричат о бедности, "
                "но это лицемерные крики. Хлеб насущный у нас появился. Но в обмен на некоторую "
                "комфортность существования у людей отняли смысл жизни - жить же только ради "
                "мира вещей, пусть даже супермодных, престижных, Россия не приучена. "
                "Человек не рождён для того, чтобы осознавать себя как небольшое, но "
                "рентабельное предприятие, в которое он вкладывает деньги, которые сам же и "
                "зарабатывает. Поэтому люди отчаянно ищут, откуда и куда мы идём. "
                "И эти вопросы  - кто я и зачем я существую -  становятся одними из главных для нас. "
                "Скорее, этими вопросами задаются люди, уже имеющие некий жизненный опыт. А молодёжь "
                "гораздо больше волнуют проценты по кредитам или наличие свободных мест на курортах "
                "Гоа. – На самом деле никто не знает, что волнует молодёжь. "
                "Молодые склонны копировать тот стиль жизни, который пропагандируют масс-медиа. "
                "А подросткам сегодня чуть ли не с детских лет навязывается образ человека "
                "покупающего, им внушают, что их главная задача в жизни – потреблять."
            )["level_int"],
            4,
        )

    def test_text_18(self):
        self.assertEqual(
            TestAnalyzer.text_analyzer.start_foreign(
                "Договор аренды квартиры — документ подтверждающий предоставление собственником квартиры "
                "(арендодателем) другой стороне (арендатору) жилого помещения за определенную плату во "
                "владение и пользование с ограниченным сроком по времени и другими условиями. Нотариальное "
                "заверение договора аренды не требуется и обязательной нотариальной формы такого договора "
                "законодательством не предусмотрено, однако по желанию - стороны вправе предусмотреть его "
                "нотариальное удостоверение."
            )["level_int"],
            6,
        )

    def test_text_19(self):
        self.assertEqual(
            TestAnalyzer.text_analyzer.start_foreign(
                "Мы едем, едем, едем в далёкие далёкие края. "
                "Веселые соседи и добрые друзья."
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

    def test_text_20(self):
        self.assertEqual(
            TestAnalyzer.text_analyzer.start_foreign(
                "- Ай - ай - ай! - и бегом в сторону. - Ай! Ой! - закричали ребята.Эй! Мяу! му - му, гав - гав "
                "и ку - ку."
            )["not_inB2"],
            ["бегом"],
        )

    def test_text_21(self):
        self.assertEqual(
            TestAnalyzer.text_analyzer.start_foreign(
                "- Ай - ай - ай! - и бегом в сторону. - Ай! Ой! - закричали ребята.Эй! Мяу! му - му, гав - гав и "
                "ку - ку."
            )["inB1"],
            86,
        )

    def test_text_22(self):
        self.assertEqual(
            TestAnalyzer.text_analyzer.start_foreign(
                "Скоро мы поедем на экскурсию в Москву. Мы много говорили об этом на уроке, и вчера Иван Петрович "
                "попросил нас сделать необычное домашнее задание — написать о нашем самом интересном путешествии. "
                "Вот что написала Ирена. В этом году я и мои друзья ездили в Крым, в Ялту. Эта поездка мне очень "
                "понравилась. "
                "В Симферополь, столицу Крыма, мы ехали на поезде. Поезд шёл 36 часов. Конечно, это долго, и вы можете "
                "спросить, что делать в поезде 36 часов. Ну, во-первых, у нас было очень уютное купе, где мы не только "
                "спали, но и пили чай, ели, разговаривали, пели песни. Во-вторых, дорога была очень интересная. "
                "Из окна вагона мы видели Россию и Украину, их природу, деревни и города. В Симферополе мы были утром. "
                "В Ялту ходят автобусы, троллейбусы, можно ехать и на такси. Мы выбрали автобус-экспресс. Через 2 часа "
                "мы уже были в гостинице «ОреАнда». Ялта — чудесный южный городок на берегу Чёрного моря. Мы ездили в "
                "Ботанический сад, были в музее А.П. Чехова, на заводе «Массандровские вина». Один раз мы ходили в "
                "горы. "
                "Это было интересно, но трудно. Мы шли пешком 5 часов! Эта поездка помогла мне лучше узнать Россию и "
                "Украину, их историю и современность. Я думаю, что я поеду в Крым ещё раз."
            )["infr5000"],
            96,
        )

    def test_text_23(self):
        self.assertEqual(
            TestAnalyzer.text_analyzer.start_foreign(
                "Я хочу рассказать, как одна встреча с великим человеком сыграла огромную роль в моей жизни. "
                "Когда мне было восемнадцать лет, я приехал в Петербург и поступил учиться в университет. "
                "Я всегда о чень любил музыку. Моим любимым композитором был Пётр Ильич Чайковский. Поэтому в "
                "свободное время я часто ходил в оперный театр и с удовольствием слушал все оперы Чайковского, "
                "смотрел его балеты.Однажды мои друзья пригласили меня в гости в одну семью. Хозяйка этого дома была "
                "прекрасной певицей и часто выступала на концертах. Я с удовольствием пошёл к ним. Это был для меня "
                "счастливый вечер, потому что в тот вечер к ним в гости пришёл Пётр Ильич Чайковский. Поздно вечером "
                "мы вместе с Чайковским вышли из дома, и он спросил, где живу. Узнав, что я живу недалеко от его дома, "
                "он предложил мне пойти пешком. Я был счастлив, ведь я не только познакомился с великим композитором, "
                "и мог поговорить с ним во время нашей прогулки.Мы пошли по набережной реки Невы. Была прекрасная "
                "лунная ночь. Сначала мы шли молча. Потом Пётр Ильич спросил меня:—Я слышал, что Вы хотите стать "
                "художником. Это правда?—Да, — ответил я.Мы помолчали, а потом я спросил его:— Пётр Ильич, говорят, "
                "что гении создают свои произведения, пишут музыку, картины только в те минуты, когда они работают "
                "легко и свободно, как будто кто-то помогает им. В общем, когда к ним приходит вдохновение. Что Вы "
                "думаете об этом?— Ах, молодой человек, не говорите глупости! Нельзя ждать вдохновения, должен прежде "
                "всего труд, труд и труд! Нужно не ждать вдохновения, а серьёзно работать, трудиться каждый день. "
                "Помните, молодой человек, одного вдохновения мало, даже гений или очень талантливый человек ничего "
                "не добьётся в жизни, не сделает ничего значительного, если не будет трудиться. Я, например, считаю, "
                "что я самый обыкновенный человек.Я не согласился с ним и хотел поспорить, но он остановил меня и "
                "продолжил;— Нет, нет, не спорьте, я знаю, что говорю. Советую Вам, молодой человек, запомнить на "
                "всю жизнь, что вдохновение приходит только к тому человеку, который серьёзно и много работает, "
                "вдохновение рождается только из труда и во время труда. Я каждое утро в 8 или 9 часов начинаю "
                "работать и пишу музыку. Если мне не нравится, что я написал сегодня, завтра я буду делать эту же "
                "работу, буду писать всё сначала. Так я пишу день, два, десять дней. Вы сможете сделать больше и "
                "лучше, чем талантливые, но ленивые люди."
            )["key_words"],
            [
                "вдохновение",
                "композитор",
                "гений",
                "музыка",
                "труд",
                "трудиться",
                "спрашивать",
                "талантливый",
                "серьезно",
                "писать",
            ],
        )

    def test_text_24(self):
        self.assertEqual(
            TestAnalyzer.text_analyzer.start_foreign(
                "Договор аренды квартиры — документ подтверждающий предоставление собственником квартиры "
                "(арендодателем) другой стороне (арендатору) жилого помещения за определенную плату во "
                "владение и пользование с ограниченным сроком по времени и другими условиями."
            )["characters"],
            250,
        )

    def test_text_25(self):
        self.assertEqual(
            TestAnalyzer.text_analyzer.start_foreign(
                "Меня зовут Миша, у меня есть подруга Маша. Все говорят, что мы хорошая пара. Да, но в последнее время "
                "у нас есть небольшая проблема. Уже год моя подруга Маша — вегетарианка. И они не просто не ест мясо, "
                "она строгая вегетарианка. Это значит, что она также не ест рыбу. Мясо она и раньше ела редко, "
                "не любила она его. А вот рыбу она очень любила! Всегда, когда я приглашал Машу в ресторан, "
                "она ела рыбу. "
            )["rki_children_1000"],
            "85 %",
        )

    def test_text_26(self):
        self.assertEqual(
            TestAnalyzer.text_analyzer.start_foreign(
                "О резком росте потока нелегальных мигрантов, которые пытаются попасть в Евросоюз через Беларусь, "
                "заговорили еще в начале лета. В начале июля в Литве даже объявили режим чрезвычайной ситуации в связи "
                "с этим. А в конце августа Литва, Латвия и Польша заявили, что из-за потока желающих нелегально "
                "пересечь границу они собираются построить забор на границе с Беларусью. "
            )["level_number"],
            4.9,
        )

    def test_text_27(self):
        self.assertEqual(
            TestAnalyzer.text_analyzer.start_foreign(
                "О резком росте потока нелегальных мигрантов, которые пытаются попасть в Евросоюз через Беларусь, "
                "заговорили еще в начале лета. В начале июля в Литве даже объявили режим чрезвычайной ситуации в связи "
                "с этим. А в конце августа Литва, Латвия и Польша заявили, что из-за потока желающих нелегально "
                "пересечь границу они собираются построить забор на границе с Беларусью. "
            )["level_comment"],
            "Конец B2. II сертификационный уровень.",
        )

    def test_text_28(self):
        self.assertEqual(
            TestAnalyzer.text_analyzer.start_foreign(
                "Известно, что если звезда подходит слишком близко к сверхмассивной черной дыре, то приливные силы "
                "могут ее разорвать. При этом вещество звезды разгоняется до скоростей от нескольких процентов до "
                "нескольких десятков процентов от скорости света, а также генерируется электромагнитное излучение и "
                "рождаются другие элементарные частицы. По данным предыдущих наблюдений, полное энерговыделение в таких"
                " событиях составляет приблизительно 1048–1052 эрг. "
            )["level_comment"],
            "ой-ой-ой, этот текст сложный даже для носителя",
        )

    def test_text_29(self):
        self.assertEqual(
            TestAnalyzer.text_analyzer.start_foreign(
                "Меня зовут Миша, у меня есть подруга Маша. Все говорят, что мы хорошая пара. Да, но в последнее "
                "время у нас есть небольшая проблема. Уже год моя подруга Маша — вегетарианка. И они не просто не ест "
                "мясо, она строгая вегетарианка. Это значит, что она также не ест рыбу. Мясо она и раньше ела редко, "
                "не любила она его. "
            )["level_comment"],
            "A1. Элементарный уровень.",
        )

    def test_text_30(self):
        self.assertEqual(
            TestAnalyzer.text_analyzer.start_foreign(
                "Но сегодня я здесь, и сегодня я в форме. Сегодня мой хуй отсосёшь мне ты! Говно, залупа, пенис, "
                "хер, давалка, хуй, блядина, Головка, шлюха, жопа, член, еблан, петух… мудила "
                "Рукоблуд, ссанина, очко, блядун, вагина, Сука, ебланище, влагалище, пердун, дрочила"
                "Пидор, пизда, туз, малафья Гомик, мудила, пилотка, манда,Анус, вагина, путана, пидрила"
                "Шалава, хуила, мошонка, елда…"
                "Опять ебет мозги пресса, озноб и джетлаг. Засунь себе в жопу бейдж и вопросы, Шерлок. "
            )["obsc_check"],
            True,
        )

    def test_text_31(self):
        self.assertEqual(
            TestAnalyzer.text_analyzer.start_foreign(
                "Летит кибитка удалая через леса и поля."
            )["old_words"],
            ["кибитка"],
        )


if __name__ == "__main__":
    unittest.main()
