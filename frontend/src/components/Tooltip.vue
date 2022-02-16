<template>
  <div class="tooltip">
    <span class="icon is-small icon-middle"><question-icon /></span>
    <span class="tooltiptext has-text-weight-normal" v-html="text"></span>
  </div>
</template>

<script>
export default {
  props: {
    text: String
  }
}
</script>

<style>
.tooltiptext a {
  color: #53a0f8 !important;
}

.tooltiptext a:hover {
  color: #a7cbf5 !important;
}
</style>
