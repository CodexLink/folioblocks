<template>
  <div style="max-width: 100%; padding-bottom: 10%">
    <slot></slot>
  </div>
</template>

<style scoped>
div {
  margin-top: 0%;
  margin-left: 35%;
  margin-right: 35%;
}

@media (max-width: 100em) {
  div {
    margin: 0%;
    margin-left: 30%;
    margin-right: 30%;
  }
}

@media (max-width: 60em) {
  div {
    margin: 0%;
    margin-left: 10%;
    margin-right: 10%;
  }
}
</style>
