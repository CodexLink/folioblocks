<template>
  <q-layout view="hHh lpR lFf">
    <q-page-container>
      <div>
        <h2>Welcome to Folioblocks Credential Receipt Explorer</h2>
      </div>
      <div class="search">
        <q-form @submit.prevent="onSearchSubmit" class="q-gutter-md">
          <q-input
            class="searchbar"
            clearable
            v-model="searchContext"
            debounce="500"
            filled
            placeholder="Paste or type something here."
            hint="Search by address, transaction hash, or even by block number."
          >
            <template v-slot:append>
              <q-icon name="search" />
            </template>
          </q-input>
        </q-form>
      </div>

      <q-card class="header">
        <q-card-section>
          <div class="text-h6">Blockchain Statistics</div>
          <div class="text-subtitle1">
            Some interesting minimal information about the blockchain's current
            state.
          </div>
        </q-card-section>
        <div class="profile status bg-cyan-2">
          <q-avatar class="icon" icon="view_in_ar" />
          <div>
            <h4>Blocks</h4>
            <p class="dataheader">{{ n_blocks }}</p>
          </div>

          <q-avatar class="icon" icon="mdi-sitemap" />
          <div>
            <h4>Transaction Mapping</h4>
            <p class="dataheader">{{ txs_mapping_count }}</p>
          </div>

          <q-avatar class="icon" icon="swap_horiz" />
          <div>
            <h4>Transactions</h4>
            <p class="dataheader">{{ txs_count }}</p>
          </div>

          <q-avatar class="icon" icon="person" />
          <div>
            <h4>Addresses</h4>
            <p class="dataheader">{{ addresses }}</p>
          </div>
        </div>
      </q-card>

      <div class="main">
        <div class="row gridblock">
          <h5>Latest Transactions</h5>
          <q-btn
            class="viewall"
            rounded
            color="accent"
            text-color="black"
            label="View All"
            to="/explorer/transactions"
          />
        </div>
        <div class="row">
          <h5>Latest Blocks</h5>
          <q-btn
            class="viewall"
            rounded
            color="accent"
            text-color="black"
            label="View All"
            to="/explorer/blocks"
          />
        </div>

        <q-table
          :rows="transaction_rows"
          :columns="transaction_cols"
          row-key="name"
          :loading="txs_loading_state"
          :hide-pagination="true"
          no-data-label="Failed to fetch from the chain or theres no transactions from chain to render."
        >
          <template v-slot:body="props">
            <q-tr :props="props">
              <q-td key="Transaction Hash" :props="props">
                <router-link
                  :to="'/explorer/transaction/' + props.row.tx_hash"
                  style="text-decoration: none"
                  >{{ props.row.tx_hash }}</router-link
                ></q-td
              >
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

        <q-table
          :rows="block_rows"
          :columns="block_cols"
          row-key="name"
          :loading="blocks_loading_state"
          :hide-pagination="true"
          no-data-label="Failed to fetch from the chain or theres no blocks from chain to render."
        >
          <template v-slot:body="props">
            <q-tr :props="props">
              <q-td key="Block ID" :props="props">
                <router-link
                  :to="'/explorer/block/' + props.row.id"
                  style="text-decoration: none"
                  >{{ props.row.id }}</router-link
                >
              </q-td>
              <q-td key="Transaction Count" :props="props">{{
                props.row.tx_count
              }}</q-td>

              <q-td key="Validator" :props="props">
                <router-link
                  :to="'/explorer/address/' + props.row.validator"
                  style="text-decoration: none"
                  >{{ props.row.validator }}</router-link
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
import { useRouter } from 'vue-router';
import { MASTER_NODE_BACKEND_URL } from '/utils/utils.js';

const block_cols = [
  {
    name: 'Block ID',
    align: 'center',
    label: 'Block ID',
    field: 'id',
    sortable: true,
  },
  {
    name: 'Transaction Count',
    align: 'center',
    label: 'Transaction Count',
    field: 'tx_count',
    sortable: true,
  },
  {
    name: 'Validator',
    align: 'center',
    label: 'Validator',
    field: 'validator',
  },
  {
    name: 'Timestamp',
    align: 'center',
    label: 'Timestamp',
    field: 'timestamp',
    sortable: true,
  },
];

