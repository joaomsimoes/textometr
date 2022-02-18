<template>
  <section class="section">
    <div class="container is-max-desktop">
      <h4 class="title is-4 has-text-centered">Проверка частотности слов</h4>
      <article class="message">
        <div class="message-body">
          Сервис проверки частотности слов предлагает анализ лексики сразу по нескольким частотным
          словарям. Вы можете получить частотный анализ одного слова или сравнить частотность,
          например, нескольких близких по значению слов.
        </div>
      </article>
      <article v-if="errorMessage" class="message is-danger">
        <div class="message-body">
          {{ errorMessage }}
        </div>
      </article>
      <div class="field">
        <div class="control">
          <input
            type="text"
            v-model="text"
            class="input"
            placeholder="Введите от 1 до 5 слов в начальной форме. Например: больница, поликлиника, клиника, госпиталь"
            @input="clear"
            @keyup.enter="frequencyCheck"
          />
        </div>
      </div>
      <div class="field is-grouped is-grouped-centered">
        <p class="control">
          <a
            class="button is-link is-rounded is-medium"
            :class="{
              'is-loading': loading
            }"
            @click="frequencyCheck"
            >Проверить</a
          >
        </p>
      </div>
    </div>
  </section>

  <section class="section" id="result" v-if="result && !loading">
    <div class="container is-max-desktop">
      <h1 class="title is-1">Результат</h1>
      <table class="table is-hoverable is-fullwidth is-bordered">
        <tbody>
          <tr>
            <td></td>
            <td v-for="item in result" class="has-text-centered">
              <span class="is-size-5 has-text-weight-semibold">{{ item['lemma'] }}</span>
            </td>
          </tr>
          <tr>
            <th>Часть речи</th>
            <td v-for="item in result" class="has-text-centered">
              <template v-if="item['pos']">
                {{ item['pos'] }}
              </template>
              <span v-else class="icon is-small">
                <x-mark-icon />
              </span>
            </td>
          </tr>
          <tr>
            <th>Частотность по текстам для взрослых</th>
            <td v-for="item in result" class="has-text-centered">
              <template v-if="item['comment_main']">
                {{ item['comment_main'] }}
              </template>
              <span v-else class="icon is-small">
                <x-mark-icon />
              </span>
            </td>
          </tr>
          <tr>
            <th>Частотность по текстам для детей</th>
            <td v-for="item in result" class="has-text-centered">
              <template v-if="item['comment_child']">
                {{ item['comment_child'] }}
              </template>
              <span v-else class="icon is-small">
                <x-mark-icon />
              </span>
            </td>
          </tr>
          <tr>
            <th>Уровень по лексическим минимумам ТРКИ</th>
            <td v-for="item in result" class="has-text-centered">
              <template v-if="item['cefr']">
                {{ item['cefr'] }}
              </template>
              <span v-else class="icon is-small">
                <x-mark-icon />
              </span>
            </td>
          </tr>
          <tr>
            <th>Уровень по спискам KELLY</th>
            <td v-for="item in result" class="has-text-centered">
              <template v-if="item['kelly']">
                {{ item['kelly'] }}
              </template>
              <span v-else class="icon is-small">
                <x-mark-icon />
              </span>
            </td>
          </tr>
          <tr>
            <th>Частотность по Новому частотному словарю русской лексики, ipm</th>
            <td v-for="item in result" class="has-text-centered">
              <template v-if="item['rnc_ipm']">
                {{ item['rnc_ipm'] }}
              </template>
              <span v-else class="icon is-small">
                <x-mark-icon />
              </span>
            </td>
          </tr>
          <tr>
            <th>Частотность по корпусу литературы для детей Деткорпус, ipm</th>
            <td v-for="item in result" class="has-text-centered">
              <template v-if="item['detcorpus_ipm']">
                {{ item['detcorpus_ipm'] }}
              </template>
              <span v-else class="icon is-small">
                <x-mark-icon />
              </span>
            </td>
          </tr>
          <tr>
            <th>Частотность по корпусу учебников РКИ RuFoLa (A1-B1), ipm</th>
            <td v-for="item in result" class="has-text-centered">
              <template v-if="item['rufola_123_ipm']">
                {{ item['rufola_123_ipm'] }}
              </template>
              <span v-else class="icon is-small">
                <x-mark-icon />
              </span>
            </td>
          </tr>
          <tr>
            <th :colspan="result.length + 1">
              <div class="mt-5">
                Частотность по корпусу учебников РЯ для детей младшего школьного возраста TIRTEC,
                ipm
              </div>
            </th>
          </tr>
          <tr>
            <th>Дети-инофоны</th>
            <td v-for="item in result" class="has-text-centered">
              <template v-if="item['det_rki_ipm']">
                {{ item['det_rki_ipm'] }}
              </template>
              <span v-else class="icon is-small">
                <x-mark-icon />
              </span>
            </td>
          </tr>
          <tr>
            <th>Дети-билингвы</th>
            <td v-for="item in result" class="has-text-centered">
              <template v-if="item['bilingual_ipm']">
                {{ item['bilingual_ipm'] }}
              </template>
              <span v-else class="icon is-small">
                <x-mark-icon />
              </span>
            </td>
          </tr>
          <tr>
            <th>Дети-российские школьники</th>
            <td v-for="item in result" class="has-text-centered">
              <template v-if="item['native_ipm']">
                {{ item['native_ipm'] }}
              </template>
              <span v-else class="icon is-small">
                <x-mark-icon />
              </span>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </section>

  <section class="section">
    <div class="container is-max-desktop">
      <h1 class="title is-1">Литература</h1>
      <h5 class="title is-5">Частотные списки русского языка, использованные в расчетах</h5>
      <div class="content">
        <ol>
          <li>
            <strong class="mr-2">ЧС НКРЯ:</strong>
            <a href="http://dict.ruslang.ru/freq.php"
              >Новый частотный словарь русской лексики (О. Н. Ляшевская, С. А. Шаров)</a
            >
          </li>
          <li>
            <strong class="mr-2">ДетКорпус:</strong>
            <a href="http://detcorpus.ru/pages/about.html"
              >Корпус русской детской литературы XX—XXI в.</a
            >
          </li>
          <li>
            <strong class="mr-2">RuFoLa:</strong>
            Корпус текстов из учебников русского языка как иностранного (для взрослых учащихся)
          </li>
          <li>
            <strong class="mr-2">TIRTEC:</strong>
            <a href="https://digitalpushkin.tilda.ws/tirtec"
              >Корпус текстов из учебников русского языка для детей младшего школьного возраста</a
            >
          </li>
          <li>
            <strong class="mr-2">KELLY:</strong>
            <a href="http://corpus.leeds.ac.uk/serge/kelly/">Списки проекта KELLY</a>
          </li>
        </ol>
      </div>

      <h5 class="title is-5">Система лексических минимумов по русскому языку как иностранному</h5>
      <div class="content">
        <ol>
          <li>
            Система лексических минимумов по русскому языку как иностранному: Лексический минимум по
            русскому языку как иностранному. Элементарный уровень. Общее владение / под ред. Н.П.
            Андрюшиной, Т.В. Козловой. – 4е изд., испр. и доп. – СПб. : Златоуст, 2012. – 80 с.
          </li>
          <li>
            Лексический минимум по русскому языку как иностранному. Базовый уровень. Общее владение
            / Н.П. Андрюшина, Т.В. Козлова (электронное издание). – 5е изд. – СПб. : Златоуст,2015.
            – 116 с.
          </li>
          <li>
            Лексический минимум по русскому языку как иностранному. Первый сертификационный уровень.
            Общее владение / Н.П. Андрюшина и др. – 9е изд. – СПб. : Златоуст, 2017. – 200 с.
          </li>
          <li>
            Лексический минимум по русскому языку как иностранному. Второй сертификационный уровень.
            Общее владение / под редакцией Н.П. Андрюшиной. – 7-е изд. – СПб. : Златоуст, 2017. –
            164 с.
          </li>
          <li>
            Лексический минимум по русскому языку как иностранному. Третий сертификационный уровень.
            Общее владение / под ред. Н.П. Андрюшиной. – СПб. : Златоуст, 2018. – 201 с.
          </li>
        </ol>
      </div>
    </div>
  </section>
</template>

<script>
import axios from 'axios'
import { useHead } from '@vueuse/head'

export default {
  setup() {
    useHead({
      title: 'Текстометр. Проверка частотности слов',
      meta: [
        {
          name: 'description',
          content:
            'Сервис проверки частотности слов предлагает анализ лексики сразу по нескольким частотным словарям. Вы можете получить частотный анализ одного слова или сравнить частотность, например, нескольких близких по значению слов.'
        }
      ]
    })
  },

  data() {
    return {
      loading: false,
      text: '',
      result: null,
      errorMessage: null
    }
  },
  methods: {
    frequencyCheck: function () {
      this.clear()
      this.loading = true
      axios
        .post('/api/frequency', { text: this.text })
        .then((response) => {
          this.result = response.data
          setTimeout(() => {
            document.querySelector('#result').scrollIntoView({ behavior: 'smooth' })
          }, 0)
        })
        .catch((error) => {
          console.log(error)
          this.errorMessage = 'Упс, что-то пошло не так... Попробуйте позже.'
        })
        .then(() => {
          this.loading = false
        })
    },
    clear: function () {
      this.result = null
      this.errorMessage = null
    }
  }
}
</script>
