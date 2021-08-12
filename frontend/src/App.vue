<template>
  <div id="app">
    <nav class="bd-navbar navbar has-shadow is-spaced"
         role="navigation" aria-label="main navigation">
      <div class="container">
        <div class="navbar-brand">
          <a class="navbar-item" href="https://textometr.ru">
            <img id="logo" class="mr-2" src="./assets/logo.png">
          </a>

          <a role="button" class="navbar-burger" data-target="navMenu"
             aria-label="menu" aria-expanded="false">
            <span aria-hidden="true"></span>
            <span aria-hidden="true"></span>
            <span aria-hidden="true"></span>
          </a>
        </div>
        <div class="navbar-menu" id="navMenu">
          <div class="navbar-end">
            <a class="navbar-item" href="#about">О проекте</a>
            <a class="navbar-item" href="#publications">Публикации</a>
            <a class="navbar-item" href="#contacts">Контакты</a>
            <a class="navbar-item" href="https://www.facebook.com/textometr">Мы в Facebook</a>
            <div class="navbar-item">
              <span class="icon is-clickable" @click="changeTheme">
                <font-awesome-icon v-if="theme === 'light'" :icon="['fas', 'moon']" />
                <font-awesome-icon v-if="theme === 'dark'" :icon="['fas', 'sun']"/>
              </span>
            </div>
          </div>
        </div>
      </div>
    </nav>

    <section class="section">
      <div class="container is-max-desktop">
        <h4 class="title is-4 has-text-centered">Оценка сложности учебного текста</h4>
        <div class="level">
          <div class="level-item">
            <span class="is-size-5 has-text-right">Русский как иностранный</span>
          </div>
          <div class="level-item has-text-centered">
            <div class="field">
              <div class="control">
                <label class="switch mr-5 ml-5">
                  <input type="checkbox" v-model="checkboxMode" @click="clear">
                  <span class="slider round"></span>
                </label>
              </div>
            </div>
          </div>
          <div class="level-item">
            <span class="is-size-5 has-text-left">Русский как родной<sup>beta</sup></span>
          </div>
        </div>
        <article v-if="result && result.text_ok === false" class="message is-danger">
          <div class="message-body">
            {{ result.text_error_message }}
          </div>
        </article>
        <article v-if="hostname === 'pushkin-lab.ru'" class="message is-danger">
          <div class="message-body">
            Для корректной работы сервиса перейдите на новый адрес
            <a class="has-text-link" href="https://textometr.ru">textometr.ru</a>
          </div>
        </article>
        <div class="field">
          <div class="control">
            <textarea v-model="text" class="textarea" rows="15"
                      placeholder="Вставьте текст для измерения"></textarea>
          </div>
        </div>
        <div class="field is-grouped is-grouped-centered">
          <p class="control">
            <a class="button is-primary is-rounded is-medium"
                :class="{ 'is-loading': loading, 'is-primary': mode === 'foreign', 'is-warning': mode === 'native' }"
                @click="analyze">Измерить</a>
          </p>
        </div>
      </div>
    </section>

    <section class="section" id="result" v-if="text && result && result.text_ok === true && !loading">
      <div class="container is-max-desktop">
        <h1 class="title is-1">
          Результат
          <button @click="download" class="button is-small">Скачать</button>
        </h1>
        <table v-if="mode === 'foreign'"  class="table is-hoverable is-fullwidth">
          <tbody>
            <tr>
              <td colspan="2">
                <div class="mb-2">
                  <strong>{{ result.level_comment }}</strong>
                </div>
                <progress class="progress mb-4"
                          :class="getProgressClassForeign(result.level_number)"
                          :value="result.level_number"
                          max="8">{{ result.level_number}}</progress>
              </td>
            </tr>
            <tr>
              <th>{{ TEXT_FEATURES['sentences'].title }}</th>
              <td>{{ result.sentences }}</td>
            </tr>
            <tr>
              <th>{{ TEXT_FEATURES['words'].title }}</th>
              <td>{{ result.words }}</td>
            </tr>
            <tr>
              <th>{{ TEXT_FEATURES['unique_words'].title }}</th>
              <td>{{ result.unique_words }}</td>
            </tr>
            <tr>
              <th>
                {{ TEXT_FEATURES['tt_ratio'].title }}
                <div class="tooltip">
                  <font-awesome-icon :icon="['far', 'question-circle']" />
                  <span class="tooltiptext has-text-weight-normal">{{ TEXT_FEATURES['tt_ratio'].description }}</span>
                </div>
              </th>
              <td>{{ result.tt_ratio }}</td>
            </tr>
            <tr>
              <td colspan="2">
                <br>
              </td>
            </tr>
            <tr v-if="result.key_words.length > 0">
              <th>
                {{ TEXT_FEATURES['key_words'].title }}
                <div class="tooltip">
                  <font-awesome-icon :icon="['far', 'question-circle']" />
                  <span class="tooltiptext has-text-weight-normal">{{ TEXT_FEATURES['key_words'].description }}</span>
                </div>
              </th>
              <td>
                <div class="tags">
                  <span v-for="word in result.key_words" :key="word" class="tag is-success is-light is-medium">
                    {{ word }}
                  </span>
                </div>
              </td>
            </tr>
            <tr v-if="result.cool_words.length > 0">
              <th>
                {{ TEXT_FEATURES['cool_words'].title }}
                <div class="tooltip">
                  <font-awesome-icon :icon="['far', 'question-circle']" />
                  <span class="tooltiptext has-text-weight-normal">{{ TEXT_FEATURES['cool_words'].description }}</span>
                </div>
              </th>
              <td>
                <div class="tags">
                  <span v-for="word in result.cool_words" :key="word" class="tag is-success is-light is-medium">
                    {{ word }}
                  </span>
                </div>
              </td>
            </tr>
            <tr>
              <td colspan="2">
                <br>
              </td>
            </tr>
            <tr>
              <th>{{ TEXT_FEATURES['inA1'].title }}</th>
              <td>{{ result.inA1 }}%</td>
            </tr>
            <tr v-if="result.not_inA1.length > 0">
              <th>{{ TEXT_FEATURES['not_inA1'].title }}</th>
              <td>
                <div class="tags">
                  <span v-for="word in result.not_inA1" :key="word" class="tag is-success is-light is-medium">
                    {{ word }}
                  </span>
                </div>
              </td>
            </tr>
            <tr>
              <th>{{ TEXT_FEATURES['inA2'].title }}</th>
              <td>{{ result.inA2 }}%</td>
            </tr>
            <tr v-if="result.not_inA2.length > 0">
              <th>{{ TEXT_FEATURES['not_inA2'].title }}</th>
              <td>
                <div class="tags">
                  <span v-for="word in result.not_inA2" :key="word" class="tag is-success is-light is-medium">
                    {{ word }}
                  </span>
                </div>
              </td>
            </tr>
            <tr>
              <th>{{ TEXT_FEATURES['inB1'].title }}</th>
              <td>{{ result.inB1 }}%</td>
            </tr>
            <tr v-if="result.not_inB1.length > 0">
              <th>{{ TEXT_FEATURES['not_inB1'].title }}</th>
              <td>
                <div class="tags">
                  <span v-for="word in result.not_inB1" :key="word" class="tag is-success is-light is-medium">
                    {{ word }}
                  </span>
                </div>
              </td>
            </tr>
            <tr>
              <th>{{ TEXT_FEATURES['inB2'].title }}</th>
              <td>{{ result.inB2 }}%</td>
            </tr>
            <tr v-if="result.not_inB2.length > 0">
              <th>{{ TEXT_FEATURES['not_inB2'].title }}</th>
              <td>
                <div class="tags">
                  <span v-for="word in result.not_inB2" :key="word" class="tag is-success is-light is-medium">
                    {{ word }}
                  </span>
                </div>
              </td>
            </tr>
            <tr>
              <th>{{ TEXT_FEATURES['inC1'].title }}</th>
              <td>{{ result.inC1 }}%</td>
            </tr>
            <tr v-if="result.not_inC1.length > 0">
              <th>{{ TEXT_FEATURES['not_inC1'].title }}</th>
              <td>
                <div class="tags">
                  <span v-for="word in result.not_inC1" :key="word" class="tag is-success is-light is-medium">
                    {{ word }}
                  </span>
                </div>
              </td>
            </tr>
            <tr>
              <th>
                {{ TEXT_FEATURES['infr5000'].title }}
                <div class="tooltip">
                  <font-awesome-icon :icon="['far', 'question-circle']" />
                  <span class="tooltiptext has-text-weight-normal" v-html="TEXT_FEATURES['infr5000'].description"></span>
                </div>
              </th>
              <td>{{ result.infr5000 }}%</td>
            </tr>
            <tr v-if="result.cool_but_not_in_slovnik.length > 0">
              <th>{{ TEXT_FEATURES['cool_but_not_in_slovnik'].title }}</th>
              <td>
                <div class="tags">
                  <span v-for="word in result.cool_but_not_in_slovnik" :key="word" class="tag is-success is-light is-medium">
                    {{ word }}
                  </span>
                </div>
              </td>
            </tr>
            <tr v-if="result.rare_words.length > 0">
              <th>{{ TEXT_FEATURES['rare_words'].title }}</th>
              <td>
                <div class="tags">
                  <span v-for="word in result.rare_words" :key="word" class="tag is-success is-light is-medium">
                    {{ word }}
                  </span>
                </div>
              </td>
            </tr>
            <tr>
              <td colspan="2">
                <br>
              </td>
            </tr>
            <tr>
              <th>{{ TEXT_FEATURES['reading_for_detail_speed'].title }}</th>
              <td>{{ result.reading_for_detail_speed }}</td>
            </tr>
            <tr>
              <th>{{ TEXT_FEATURES['skim_reading_speed'].title }}</th>
              <td>{{ result.skim_reading_speed }}</td>
            </tr>
            <tr>
              <th>
                {{ TEXT_FEATURES['gram_complex'].title }}
                <div class="tooltip">
                  <font-awesome-icon :icon="['far', 'question-circle']" />
                  <span class="tooltiptext has-text-weight-normal">{{ TEXT_FEATURES['gram_complex'].description }}</span>
                </div>
              </th>
              <td>
                <div class="tags">
                  <span v-for="gram_theme in result.gram_complex" :key="gram_theme" class="tag is-success is-light is-medium">
                    {{ gram_theme }}
                  </span>
                </div>
              </td>
            </tr>
            <tr id="frequency_bag">
              <th>{{ TEXT_FEATURES['frequency_bag'].title }}</th>
              <td>
                <table class="table is-narrow is-bordered mb-1">
                  <tbody>
                    <tr v-for="item in wordFrequencyArray" :key="item[0]">
                      <td>{{ item[0] }}</td>
                      <td>{{ item[1] }}</td>
                    </tr>
                  </tbody>
                </table>
                <a href="#frequency_bag" @click="toggleShowAll()">
                  {{ showAll ? 'Скрыть' : 'Показать все' }}
                </a>
              </td>
            </tr>
          </tbody>
        </table>
        <table v-if="mode === 'native'" class="table is-hoverable is-fullwidth">
          <tbody>
            <tr>
              <td colspan="2">
                <div class="mb-2">
                  <strong>{{ result.level_comment }}</strong>
                </div>
                <progress class="progress mb-4"
                          :class="getProgressClassNative(result.formula_pushkin)"
                          :value="result.formula_pushkin"
                          max="10">{{ result.formula_pushkin}}</progress>
              </td>
            </tr>
            <tr>
              <th>{{ TEXT_FEATURES['structure_complex'].title }}</th>
              <td>{{ result.structure_complex }}</td>
            </tr>
            <tr>
              <th>{{ TEXT_FEATURES['lexical_complex'].title }}</th>
              <td>{{ result.lexical_complex }}</td>
            </tr>
            <tr>
              <th>{{ TEXT_FEATURES['narrativity'].title }}</th>
              <td>{{ result.narrativity }}</td>
            </tr>
            <tr>
              <th>{{ TEXT_FEATURES['description'].title }}</th>
              <td>{{ result.description }}</td>
            </tr>
            <tr>
              <td colspan="2">
                <br>
              </td>
            </tr>
            <tr>
              <th>{{ TEXT_FEATURES['sentences'].title }}</th>
              <td>{{ result.sentences }}</td>
            </tr>
            <tr>
              <th>{{ TEXT_FEATURES['words'].title }}</th>
              <td>{{ result.words }}</td>
            </tr>
            <tr>
              <th>{{ TEXT_FEATURES['unique_words'].title }}</th>
              <td>{{ result.unique_words }}</td>
            </tr>
            <tr>
              <th>{{ TEXT_FEATURES['mean_len_word'].title }}</th>
              <td>{{ result.mean_len_word }}</td>
            </tr>
            <tr>
              <th>{{ TEXT_FEATURES['mean_len_sentence'].title }}</th>
              <td>{{ result.mean_len_sentence }}</td>
            </tr>
            <tr>
              <td colspan="2">
                <br>
              </td>
            </tr>
            <tr>
              <th>{{ TEXT_FEATURES['formula_flesh_oborneva'].title }}</th>
              <td>{{ result.formula_flesh_oborneva }}</td>
            </tr>
            <tr>
              <th>{{ TEXT_FEATURES['formula_flesh_kinc_oborneva'].title }}</th>
              <td>{{ result.formula_flesh_kinc_oborneva }}</td>
            </tr>
            <tr>
              <td colspan="2">
                <br>
              </td>
            </tr>
            <tr>
              <th>
                {{ TEXT_FEATURES['lex_density'].title }}
                <div class="tooltip">
                  <font-awesome-icon :icon="['far', 'question-circle']" />
                  <span class="tooltiptext has-text-weight-normal">{{ TEXT_FEATURES['lex_density'].description }}</span>
                </div>
              </th>
              <td>{{ result.lex_density }}</td>
            </tr>
            <tr>
              <th>
                {{ TEXT_FEATURES['tt_ratio'].title }}
                <div class="tooltip">
                  <font-awesome-icon :icon="['far', 'question-circle']" />
                  <span class="tooltiptext has-text-weight-normal">{{ TEXT_FEATURES['tt_ratio'].description }}</span>
                </div>
              </th>
              <td>{{ result.tt_ratio }}</td>
            </tr>
            <tr>
              <th>
                {{ TEXT_FEATURES['laposhina_list'].title }}
                <div class="tooltip">
                  <font-awesome-icon :icon="['far', 'question-circle']" />
                  <span class="tooltiptext has-text-weight-normal">{{ TEXT_FEATURES['laposhina_list'].description }}</span>
                </div>
              </th>
              <td>{{ result.laposhina_list }}</td>
            </tr>
            <tr>
              <th>
                {{ TEXT_FEATURES['detcorpus_5000'].title }}
                <div class="tooltip">
                  <font-awesome-icon :icon="['far', 'question-circle']" />
                  <span class="tooltiptext has-text-weight-normal">{{ TEXT_FEATURES['detcorpus_5000'].description }}</span>
                </div>
              </th>
              <td>{{ result.detcorpus_5000 }}</td>
            </tr>
            <tr v-if="result.rare_words.length > 0">
              <th>{{ TEXT_FEATURES['rare_words'].title }}</th>
              <td>
                <div class="tags">
                  <span v-for="word in result.rare_words" :key="word" class="tag is-success is-light is-medium">
                    {{ word }}
                  </span>
                </div>
              </td>
            </tr>
            <tr>
              <td colspan="2">
                <br>
              </td>
            </tr>
            <tr>
              <th>{{ TEXT_FEATURES['rki_children_list'].title }}</th>
              <td>{{ result.rki_children_list }}</td>
            </tr>
            <tr>
              <th>{{ TEXT_FEATURES['lexical_complex_rki'].title }}</th>
              <td>{{ result.lexical_complex_rki }}</td>
            </tr>
            <tr id="frequency_bag">
              <th>{{ TEXT_FEATURES['frequency_bag'].title }}</th>
              <td>
                <table class="table is-narrow is-bordered">
                  <tbody>
                    <tr v-for="item in wordFrequencyArray" :key="item[0]">
                      <td>{{ item[0] }}</td>
                      <td>{{ item[1] }}</td>
                    </tr>
                  </tbody>
                </table>
                <a href="#frequency_bag" @click="toggleShowAll()">
                  {{ showAll ? 'Скрыть' : 'Показать все' }}
                </a>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
      <div class="container is-max-desktop has-text-centered mt-6">
        <a href="https://www.buymeacoffee.com/textometr">
          <img src="https://img.buymeacoffee.com/button-api/?text=Buy me a coffee&emoji=&slug=textometr&button_colour=FFDD00&font_colour=000000&font_family=Cookie&outline_colour=000000&coffee_colour=ffffff">
        </a>
      </div>
    </section>

    <section class="section" id="about">
      <div class="container is-max-desktop">
        <h1 class="title is-1 is-spaced">О проекте</h1>
        <div class="content">
          <p>
            Текстометр позволяет быстро получить информацию о тексте,
            актуальную для его подготовки к уроку русского языка:
            уровень сложности текста, ключевые слова, самые полезные слова,
            статистика по вхождению слов в лексические минимумы.
          </p>
          <p>
            Подробнее о том, как получаются эти данные.
          </p>
        </div>
        <h5 class="title is-5">Определение уровня текста для иностранных учащихся</h5>
        <div class="content">
          <p>
            Определение уровня по шкале CEFR от А1 до С2 происходит автоматически,
            с помощью регрессионной модели, обученной на корпусе из 700 текстов из
            пособий по РКИ. Подробнее о параметрах модели и признаках, на которых
            она обучалась, можно почитать <a href="#publications">здесь [1].</a>
          </p>
          <p>
            Может ли она ошибаться? Эксперименты показывают, что модель склонна
            немного завышать уровень сложности текста, поскольку она производит
            расчеты исходя из данных лексических минимумов. Практика же показывает,
            что студенты обычно знают (или угадывают из контекста) больше слов,
            чем в минимумах. Особенно это касается интернационализмов и слов,
            которые похоже звучат на родном языке ученика. Это стоит учитывать
            при подготовке текстов для славяно- или англоговорящих учеников.
            Подробнее об эксперименте со сравнением работы программы,
            мнения экспертов-преподавателей и самих студентов можно почитать <a href="#publications">здесь [3].</a>
          </p>
        </div>
        <h5 class="title is-5">Определение уровня текста для носителей языка (beta-версия)</h5>
        <div class="content">
          <p>
            Уровни сложности текста для иностранцев хорошо стандартизированы и задокументированы.
            В текстах для носителей языка понятие сложности текста многограннее: текст бывает
            написан короткими словами и фразами, что позволяет стандартным формулам читабельности
            отнести его к простым, но “продраться” сквозь незнакомые слова  или стилистические
            особенности затруднительно.
          </p>
          <p>
            Поэтому тексты для чтения носителем языка наша система оценивает по двум критериям: структурная
            сложность и лексическая. <strong>Структурная сложность</strong> учитывает классическую формулу читабельности
            Флеша, адаптированную для русского языка, а также наличие частей речи и оборотов, затрудняющих
            чтение (причастия, пассивные формы и др.) <strong>Лексическая сложность</strong> рассчитывается
            на основании вхождения слов текста в специализированные частотные списки.
          </p>
        </div>
      </div>
    </section>

    <section class="section">
      <div class="container is-max-desktop">
        <div class="columns">
          <div class="column is-flex is-align-items-stretch">
            <div class="box">
              <div class="columns is-mobile">
                <div class="column is-narrow">
                  <figure class="image is-64x64">
                    <img class="is-rounded" src="./assets/maximova.jpg">
                  </figure>
                </div>
                <div class="column">
                  <div class="has-text-weight-bold">Виктория Максимова</div>
                  <div class="is-size-7">преподаватель РКИ, основатель FB сообщества «Сторителлинг в РКИ»</div>
                </div>
              </div>
              <p>
                Теперь, когда Текстометр появился, мне уже трудно представить, как бы я готовила тексты без него. Это незаменимый инструмент для моей работы: строгие объективные параметры оценки, простой и интуитивно понятный дизайн. Спасибо разработчикам проекта!
              </p>
            </div>
          </div>

          <div class="column is-flex is-align-items-stretch">
            <div class="box">
              <div class="columns is-mobile">
                <div class="column is-narrow">
                  <figure class="image is-64x64">
                    <img class="is-rounded" src="./assets/golubeva.jpg">
                  </figure>
                </div>
                <div class="column">
                  <div class="has-text-weight-bold">Анна Голубева</div>
                  <div class="is-size-7">главный редактор издательства «Златоуст»</div>
                </div>
              </div>
              <p>
                Сервис очень помогает в работе и при общении с авторами! Особенно полезен частотный список, объективирует, что целесообразно оставлять в тексте, а что адаптировать или тренировать. Спасибо коллегам из Института Пушкина!
              </p>
            </div>
          </div>

          <div class="column is-flex is-align-items-stretch">
            <div class="box">
              <div class="columns is-mobile">
                <div class="column is-narrow">
                  <figure class="image is-64x64">
                    <img class="is-rounded" src="./assets/nekrasova.jpg">
                  </figure>
                </div>
                <div class="column">
                  <div class="has-text-weight-bold">Юлия Некрасова</div>
                  <div class="is-size-7">преподаватель РКИ Университета Салерно</div>
                </div>
              </div>
              <p>
                Очень ценная методическая находка! Огромный потенциал для подготовки заданий для уровней B1 &mdash; C1, диктантов, заданий для экзаменов и т.п. Прошу прощения за сленг, но огромный респект разработчикам!
              </p>
            </div>
          </div>
        </div>
      </div>
    </section>

    <section class="section" id="publications">
      <div class="container is-max-desktop">
        <h1 class="title is-1 is-spaced">Публикации</h1>
        <div class="content">
          <p>
            При ссылке на ресурс мы рекомендуем цитировать данную работу:
          </p>
          <p>
            <a href="https://www.researchgate.net/publication/325568093_Automated_Text_Readability_Assessment_For_Russian_Second_Language_Learners">
              [1] Laposhina А. N., Veselovskaya Т. S., Lebedeva M. U., Kupreshchenko O. F. Automated Text
              Readability Assessment For Russian Second Language Learners // Komp'juternaja Lingvistika i
              Intellektual'nye Tehnologii Сер. "Computational Linguistics and Intellectual Technologies:
              Proceedings of the International Conference "Dialogue 2018". Issue 17 (24), 2018
            </a>
          </p>
          <p>
            Ещё публикации о программе:
          </p>
          <p>
            <a href="https://www.researchgate.net/publication/346084779_AVTOMATICESKOE_OPREDELENIE_SLOZNOSTI_TEKSTA_PO_RKI">
              [2] Лапошина А.Н. Автоматическое определение сложности текста по РКИ // Сборник материалов
              международной научно-практической интернет-конференции «Актуальные вопросы описания
              и преподавания русского языка как иностранного/неродного»: сб. статей /науч. ред.
              Н.В. Кулибина. М.: 2018. С. 573-579
            </a>
          </p>
          <p>
            <a href="https://www.researchgate.net/publication/346084691_OPYT_EKSPERIMENTALNOGO_ISSLEDOVANIA_SLOZNOSTI_TEKSTOV_PO_RKI">
              [3] Лапошина А.Н. Опыт экспериментального исследования сложности текстов по РКИ // Динамика языковых
              и культурных процессов в современной России [Электронный ресурс].  —  Вып.  6.  Материалы
              VI  Конгресса РОПРЯЛ (г. Уфа, 11–14 октября 2018 года). — СПб.: РОПРЯЛ, 2018. С. 1154-1179
            </a>
          </p>
        </div>
      </div>
    </section>

    <section class="section" id="contacts">
      <div class="container is-max-desktop">
        <h1 class="title is-1 is-spaced">Контакты</h1>
        <div class="content">
          <div class="box">
            <article class="media">
              <div class="columns">
                <div class="column is-narrow">
                  <figure class="image is-128x128">
                    <img src="./assets/tonya.png" loading="lazy">
                  </figure>
                </div>
                <div class="column">
                  <div class="content">
                    <p>
                      Куратор проекта — <a href="https://www.pushkin.institute/sveden/employees/detail.php?ELEMENT_ID=15425">Антонина Лапошина</a>
                    </p>
                    <p>
                      Если у вас возник вопрос, вы нашли ошибку или считаете, что не хватает
                      какой-то функции, обязательно напишите мне с пометкой "Текстометр".
                      Мы очень любим и ценим обратную связь!
                    </p>
                    <p>
                      <a href="mailto:antonina.laposhina@gmail.com">
                        <span class="icon-text">
                          <font-awesome-icon :icon="['far', 'envelope']" class="icon"/>
                          <span class="ml-1">antonina.laposhina@gmail.com</span>
                        </span>
                      </a>
                      <br>
                      <a href="https://www.facebook.com/antonina.laposhina">
                        <span class="icon-text">
                          <font-awesome-icon :icon="['fab', 'facebook']" class="icon"/>
                          <span class="ml-1">antonina.laposhina</span>
                        </span>
                      </a>
                    </p>
                  </div>
                </div>
              </div>
            </article>
          </div>
        </div>
      </div>
      <div v-if="loading || !text || !result || result.text_ok === false"
           class="container is-max-desktop has-text-centered mt-6">
        <a href="https://www.buymeacoffee.com/textometr">
          <img src="https://img.buymeacoffee.com/button-api/?text=Buy me a coffee&emoji=&slug=textometr&button_colour=FFDD00&font_colour=000000&font_family=Cookie&outline_colour=000000&coffee_colour=ffffff">
        </a>
      </div>
    </section>

    <footer class="footer pb-6 has-background-white-ter">
      <div class="content has-text-centered">
        <a href="https://digitalpushkin.tilda.ws/events">Лаборатория Института Пушкина</a>
      </div>
    </footer>
  </div>
