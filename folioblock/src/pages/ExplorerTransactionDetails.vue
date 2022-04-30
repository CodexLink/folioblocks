<template>
  <q-layout view="hHh lpR lFf">
    <q-page-container>
      <div class="header">
        <q-btn
          class="back"
          outline
          round
          color="black"
          icon="arrow_back"
          to="/explorerdashboard"
        />

        <q-input
          class="searchbar"
          v-model="search"
          debounce="500"
          filled
          placeholder="Search"
        >
          <template v-slot:append>
            <q-icon name="search" />
          </template>
        </q-input>
      </div>
      <q-separator color="black" />

      <h5>Transaction Details</h5>
      <q-separator color="black" />

      <div>
        <q-card class="my-card">
          <q-card-section class="details">
            <p>Transaction Hash : {{}}</p>
            <p>Status : {{}}</p>
            <p>From : {{}}</p>
            <p>To : {{}}</p>
            <p>Validator : {{}}</p>
          </q-card-section>
        </q-card>
      </div>
    </q-page-container>
  </q-layout>
</template>

<script>
import { defineComponent } from 'vue';

export default defineComponent({
  name: 'ExplorerTransactionDetails',
  components: {},
  setup() {
    return {};
  },

  data() {
    return {};
  },
});
</script>

<style scoped>
.header {
  display: grid;
  margin: 1%;
  gap: 1.5rem;
  grid-template-columns: repeat(2, 1fr);
}
.back {
  margin: 1%;
  height: 30px;
  width: 30px;
}

h5 {
  font-family: 'Poppins';
  font-weight: 500;
  margin: 0.5%;
  margin-left: 4%;
}

.my-card {
  margin: 2%;
}

.details {
  font-size: 1.5em;
  padding: 2%;
  padding-left: 4%;
}
</style>
