<template>
  <q-layout view="hHh lpR lFf">
    <q-page-container>
      <div>
        <h2>Explorer</h2>
      </div>
      <div class="search">
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

      <div class="header">
        <q-card class="profile">
          <q-card-section>
            <h2>Hello {{ user }}</h2>
            <p class="alias">You are also known as {{ alias }}</p>
            <div class="btn">
              <q-btn
                outline
                rounded
                color="black"
                label="View Your Profile"
                to="/exploreraccountdetails"
              />
              <q-btn outline rounded color="black" label="Recruit People" />
              <q-btn
                outline
                rounded
                color="black"
                label="Generate Certificate"
              />
            </div>
          </q-card-section>
        </q-card>

        <q-card class="status">
          <q-avatar class="icon" icon="view_in_ar" />
          <div>
            <h4>Total Blocks</h4>
            <p class="dataheader">{{ blocks }}</p>
          </div>

          <q-avatar class="icon" icon="schedule" />
          <div>
            <h4>Block Time</h4>
            <p class="dataheader">{{ time }}</p>
          </div>

          <q-avatar class="icon" icon="swap_horiz" />
          <div>
            <h4>Total TXS</h4>
            <p class="dataheader">{{ txs }}</p>
          </div>

          <q-avatar class="icon" icon="person" />
          <div>
            <h4>Total Addresses</h4>
            <p class="dataheader">{{ addresses }}</p>
          </div>
        </q-card>
      </div>

      <div class="main">
        <div class="row">
          <h5>Latest Blocks</h5>
          <q-btn
            class="viewall"
            rounded
            color="accent"
            text-color="black"
            label="View All"
            to="/explorerblocks"
          />
        </div>

        <q-table
          :rows="transactionrows"
          :columns="transactioncolumns"
          row-key="name"
        />
        <div class="row gridblock">
          <h5>Latest Transactions</h5>
          <q-btn
            class="viewall"
            rounded
            color="accent"
            text-color="black"
            label="View All"
            to="/explorertransaction"
          />
        </div>
        <q-table
          :rows="blocksrows"
          :columns="blockscolumns"
          row-key="name"
          @row-click="link()"
        />
      </div>
    </q-page-container>
  </q-layout>
</template>

<script>
import { defineComponent, ref } from 'vue';

const transactioncolumns = [
  {
    name: 'Text',
    align: 'center',
    label: 'TX Hash',
    field: '',
  },
  { name: 'Text', align: 'center', label: 'Details', field: '' },
  { name: 'Text', align: 'center', label: 'Text', field: '' },
];

const transactionrows = [];

const blockscolumns = [
  { name: 'block', align: 'center', label: 'Block ID', field: 'block' },
  { name: 'Text', align: 'center', label: 'Details', field: '' },
];

const blocksrows = [
  {
    name: '1',
    block: '2',
  },
];

export default defineComponent({
  name: 'ExplorerDashboard',

  setup() {
    return {
      transactioncolumns,
      transactionrows,
      blockscolumns,
      blocksrows,
      search: ref(''),
    };
  },

  data() {
    return {
      user: '0x3a6a41bf23',
      alias: 'Ronan',

      blocks: '100000',
      time: '2 ms',
      txs: '10000',
      addresses: '100000',

      blockid: '',
      hash: '',
      transactions: '',
      validator: '',
    };
  },

  methods: {
    link() {
      void this.$router.push('/explorerblockdetails');
    },
  },
});
</script>

<style scoped>
.my-card-blocksdata {
  width: 100%;
  height: 60%;
}

/* User Info and Block info */
.header {
  display: grid;
  margin: 6%;
  margin-top: 0%;
  gap: 1.5rem;
  grid-template-columns: repeat(2, 1fr);
}

.profile {
  background-color: #a7eaff;
  height: 100%;
}

.alias {
  font-family: 'Poppins';
  font-size: 1.3em;
  text-align: center;
  margin-bottom: 5%;
}

.btn {
  display: grid;
  gap: 1em;
  grid-template-columns: repeat(3, 1fr);
  padding: 1%;
  font-size: 1em;
}

.status {
  display: grid;
  grid-template-columns: 20% 30% 20% 30%;
  background-color: #a7eaff;
}
.icon {
  font-size: 150px;
  margin-left: 20%;
}

.dataheader {
  font-size: 2em;
  font-family: 'Poppins';
  font-weight: 500;
  line-height: 0px;
  margin-left: 10%;
}

