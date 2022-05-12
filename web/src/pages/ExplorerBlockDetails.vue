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
          to="/explorer/blocks"
        />
      </div>
      <q-separator color="black" />
      <h5>Block #{{ nth_block }}</h5>
      <q-separator color="black" />

      <q-card class="my-card wrapped-content">
        <q-linear-progress
          v-if="associated_tx_loading_state"
          query
          color="secondary"
          class="q-mt-sm"
        />
        <q-card-section>
          <div class="text-h6">Block Information</div>
          <div class="text-subtitle1">
            Here contains extra information regarding this block.
          </div>
        </q-card-section>

        <q-card-section class="details">
          <div>
            <p>
              Hash Block: <strong>{{ hash_block_ref }}</strong>
            </p>
            <p>Prev Hash Block: {{ prev_hash_block_ref }}</p>
            <p>Nonce: {{ calc_nonce }}</p>
            <p>Content Bytes: {{ block_content_size }}</p>
            <router-link
              :to="'/explorer/address/' + validator"
              style="text-decoration: none"
            >
              <p>
                Validator:
                <strong>{{ validator }}</strong>
              </p>
            </router-link>
            <p>Timestamp: {{ timestamp }}</p>
          </div>
        </q-card-section>
      </q-card>

      <div class="q-pa-md my-card">
        <q-table
          :rows="tx_rows"
          :columns="tx_cols"
          row-key="id"
          :loading="associated_tx_loading_state"
          :rows-per-page-options="[default_tx_rows]"
          title="Associated Transactions"
          no-data-label="No associated transactions from this block, or failed to fetch data from the chain."
        >
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
import { defineComponent, ref } from 'vue';
import { useQuasar } from 'quasar';
import axios from 'axios';
import {
  MASTER_NODE_BACKEND_URL,
  resolveTransactionActions,
  TABLE_DEFAULT_ROW_COUNT,
} from '/utils/utils.js';
import { useRoute, useRouter } from 'vue-router';

const tx_cols = [
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
  name: 'ExplorerBlockDetails',
  components: {},
  data() {
    return {
      nth_block: ref('—'),
      block_content_size: ref('—'),
      hash_block_ref: ref('—'),
      prev_hash_block_ref: ref('—'),
      calc_nonce: ref('—'),
      validator: ref('—'),
      timestamp: ref('—'),
      associated_tx_loading_state: ref(true),
      default_tx_rows: ref(TABLE_DEFAULT_ROW_COUNT),
    };
  },
  setup() {
    const $route = useRoute();
    const $router = useRouter();
    return {
      tx_cols,
      tx_rows: ref([]),
    };
  },
  mounted() {
    this.getBlockContext();
  },
  methods: {
    getBlockContext() {
      this.associated_tx_loading_state = true;
      axios
        .get(
          `https://${MASTER_NODE_BACKEND_URL}/explorer/block/${this.$route.params.id}`
        )
        .then((response) => {
          // * Assign context from the block information.
          this.nth_block = response.data.id;
          this.block_content_size = response.data.content_bytes_size;
          this.hash_block_ref = response.data.hash_block;
          this.prev_hash_block_ref = response.data.prev_hash_block;
          this.calc_nonce = response.data.contents.nonce;
          this.validator = response.data.contents.validator;
          this.timestamp = response.data.contents.timestamp;

          // * Assign from the tmeporary variable to modify transaction actions.
          let resolved_txs = [];

          // ! Resolve transaction actions to understandable context.
          for (let fetched_tx of response.data.contents.transactions) {
            fetched_tx.action = resolveTransactionActions(fetched_tx.action);

            resolved_txs.push(fetched_tx);
          }

          this.tx_rows = resolved_txs.reverse();
          this.associated_tx_loading_state = false;
        })
        .catch((e) => {
          if (e.request.status === 404) {
            this.$q.notify({
              color: 'red',
              position: 'top',
              message: 'Block not found.',
              timeout: 5000,
              progress: true,
              icon: 'mdi-cancel',
            });
            void this.$router.push({ path: '/explorer/blocks' });
          } else {
            this.$q.notify({
              color: 'red',
              position: 'top',
              message: `Failed to fetch block context from the chain, please try again later. Reason: ${e.message}`,
              timeout: 10000,
              progress: true,
              icon: 'mdi-cancel',
            });

            this.associated_tx_loading_state = false;
          }
        });
    },
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
  width: fit-content;
}

.details {
  font-size: 1.5em;
  padding: 2%;
}

.wrap-content {
  inline-size: auto;
  overflow-wrap: break-word;
}

@media (max-width: 60em) {
  .details {
    font-size: 1.5em;
    padding: 6%;
  }
}
</style>
