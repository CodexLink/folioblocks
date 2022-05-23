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
          to="/explorer"
        />
      </div>
      <q-separator color="black" />
      <h5>Transactions</h5>
      <q-separator color="black" />

      <div class="q-pa-md">
        <q-table
          :rows="tx_rows"
          :columns="tx_cols"
          row-key="id"
          :loading="txs_loading_state"
          :rows-per-page-options="[default_tx_rows]"
          no-data-label="Failed to fetch from the chain or theres no transactions from chain to render."
        >
          <template v-slot:top-right>
            <q-btn
              color="green"
              icon-right="refresh"
              label="Refresh"
              no-caps
              @click="getTransactions"
            />
          </template>
          <template v-slot:body="props">
            <q-tr :props="props">
              <q-td key="Transaction Number" :props="props">{{
                props.row.id
              }}</q-td>
              <q-td key="Transaction Hash" :props="props">
                <router-link
                  :to="'/explorer/transaction/' + props.row.tx_hash"
                  style="text-decoration: none"
                  >{{ props.row.tx_hash }}</router-link
                ></q-td
              >
              <q-td key="Transaction Action" :props="props">{{
                props.row.action
              }}</q-td>
              <q-td key="From Address" :props="props">
                <router-link
                  :to="'/explorer/address/' + props.row.from_address"
                  style="text-decoration: none"
                  >{{ props.row.from_address }}</router-link
                >
              </q-td>
              <q-td key="To Address" :props="props">
                <router-link
                  :to="'/explorer/address/' + props.row.to_address"
                  style="text-decoration: none"
                  >{{ props.row.to_address }}</router-link
                >
              </q-td>
              <q-td key="Timestamp" :props="props">{{
                props.row.timestamp
              }}</q-td>
            </q-tr>
          </template>
        </q-table>
      </div>
    </q-page-container>
  </q-layout>
</template>

<script>
import axios from 'axios';
import { defineComponent, ref } from 'vue';
import {
  MASTER_NODE_BACKEND_URL,
  resolveTransactionActions,
  TABLE_DEFAULT_ROW_COUNT,
} from '/utils/utils.js';

const tx_cols = [
  {
    name: 'Transaction Number',
    align: 'center',
    label: 'Transaction #',
    field: 'id',
    required: true,
    sortable: true,
  },
  {
    name: 'Transaction Hash',
    align: 'center',
    label: 'Transaction Hash',
    field: 'tx_hash',
    required: true,
    sortable: true,
  },
  {
    name: 'Transaction Action',
    align: 'center',
    label: 'Action',
    field: 'action',
    sortable: true,
  },
  {
    name: 'From Address',
    align: 'center',
    label: 'From Address',
    field: 'from_address',
    sortable: true,
  },

  {
    name: 'To Address',
    align: 'center',
    label: 'To Address',
    field: 'to_address',
    sortable: true,
  },
  {
    name: 'Timestamp',
    align: 'center',
    label: 'Timestamp',
    field: 'timestamp',
    sortable: true,
  },
];

export default defineComponent({
  name: 'ExplorerTransaction',
  components: {},
  data() {
    return {
      txs_loading_state: ref(true),
      first_instance: ref(true),
    };
  },
  setup() {
    return {
      tx_cols,
      tx_rows: ref([]),
      default_tx_rows: ref(TABLE_DEFAULT_ROW_COUNT),
    };
  },
  mounted() {
    this.getTransactions();
  },
  methods: {
    getTransactions() {
      this.txs_loading_state = true;
      axios
        .get(`${MASTER_NODE_BACKEND_URL}/explorer/transactions`)
        .then((response) => {
          // * Assign from the tmeporary variable to modify transaction actions.
          let resolved_txs = [];
          let tx_count = 1;

          // ! Resolve transaction actions to understandable context.
          for (let fetched_tx of response.data) {
            fetched_tx.action = resolveTransactionActions(fetched_tx.action);
            fetched_tx.id = tx_count;

            tx_count += 1;
            resolved_txs.push(fetched_tx);
          }

          // ! Assign then reverse it.
          this.tx_rows = resolved_txs;
          this.tx_rows.reverse();

          this.txs_loading_state = false;

          if (!this.first_instance)
            this.$q.notify({
              color: 'green',
              position: 'top',
              message: 'Transactions has been updated.',
              timeout: 5000,
              progress: true,
              icon: 'mdi-account-check',
            });
          this.first_instance = false;
        })
        .catch((e) => {
          this.$q.notify({
            color: 'red',
            position: 'top',
            message: `Failed to fetch transactions from the server. Please try again later. Reason: ${e.message}`,
            timeout: 5000,
            progress: true,
            icon: 'mdi-cancel',
          });

          this.txs_loading_state = false;
        });
    },
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
}

h2 {
  font-size: 2.5em;
  font-weight: 500;
  text-align: center;
  margin-bottom: 1%;
}

h4 {
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

  margin-left: 5%;
}

.webtitle {
  margin-left: 1%;
}

.logo {
  margin-right: 1.5%;
  margin-bottom: 0.5%;
  margin-top: 0.5%;
  margin-left: 0.5%;
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
  font-weight: 500;
  margin: 0.5%;
  margin-left: 4%;
}
</style>
