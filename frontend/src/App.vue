<template>
  <nav class="bd-navbar navbar has-shadow" role="navigation" aria-label="main navigation">
    <div class="container">
      <div class="navbar-brand">
        <a class="navbar-item" href="https://textometr.ru">
          <img id="logo" src="/src/assets/logo.svg" />
          <span id="logo-text">Текстомéтр</span>
        </a>

        <a
          role="button"
          class="navbar-burger"
          :class="{ 'is-active': burgerActive }"
          aria-label="menu"
          aria-expanded="false"
          @click="burgerActive = !burgerActive"
        >
          <span aria-hidden="true"></span>
          <span aria-hidden="true"></span>
          <span aria-hidden="true"></span>
        </a>
      </div>
      <div class="navbar-menu" :class="{ 'is-active': burgerActive }">
        <div class="navbar-end">
          <a class="navbar-item" @click="goToPage('/')">Анализ сложности текста</a>
          <a class="navbar-item" @click="goToPage('/frequency-check')">Проверка частотности слов</a>
          <a class="navbar-item" id="contacts-ref" @click="goToContacts" href="#contacts"
            >Контакты</a
          >
          <a class="navbar-item" href="https://www.facebook.com/textometr">Мы в Facebook</a>
          <div class="navbar-item">
            <span class="icon is-small is-clickable" @click="changeTheme">
              <moon-icon v-if="theme === 'light'" />
              <sun-icon v-if="theme === 'dark'" class="sun" />
            </span>
          </div>
        </div>
      </div>
    </div>
  </nav>

  <router-view></router-view>

  <section class="section" id="contacts">
    <div class="container is-max-desktop">
      <h1 class="title is-1 is-spaced">Контакты</h1>
      <div class="content">
        <div class="box">
          <article class="media">
            <div class="columns">
              <div class="column is-narrow">
                <figure class="image is-128x128">
                  <img src="./assets/tonya.png" loading="lazy" />
                </figure>
              </div>
              <div class="column">
                <div class="content">
                  <p>
                    Куратор проекта —
                    <a
                      href="https://www.pushkin.institute/sveden/employees/detail.php?ELEMENT_ID=15425"
                      >Антонина Лапошина</a
                    >
                  </p>
                  <p>
                    Если у вас возник вопрос, вы нашли ошибку или считаете, что не хватает какой-то
                    функции, обязательно напишите мне с пометкой "Текстометр". Мы очень любим и
                    ценим обратную связь!
                  </p>
                  <p>
                    <a href="mailto:antonina.laposhina@gmail.com">
                      <span class="icon-text">
                        <span class="icon is-small"><email-icon /></span>
                        <span class="ml-1">antonina.laposhina@gmail.com</span>
                      </span>
                    </a>
                    <br />
                    <a href="https://www.facebook.com/antonina.laposhina">
                      <span class="icon-text">
                        <span class="icon is-small"><facebook-icon /></span>
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
    <div class="container is-max-desktop has-text-centered mt-6">
      <a href="https://pay.cloudtips.ru/p/d53d30d0">
        <button class="button donate">Поддержать проект 💸</button>
      </a>
    </div>
  </section>

  <footer class="footer pb-6 has-background-white-ter">
    <div class="content has-text-centered">
      <a href="https://digitalpushkin.tilda.ws/events">Лаборатория Института Пушкина</a>
    </div>
  </footer>
</template>

<script>
export default {
  data() {
    return {
      theme: 'light',
      burgerActive: false
    }
  },
  mounted() {
    if (localStorage.getItem('theme') === 'dark') {
      this.theme = 'dark'
      document.body.classList.add('dark-theme')
    }
  },
  methods: {
    changeTheme() {
      this.burgerActive = false
      if (this.theme === 'light') {
        this.theme = 'dark'
      } else {
        this.theme = 'light'
      }
      localStorage.setItem('theme', this.theme)
      document.body.classList.toggle('dark-theme')
    },

    goToContacts(e) {
      this.burgerActive = false
      e.preventDefault()

      document.querySelector(e.target.getAttribute('href')).scrollIntoView({
        behavior: 'smooth'
      })
    },

    goToPage(page) {
      this.burgerActive = false
      this.$router.push(page)
    }
  }
}
</script>

<style scoped></style>