</template>

<script>
import axios from 'axios'

const TEXT_FEATURES = {
  // параметры текста для русского как иностранного
  level_number: {
    title: 'Уровень текста',
    type: 'progress'
  },
  level_comment: {
    title: 'Уроверь текста',
    type: 'string'
  },
  sentences: {
    title: 'Предложений',
    type: 'number'
  },
  unique_words: {
    title: 'Уникальных слов',
    type: 'number'
  },
  key_words: {
    title: 'Ключевые слова',
    description: 'Это слова, наиболее характерные для этого текста. Они высчитываются с помощью рейтинга: количество раз, которое слово встречается в этом тексте / частота слова по Национальному корпусу русского языка (мера TF/IDF). Выигрывают слова, которые часто встречаются в данном тексте, но редко — во всех других текстах корпуса, то есть максимально характерные именно для этого текста.',
    type: 'array'
  },
  cool_words: {
    title: 'Самые полезные слова',
    description: 'Это слова-кандидаты в словарик по данному тексту; cлова, которые, скорее всего, ещё не знакомы студентам (их нет в лексических минимумах предыдущих уровней), но есть в минимуме данного уровня или в списке 3 000 самых частотных слов русского языка по НКРЯ.',
    type: 'array'
  },
  inA1: {
    title: 'Лексический список А1 покрывает',
    type: 'percent'
  },
  not_inA1: {
    title: 'Не входит в лексический список А1',
    type: 'array'
  },
  inA2: {
    title: 'Лексический список А2 покрывает',
    type: 'number'
  },
  not_inA2: {
    title: 'Не входит в лексический список А2',
    type: 'array'
  },
  inB1: {
    title: 'Лексический список B1 покрывает',
    type: 'number'
  },
  not_inB1: {
    title: 'Не входит в лексический список B1',
    type: 'array'
  },
  inB2: {
    title: 'Лексический список B2 покрывает',
    type: 'number'
  },
  not_inB2: {
    title: 'Не входит в лексический список B2',
    type: 'array'
  },
  inC1: {
    title: 'Лексический список C1 покрывает',
    type: 'number'
  },
  not_inC1: {
    title: 'Не входит в лексический список C1',
    type: 'array'
  },
  infr5000: {
    title: 'Частотный список 5000 покрывает',
    description: 'Список 5000 самых частотных слов русского языка из <a href="http://dict.ruslang.ru/freq.php" target="_blank">Нового частотного словаря русской лексики</a>',
    type: 'number'
  },
  cool_but_not_in_slovnik: {
    title: 'Полезные слова, которых нет в лексическом минимуме',
    type: 'array'
  },
  rare_words: {
    title: 'Редкие слова',
    type: 'array'
  },
  reading_for_detail_speed: {
    title: 'Изучающее чтение текста займет',
    type: 'string'
  },
  skim_reading_speed: {
    title: 'Просмотровое чтение текста займет',
    type: 'string'
  },
  gram_complex: {
    title: 'Возможные грамматические темы',
    description: 'Алгоритм подсчитывает количество частей речи и грамматических форм и предлагает темы, на которые в тексте можно найти наибольшее количество примеров.',
    type: 'array'
  },
  formula_pushkin: {
    title: 'Уровень сложности',
    type: 'progress'
  },
  structure_complex: {
    title: 'Структурная сложность',
    type: 'number'
  },
  lexical_complex: {
    title: 'Лексическая сложность',
    type: 'number'
  },
  narrativity: {
    title: 'Динамичность текста',
    type: 'number'
  },
  description: {
    title: 'Описательность текста',
    type: 'number'
  },
  words: {
    title: 'Слов',
    type: 'number'
  },
  mean_len_word: {
    title: 'Средняя длина слова',
    type: 'number'
  },
  mean_len_sentence: {
    title: 'Средняя длина предложения',
    type: 'number'
  },
  formula_flesh_oborneva: {
    title: 'Формула Флеша',
    type: 'number'
  },
  formula_flesh_kinc_oborneva: {
    title: 'Формула Флеша-Кинкейда',
    type: 'number'
  },
  lex_density: {
    title: 'Лексическая плотность',
    description: 'Отношение количества смысловых и служебных частей речи: чем плотность выше, тем текст сложнее.',
    type: 'number'
  },
  tt_ratio: {
    title: 'Лексическое разнообразие',
    description: 'Отношение количества уникальных слов текста к количеству всех слов текста. Обозначается величиной от 0 до 1 (когда все слова в тексте уникальны). Под словом здесь понимается лексема, т.е. все словоформы данной лексической единицы. Эта мера полезна для оценки повторяемости, воспроизводимости лексики текста.',
    type: 'number'
  },
  laposhina_list: {
    title: 'Список Русский детский 2000',
    description: 'Сколько процентов лексики текста покрывается списком из 2000 самых частотных слов для детской учебной литературы.',
    type: 'percent'
  },
  detcorpus_5000: {
    title: 'Список Русский детский 5000',
    description: 'Сколько процентов лексики текста покрывается списком из 5000 самых частотных слов для детской литературы.',
    type: 'percent'
  },
  rki_children_list: {
    title: 'Список Детский РКИ 4000',
    type: 'percent'
  },
  lexical_complex_rki: {
    title: 'Лексическая сложность текста для детей-иностранцев',
    type: 'number'
  },
  frequency_bag: {
    title: 'Частотный словарь по тексту',
    type: 'list'
  }
}

