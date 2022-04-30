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

      <h5>Blocks</h5>
      <q-separator color="black" />

      <div class="q-pa-md">
        <q-table :rows="blocksrows" :columns="blockscolumns" row-key="name" />
      </div>
    </q-page-container>
  </q-layout>
</template>

<script>
import { defineComponent } from 'vue';

const blockscolumns = [
  {
    name: 'Text',
    align: 'center',
    label: 'Block ID',
    field: '',
  },
  { name: 'Text', align: 'center', label: 'Time', field: '' },

  { name: 'Text', align: 'center', label: 'No. of Transaction', field: '' },

  {
    name: 'Text',
    align: 'center',
    label: 'Address Validator',
    field: '',
  },
];

const blocksrows = [
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
      blockscolumns,
      blocksrows,
    };
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
</style>