h4 {
  font-family: 'Poppins';
  font-size: 1.8em;
  font-weight: 400;
  margin-left: 10%;
}
/* User Info and Block info end */

.search {
  display: grid;
  margin: 6%;
  margin-bottom: 2%;
  margin-top: 2%;
}

.searchbar {
  width: 50%;
  margin-left: auto;
  margin-right: auto;
}

/* Table */

.main {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 1.5rem;
  margin: 6%;
  margin-bottom: 0%;
  padding-bottom: 3%;
  margin-top: 2%;
}

h5 {
  font-family: 'Poppins';
  font-weight: 500;
  margin: 0%;
}

h2 {
  font-family: 'Poppins';
  font-size: 2.5em;
  font-weight: 500;
  text-align: center;
  margin-bottom: 1%;
  word-break: break-all;
}

.viewall {
  margin-left: 5%;
}

.gridblock {
  grid-row-start: 1;
}

@media (max-width: 90em) {
  .header {
    display: grid;
    margin: 6%;
    gap: 1.5rem;
    grid-template-columns: repeat(1, 1fr);
  }

  .status {
    display: grid;
    grid-template-columns: 15% 35% 15% 35%;
  }

  .main {
    display: grid;
    grid-template-columns: repeat(1, 1fr);
    gap: 1.5rem;
    margin: 6%;
    margin-bottom: 0%;
    padding-bottom: 3%;
    margin-top: 2%;
  }

  .gridblock {
    grid-row-start: 3;
  }

  .icon {
    font-size: 100px;
    margin-left: 40%;
  }

  h4 {
    font-family: 'Poppins';
    font-size: 0.8em;
    font-weight: 400;
    line-height: 30px;
    margin-left: 0%;
  }

  p {
    font-size: 1em;
    font-family: 'Poppins';
  }
  .dataheader {
    font-size: 1em;
    font-family: 'Poppins';
    font-weight: 500;
    line-height: 0px;
    margin-left: 0%;
  }
  h5 {
    font-size: 1.3em;
    font-family: 'Poppins';
    font-weight: 500;
    margin: 0%;
  }

  .btn {
    display: grid;
    gap: 1em;
    grid-template-columns: repeat(1, 1fr);
    padding: 1%;
    font-size: 0.5em;
  }

  .viewall {
    margin-left: 5%;
    font-size: 0.8em;
  }

  h2 {
    font-family: 'Poppins';
    font-size: 2em;
    font-weight: 500;
    text-align: center;
    margin-bottom: 1%;
    overflow: hidden;
  }

  .alias {
    font-family: 'Poppins';
    font-size: 1em;
    text-align: center;
    margin-bottom: 5%;
  }
}

@media (max-width: 60em) {
  .header {
    display: grid;
    margin: 6%;
    gap: 1.5rem;
    grid-template-columns: repeat(1, 1fr);
  }

  .status {
    display: grid;
    grid-template-columns: 25% 25% 25% 25%;
  }

  .main {
    display: grid;
    grid-template-columns: repeat(1, 1fr);
    gap: 1.5rem;
    margin: 6%;
    margin-bottom: 0%;
    padding-bottom: 3%;
    margin-top: 2%;
  }

  .gridblock {
    grid-row-start: 3;
  }

  .icon {
    font-size: 90px;
    margin-left: 1%;
  }

  h4 {
    font-family: 'Poppins';
    font-size: 0.8em;
    font-weight: 400;
    line-height: 15px;
    margin-left: 0%;
  }

  p {
    font-size: 1em;
    font-family: 'Poppins';
  }
  .dataheader {
    font-size: 1em;
    font-family: 'Poppins';
    font-weight: 500;
    line-height: 0px;
    margin-left: 0%;
  }
  h5 {
    font-size: 1.3em;
    font-family: 'Poppins';
    font-weight: 500;
    margin: 0%;
  }

  .btn {
    display: grid;
    gap: 1em;
    grid-template-columns: repeat(1, 1fr);
    padding: 1%;
    font-size: 0.5em;
  }

  .viewall {
    margin-left: 5%;
    font-size: 0.8em;
  }

  h2 {
    font-family: 'Poppins';
    font-size: 2em;
    font-weight: 500;
    text-align: center;
    margin-bottom: 1%;
  }

  .alias {
    font-family: 'Poppins';
    font-size: 1em;
    text-align: center;
    margin-bottom: 5%;
  }
}
</style>
