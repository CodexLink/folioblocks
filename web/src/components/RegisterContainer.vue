<template>
  <div style="max-width: 100%">
    <slot></slot>
  </div>
</template>

<style scoped>
div {
  margin-top: 0%;
  margin-left: 35%;
  margin-right: 35%;
  font-family: 'Poppins';
}

@media (max-width: 100em) {
  div {
    margin: 0%;
    margin-left: 30%;
    margin-right: 30%;
    font-family: 'Poppins';
  }
}

@media (max-width: 60em) {
  div {
    margin: 0%;
    margin-left: 10%;
    margin-right: 10%;
    font-family: 'Poppins';
  }
}
</style>