const transaction_cols = [
  {
    name: 'Transaction Hash',
    align: 'center',
    label: 'Transaction Hash',
    field: 'tx_hash',
    style: 'width: 50px',
  },
  {
    name: 'To Address',
    align: 'center',
    label: 'To Address',
    field: 'to_address',
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
  name: 'ExplorerDashboard',
  data() {
    return {
      n_blocks: ref('—'),
      txs_mapping_count: ref('—'),
      txs_count: ref('—'),
      addresses: ref('—'),
      txs_loading_state: ref(true),
      blocks_loading_state: ref(true),
      searchContext: ref(''),
    };
  },

  setup() {
    const $router = useRouter();

    return {
      $router,
      transaction_cols,
      transaction_rows: ref([]),
      block_cols,
      block_rows: ref([]),
    };
  },
  mounted() {
    this.txs_loading_state = true;
    this.blocks_loading_state = true;

    this.updateDashboard();
  },
  methods: {
    updateDashboard() {
      axios
        .get(`${MASTER_NODE_BACKEND_URL}/explorer/chain`)
        .then((response) => {
          this.n_blocks = response.data.node_info.total_blocks;
          this.txs_mapping_count = response.data.node_info.total_tx_mappings;
          this.txs_count = response.data.node_info.total_transactions;
          this.addresses = response.data.node_info.total_addresses;
          this.transaction_rows = response.data.transactions;
          this.block_rows = response.data.blocks;

          this.txs_loading_state = false;
          this.blocks_loading_state = false;
        })
        .catch((e) => {
          this.$q.notify({
            color: 'red',
            position: 'top',
            message: `There was an error when fetching from the chain. Please come back and try again later. Reason: ${e.message}`,
            Interval: 5000,
            progress: true,
            icon: 'mdi-cancel',
          });

          this.txs_loading_state = false;
          this.blocks_loading_state = false;
        });
    },
    onSearchSubmit() {
      // ! Directing to address.
      if (
        this.searchContext.startsWith('fl:') &&
        this.searchContext.length === 35
      ) {
        void this.$router.push({
          path: `/explorer/address/${this.searchContext}`,
        });
      }
      // ! Directing to transactions.
      else if (this.searchContext.length === 64) {
        void this.$router.push({
          path: `/explorer/transaction/${this.searchContext}`,
        });
      }
      // ! Directing to block.
      else if (Number.isInteger(parseInt(this.searchContext))) {
        void this.$router.push({
          path: `/explorer/block/${this.searchContext}`,
        });
      } else {
        this.$q.notify({
          color: 'red',
          position: 'top',
          message:
            'Failed to parse the context given, are you sure this is correct?',
          timeout: 5000,
          progress: true,
          icon: 'mdi-cancel',
        });
      }
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
  margin: 2% 25%;
  margin-bottom: 5%;
  gap: 1.5rem;
}

.profile {
  height: 100%;
}

.alias {
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
  grid-template-columns: 25% 25% 25% 25%;
}
.icon {
  font-size: 150px;
  margin-left: 20%;
}

.dataheader {
  font-size: 2em;

  font-weight: 500;
  line-height: 0px;
  margin-left: 10%;
}

h4 {
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
  margin-bottom: 0%;
  padding-bottom: 3%;
  margin-top: 2%;
  margin-left: 2%;
  margin-right: 2%;
}

h5 {
  font-weight: 500;
  margin: 0%;
}

h2 {
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
    font-size: 100px;
    margin-left: 40%;
  }

  h4 {
    font-size: 0.8em;
    font-weight: 400;
    line-height: 30px;
    margin-left: 0%;
  }

  p {
    font-size: 1em;
  }
  .dataheader {
    font-size: 1em;

    font-weight: 500;
    line-height: 0px;
    margin-left: 0%;
  }
  h5 {
    font-size: 1.3em;

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
    font-size: 2em;
    font-weight: 500;
    text-align: center;
    margin-bottom: 1%;
    overflow: hidden;
  }

  .alias {
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
    font-size: 0.8em;
    font-weight: 400;
    line-height: 15px;
    margin-left: 0%;
  }

  p {
    font-size: 1em;
  }
  .dataheader {
    font-size: 1em;

    font-weight: 500;
    line-height: 0px;
    margin-left: 0%;
  }
  h5 {
    font-size: 1.3em;

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
    font-size: 2em;
    font-weight: 500;
    text-align: center;
    margin-bottom: 1%;
  }

  .alias {
    font-size: 1em;
    text-align: center;
    margin-bottom: 5%;
  }
}
</style>
