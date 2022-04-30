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

      <h5>Block # {{ blocknumber }}</h5>
      <q-separator color="black" />

      <div>
        <q-card class="my-card">
          <q-card-section class="details">
            <p>Block ID : {{}}</p>
            <p>Hash : {{}}</p>
            <p>Transactions : {{}}</p>
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
  name: 'ExplorerBlockDetails',
  components: {},
  setup() {
    return {};
  },

  data() {
    return {
      blocknumber: '1234',
    };
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
  margin-left: auto;
  margin-right: auto;
  width: 50%;
  padding: 2%;
}

.details {
  font-size: 1.5em;
  padding: 2%;
  padding-left: 4%;
}
</style>