export default {
  name: 'App',
  data() {
    return {
      mode: 'foreign',
      loading: false,
      text: '',
      result: null,
      TEXT_FEATURES: TEXT_FEATURES,
      showAll: false,
      theme: 'light',
      hostname: location.hostname
    }
  },
  computed: {
    checkboxMode: {
      set: function(val) {
        this.mode = val ? 'native' : 'foreign'
      },
      get: function() {
        return this.mode === 'native'
      }
    },
    wordFrequencyArray: function() {
      let res = this.result && this.result.frequency_bag ? this.result.frequency_bag : []
      return this.showAll ? res : res.slice(0, 10)
    }
  },
  mounted() {
    if (localStorage.getItem('theme') === 'dark') {
      this.theme = 'dark'
      document.body.classList.add('dark-theme')
    }

    this.addMenuInteraction()
    this.addSmoothScrollForAllAnchors()
  },
  methods: {
    analyze: function () {
      this.clear()
      if (this.text.length < 10) {
          this.result = {
            text_ok: false,
            text_error_message: 'Текст слишком короткий.'
          }
      } else {
      this.loading = true
      axios.post('/analyze', { text: this.text, mode: this.mode })
        .then(response => {
          this.result = response.data
          if (response.data.text_ok) {
            setTimeout(() => {
              document.querySelector('#result').scrollIntoView({ behavior: 'smooth' })
            }, 0)
          }
        })
        .catch(error => {
          console.log(error)
          this.result = {
            text_ok: false,
            text_error_message: 'Упс, что-то пошло не так... Попробуйте позже.'
          }
        })
        .then(() => {
          this.loading = false
        })
      }
    },
    clear: function() {
      this.result = null
      this.showAll = false
    },
    getProgressClassForeign: function(level) {
      if (level <= 1) {
        return 'is-very-easy'
      }
      if (level > 1 && level <= 2) {
        return 'is-easy'
      }
      if (level > 2 && level <= 4.3) {
        return 'is-mild'
      }
      if (level > 4.3 && level <= 5.8) {
        return 'is-moderate'
      }
      if (level > 5.8 && level <= 6.8) {
        return 'is-upper-moderate'
      }
      if (level > 6.8 && level <= 7.9) {
        return 'is-difficult'
      }
      if (level > 7.9) {
        return 'is-very-difficult'
      }
    },
    getProgressClassNative: function(level) {
      if (level <= 2) {
        return 'is-very-easy'
      }
      if (level > 2 && level <= 6) {
        return 'is-easy'
      }
      if (level > 6 && level <= 7.5) {
        return 'is-mild'
      }
      if (level > 7.5 && level <= 8.5) {
        return 'is-upper-moderate'
      }
      if (level > 8.5 && level <= 9.1) {
        return 'is-difficult'
      }
      if (level > 9.1) {
        return 'is-very-difficult'
      }
    },
    download: function() {
      let content = `${this.text}\n\n`
      for (const [key, value] of Object.entries(this.result)) {
        if (TEXT_FEATURES[key]) {
          if (!Array.isArray(value) && value) {
            content += `*${TEXT_FEATURES[key].title}*\n${value}\n`
          }
          if (Array.isArray(value) && value.length > 0) {
            content += `*${TEXT_FEATURES[key].title}*\n`
            for (let v of value) {
              content += `${v}\n`
            }
          }
        }
      }
      this.downloadFile('textometr-result.txt', content)
    },
    downloadFile(filename, text) {
      var element = document.createElement('a');
      element.setAttribute('href', 'data:text/plain;charset=utf-8,' + encodeURIComponent(text))
      element.setAttribute('download', filename)

      element.style.display = 'none'
      document.body.appendChild(element)

      element.click()

      document.body.removeChild(element)
    },
    changeTheme() {
      if (this.theme === 'light') {
        this.theme = 'dark'
      } else {
        this.theme = 'light'
      }
      localStorage.setItem('theme', this.theme)
      document.body.classList.toggle('dark-theme')
    },
    toggleShowAll() {
      this.showAll = !this.showAll
    },
    addSmoothScrollForAllAnchors() {
      // add smooth scroll for all anchors
      document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
          e.preventDefault()

          document.querySelector(this.getAttribute('href')).scrollIntoView({
            behavior: 'smooth'
          })
        })
      })
    },
    addMenuInteraction() {
      // Get all "navbar-burger" elements
      const $navbarBurgers = Array.prototype.slice.call(document.querySelectorAll('.navbar-burger'), 0)

      // Check if there are any navbar burgers
      if ($navbarBurgers.length > 0) {
        // Add a click event on each of them
        $navbarBurgers.forEach( el => {
          el.addEventListener('click', () => {
            // Get the target from the "data-target" attribute
            const target = el.dataset.target;
            const $target = document.getElementById(target)

            // Toggle the "is-active" class on both the "navbar-burger" and the "navbar-menu"
            el.classList.toggle('is-active')
            $target.classList.toggle('is-active')
          })
        })
      }
    }
  }
}
</script>

<style lang="scss">

</style>
