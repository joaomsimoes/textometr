export const TEXT_FEATURES = {
  // параметры текста для русского как иностранного
  level_number: {
    title: "Уровень текста",
    type: "progress"
  },
  level_comment: {
    title: "Уроверь текста",
    type: "string"
  },
  characters: {
    title: "Знаков с пробелами",
    type: "number"
  },
  sentences: {
    title: "Предложений",
    type: "number"
  },
  unique_words: {
    title: "Уникальных слов",
    type: "number"
  },
  key_words: {
    title: "Ключевые слова",
    description:
      "Это слова, наиболее характерные для этого текста. Они высчитываются с помощью рейтинга: количество раз, которое слово встречается в этом тексте / частота слова по Национальному корпусу русского языка (мера TF/IDF). Выигрывают слова, которые часто встречаются в данном тексте, но редко — во всех других текстах корпуса, то есть максимально характерные именно для этого текста.",
    type: "array"
  },
  cool_words: {
    title: "Самые полезные слова",
    description:
      "Это слова-кандидаты в словарик по данному тексту; cлова, которые, скорее всего, ещё не знакомы студентам (их нет в лексических минимумах предыдущих уровней), но есть в минимуме данного уровня или в списке 3 000 самых частотных слов русского языка по НКРЯ.",
    type: "array"
  },
  inA1: {
    title: "Лексический список А1 покрывает",
    type: "percent"
  },
  not_inA1: {
    title: "Не входит в лексический список А1",
    type: "array"
  },
  inA2: {
    title: "Лексический список А2 покрывает",
    type: "number"
  },
  not_inA2: {
    title: "Не входит в лексический список А2",
    type: "array"
  },
  inB1: {
    title: "Лексический список B1 покрывает",
    type: "number"
  },
  not_inB1: {
    title: "Не входит в лексический список B1",
    type: "array"
  },
  inB2: {
    title: "Лексический список B2 покрывает",
    type: "number"
  },
  not_inB2: {
    title: "Не входит в лексический список B2",
    type: "array"
  },
  inC1: {
    title: "Лексический список C1 покрывает",
    type: "number"
  },
  not_inC1: {
    title: "Не входит в лексический список C1",
    type: "array"
  },
  infr5000: {
    title: "Частотный список 5000 покрывает",
    description:
      'Список 5000 самых частотных слов русского языка из <a href="http://dict.ruslang.ru/freq.php" target="_blank">Нового частотного словаря русской лексики</a>',
    type: "number"
  },
  cool_but_not_in_slovnik: {
    title: "Полезные слова, которых нет в лексическом минимуме",
    type: "array"
  },
  rare_words: {
    title: "Редкие слова",
    type: "array"
  },
  rki_children_1000: {
    title: "Лексический список РКИ-дети 1000 покрывает",
    description:
      'Списки РКИ-дети созданы на основе частотного анализа <a href="https://digitalpushkin.tilda.ws/tirtec" target="_blank">корпуса учебников русского языка для детей TIRTEC</a>',
    type: "string"
  },
  not_in_rki_children_1000: {
    title: "Не входит в список РКИ-дети 1000",
    type: "array"
  },
  rki_children_2000: {
    title: "Лексический список РКИ-дети 2000 покрывает",
    type: "string"
  },
  not_in_rki_children_2000: {
    title: "Не входит в список РКИ-дети 2000",
    type: "array"
  },
  rki_children_5000: {
    title: "Лексический список РКИ-дети 5000 покрывает",
    type: "string"
  },
  not_in_rki_children_5000: {
    title: "Не входит в список РКИ-дети 5000",
    type: "array"
  },
  reading_for_detail_speed: {
    title: "Изучающее чтение текста займет",
    type: "string"
  },
  skim_reading_speed: {
    title: "Просмотровое чтение текста займет",
    type: "string"
  },
  gram_complex: {
    title: "Возможные грамматические темы",
    description:
      "Алгоритм подсчитывает количество частей речи и грамматических форм и предлагает темы, на которые в тексте можно найти наибольшее количество примеров.",
    type: "array"
  },
  formula_pushkin: {
    title: "Уровень сложности",
    type: "progress"
  },
  structure_complex: {
    title: "Структурная сложность",
    type: "number"
  },
  lexical_complex: {
    title: "Лексическая сложность",
    type: "number"
  },
  narrativity: {
    title: "Динамичность текста",
    type: "number"
  },
  description: {
    title: "Описательность текста",
    type: "number"
  },
  words: {
    title: "Слов",
    type: "number"
  },
  mean_len_word: {
    title: "Средняя длина слова",
    type: "number"
  },
  mean_len_sentence: {
    title: "Средняя длина предложения",
    type: "number"
  },
  formula_flesh_oborneva: {
    title: "Формула Флеша",
    type: "number"
  },
  formula_flesh_kinc_oborneva: {
    title: "Формула Флеша-Кинкейда",
    type: "number"
  },
  lex_density: {
    title: "Лексическая плотность",
    description:
      "Отношение количества смысловых и служебных частей речи: чем плотность выше, тем текст сложнее.",
    type: "number"
  },
  tt_ratio: {
    title: "Лексическое разнообразие",
    description:
      "Отношение количества уникальных слов текста к количеству всех слов текста. Обозначается величиной от 0 до 1 (когда все слова в тексте уникальны). Под словом здесь понимается лексема, т.е. все словоформы данной лексической единицы. Эта мера полезна для оценки повторяемости, воспроизводимости лексики текста.",
    type: "number"
  },
  detcorpus_5000: {
    title: "Список Русский детский 5000",
    description:
      "Сколько процентов лексики текста покрывается списком из 5000 самых частотных слов для детской литературы.",
    type: "percent"
  },
  lexical_complex_rki: {
    title: "Лексическая сложность текста для детей-иностранцев",
    type: "number"
  },
  frequency_bag: {
    title: "Частотный словарь по тексту",
    type: "list"
  }
}
