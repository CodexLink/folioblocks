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

      <h5>Transactions</h5>
      <q-separator color="black" />

      <div class="q-pa-md">
        <q-table
          :rows="transactionrows"
          :columns="transactioncolumns"
          row-key="name"
        />
      </div>
    </q-page-container>
  </q-layout>
</template>

<script>
import { defineComponent } from 'vue';

const transactioncolumns = [
  {
    name: 'Text',
    align: 'center',
    label: 'TX Hash',
    field: '',
  },
  { name: 'Text', align: 'center', label: 'Time', field: '' },
  { name: 'Text', align: 'center', label: 'From', field: '' },

  { name: 'Text', align: 'center', label: 'To', field: '' },
  { name: 'Text', align: 'center', label: 'Validator', field: '' },

  { name: 'Text', align: 'center', label: 'Action Type', field: '' },
];

const transactionrows = [
  {
    name: '',
  },
  {
    name: '',
  },
  {
    name: '',
  },
  {
    name: '',
  },
  {
    name: '',
  },
  {
    name: '',
  },
  {
    name: '',
  },
];

export default defineComponent({
  name: 'ExplorerTransaction',
  components: {},
  setup() {
    return {
      transactioncolumns,
      transactionrows,
    };
  },

  data() {
    return {};
  },
});
</script>

<style scoped>
/* Navigation bar*/

.drawer {
  display: grid;
  text-align: center;
  margin: 6%;
  margin-top: 50%;
  gap: 3.5rem;
}

.btndrawer {
  font-size: 1.3em;
  font-family: 'Poppins';
}

h2 {
  font-family: 'Poppins';
  font-size: 2.5em;
  font-weight: 500;
  text-align: center;
  margin-bottom: 1%;
}

h4 {
  font-family: 'Poppins';
  font-size: 1.4em;
}

p {
  font-size: 1.3em;
}

img {
  height: 50px;
  width: 50px;
  float: left;
  margin: 5%;
}

.toolbar-items {
  font-size: 0.8em;
  font-family: 'Poppins';
  margin-left: 5%;
}

.webtitle {
  font-family: 'Poppins';
  margin-left: 1%;
}

.logo {
  margin-right: 1.5%;
  margin: 0.5%;
}

/* Navigation bar end*/

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
</style>
