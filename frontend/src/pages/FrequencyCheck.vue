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
      <div class="field">
        <div class="control">
          <input
            type="text"
            v-model="text"
            class="input"
            placeholder="Введите от 1 до 5 слов в начальной форме. Например: больница, поликлиника, клиника, госпиталь"
            @input="clear"
          />
        </div>
      </div>
      <div class="field is-grouped is-grouped-centered">
        <p class="control">
          <a class="button is-link is-rounded is-medium" @click="frequencyCheck">Проверить</a>
        </p>
      </div>
    </div>
  </section>

  <section class="section" id="result" v-if="result && !loading">
    <div class="container is-max-desktop">
      <h1 class="title is-1">Результат</h1>
      <table class="table is-hoverable is-fullwidth">
        <tbody>
          <tr>
            <th>Общая оценка</th>
            <td></td>
          </tr>
          <tr>
            <th>Первое появление в ЛМ</th>
            <td></td>
          </tr>
          <tr>
            <th>Частотность по ЧС НКРЯ</th>
            <td></td>
          </tr>
          <tr>
            <th>Частотность по Деткорпусу</th>
            <td></td>
          </tr>
          <tr>
            <th>Частотность по RuFoLa</th>
            <td></td>
          </tr>
          <tr>
            <th>Частотность по корпусу учебников РЯ: TIRTEC - РКИ</th>
            <td></td>
          </tr>
          <tr>
            <th>TIRTEC - билингвы</th>
            <td></td>
          </tr>
          <tr>
            <th>TIRTEC - носители</th>
            <td></td>
          </tr>
        </tbody>
      </table>
    </div>
  </section>

  <section class="section">
    <div class="container is-max-desktop">
      <h1 class="title is-1 is-spaced">
        Частотные списки русского языка, использованные в расчетах
      </h1>
      <div class="content">
        <p>
          ЧС НКРЯ:
          <a href="http://dict.ruslang.ru/freq.php"
            >Новый частотный словарь русской лексики (О. Н. Ляшевская, С. А. Шаров)</a
          >
        </p>
        <p>
          ДетКорпус:
          <a href="http://detcorpus.ru/pages/about.html"
            >Корпус русской детской литературы XX—XXI в.</a
          >
        </p>
        <p>
          RuFoLa: корпус текстов из учебников русского языка как иностранного (для взрослых
          учащихся)
        </p>
        <p>
          TIRTEC:
          <a href="https://digitalpushkin.tilda.ws/tirtec"
            >Корпус текстов из учебников русского языка для детей младшего школьного возраста</a
          >
        </p>
      </div>
    </div>
  </section>
</template>

<script>
import axios from 'axios'

export default {
  data() {
    return {
      loading: false,
      text: '',
      result: true
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
          if (response.data.text_ok) {
            setTimeout(() => {
              document.querySelector('#result').scrollIntoView({ behavior: 'smooth' })
            }, 0)
          }
        })
        .catch((error) => {
          console.log(error)
          this.result = {
            text_ok: false,
            text_error_message: 'Упс, что-то пошло не так... Попробуйте позже.'
          }
        })
        .then(() => {
          this.loading = false
        })
    },
    clear: function () {
      this.result = null
    }
  }
}
</script>
