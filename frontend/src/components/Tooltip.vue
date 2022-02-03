<template>
  <div class="tooltip">
    <span class="icon is-small icon-middle"><question-icon /></span>
    <span class="tooltiptext has-text-weight-normal">{{ text }}</span>
  </div>
</template>

<script>
export default {
  props: {
    text: String,
  },
};
</script>
