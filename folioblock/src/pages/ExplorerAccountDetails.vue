<template>
  <q-layout view="hHh lpR lFf">
    <q-page-container>
      <div class="header">
        <q-avatar class="usericon" icon="account_circle" />

        <div class="username">
          <h3>Profile</h3>
          <p class="user">{{ user }}</p>
        </div>
      </div>

      <div>
        <q-card class="my-card">
          <q-card-section class="details">
            <p>Text : {{}}</p>
            <p>Text : {{}}</p>
            <p>Text : {{}}</p>
            <p>Text : {{}}</p>
          </q-card-section>
        </q-card>
      </div>

      <div class="row">
        <h5>Transactions</h5>
      </div>

      <div class="q-pa-md table">
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
    label: 'Text',
    field: '',
  },
  { name: 'Text', align: 'center', label: 'Text', field: '' },
  { name: 'Text', align: 'center', label: 'Text', field: '' },
  {
    name: 'Text',
    align: 'center',
    label: 'Text',
    field: '',
  },
  { name: 'Text', align: 'center', label: 'Text', field: '' },
  { name: 'Text', align: 'center', label: 'Text', field: '' },
  {
    name: 'Text',
    align: 'center',
    label: 'Text',
    field: '',
  },
  { name: 'Text', align: 'center', label: 'Text', field: '' },
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
  name: 'ExplorerAccountDetails',
  components: {},
  setup() {
    return {
      transactioncolumns,
      transactionrows,
    };
  },

  data() {
    return {
      user: '0x7sd64033213213213133c',
    };
  },
});
</script>

<style scoped>
h5 {
  font-family: 'Poppins';
  font-weight: 500;
  margin: 0.5%;
  margin-left: 4%;
}

h3 {
  font-family: 'Poppins';
  font-weight: 500;
  margin-top: 7%;
  line-height: 25px;
}

p {
  font-family: 'Poppins';
  font-size: 1.5em;
}

.usericon {
  font-size: 200px;
}

.user {
  font-family: 'Poppins';
  font-size: 1.5em;
  font-weight: 600;
  line-height: 0px;
}

.table {
  margin: 3%;
  margin-top: 0%;
  margin-bottom: 0%;
}

.my-card {
  margin-left: 4%;
  margin-right: 4%;
  margin-bottom: 2%;
}

.details {
  font-size: 0.8em;
  padding: 2%;
  padding-left: 4%;
}

.header {
  display: grid;
  margin: 3%;
  margin-top: 1%;
  grid-template-columns: 10% 50%;
}

@media (max-width: 90em) {
  .usericon {
    font-size: 150px;
  }

  .user {
    font-family: 'Poppins';
    font-size: 1.5em;
    font-weight: 600;
    line-height: 0px;
  }

  h3 {
    font-family: 'Poppins';
    font-weight: 500;
    margin-top: 40px;
    line-height: 25px;
    margin-right: 3%;
  }

  .header {
    display: grid;
    margin: 3%;
    margin-top: 1%;
    grid-template-columns: 150px 500px;
  }
  .my-card {
    margin-left: 5%;
    margin-right: 5%;
    margin-bottom: 2%;
  }
}

@media (max-width: 40em) {
  .usericon {
    font-size: 100px;
  }

  .user {
    font-family: 'Poppins';
    font-size: 1em;
    font-weight: 600;
    line-height: 0px;
  }

  h3 {
    font-size: 1.5em;
    font-family: 'Poppins';
    font-weight: 500;
    margin-top: 20px;
    line-height: 25px;
    margin-right: 3%;
  }

  .header {
    display: grid;
    margin: 3%;
    margin-top: 1%;
    grid-template-columns: 30% 100%;
  }

  p {
    font-family: 'Poppins';
    font-size: 1em;
  }

  .my-card {
    margin-left: 6%;
    margin-right: 6%;
    margin-bottom: 2%;
  }
}
</style>
