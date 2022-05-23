<template>
  <q-layout view="hHh lpR lFf">
    <q-page-container>
      <div class="first-header">
        <q-btn
          color="secondary"
          label="Go back"
          rounded
          icon="arrow_back"
          to="/explorer/addresses"
        />
      </div>
      <div class="second-header wrap-content">

        <div>
          <h3 style="line-height: initial;">{{ user_address }}</h3>
          <p style="line-height: initial;">
          <div v-if="association_address">
            Association Context: {{ association_address }} |
            <strong>{{ association_context }}</strong>
          </div>
          <div v-else>
            No Association.
          </div>
          </p>
        </div>
      </div>

      <div>
        <q-card class="my-card wrap-content">
          <q-linear-progress
            v-if="associated_tx_loading_state"
            query
            color="secondary"
            class="q-mt-sm"
          />
          <q-card-section class="details">
            <p>User Type: {{ user_type }}</p>
            <p v-if="tx_bindings">Transaction Bindings: {{ tx_bindings }}</p>
            <p v-if="negotiations">Consensus Negotiations: {{ negotiations }}</p>
            <p v-if="description">Description: {{ description }}</p>
          </q-card-section>
        </q-card>
      </div>

      <div class="q-pa-md table">
        <q-table
          :rows="tx_rows"
          :columns="tx_cols"
          :loading="associated_tx_loading_state"
          title="Associated Transactions"
          row-key="name"
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
import axios from 'axios';
import { useQuasar } from 'quasar';
import { defineComponent, ref } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import {
  MASTER_NODE_BACKEND_URL,
  resolveTransactionActions,
} from '/utils/utils.js';

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
  name: 'ExplorerAccountDetails',
  components: {},
  data() {
    return {
      tx_rows: ref([]),
      associated_tx_loading_state: ref(true),
      user_name: ref('—'),
      user_address: ref('—'),
      association_context: ref('—'),
      association_address: ref('—'),
      description: ref('—'),
      negotiations: ref('—'),
      tx_bindings: ref('—'),
      user_type: ref('—'),
    };
  },
  setup() {
    const $q = useQuasar();
    const $route = useRoute();
    const $router = useRouter();

    return {
      $q,
      $route,
      $router,
      tx_cols,
    };
  },
  methods: {
    getAddressContext() {
      this.associated_tx_loading_state = true;
      axios
        .get(
          `${MASTER_NODE_BACKEND_URL}/explorer/address/${this.$route.params.uuid}`
        )
        .then((response) => {
          // * Assign context from the variables.
          this.user_address = response.data.uuid;
          this.association_address = response.data.association_uuid;
          this.user_type = response.data.entity_type;
          this.tx_bindings = response.data.tx_bindings_count
          this.negotiations = response.data.negotiations_count
          this.description = response.data.description
          this.association_context = response.data.association_name

          // * Resolve context for the transaction.
          // * Assign from the tmeporary variable to modify transaction actions.
          let resolved_txs = [];
          let tx_count = 1;

          // ! Resolve transaction actions to understandable context.
          for (let fetched_tx of response.data.related_txs) {
            fetched_tx.action = resolveTransactionActions(fetched_tx.action);
            fetched_tx.id = tx_count;

            tx_count += 1;
            resolved_txs.push(fetched_tx);
          }

          // ! Assign then reverse.
          this.tx_rows = resolved_txs;
          this.tx_rows.reverse()

          this.associated_tx_loading_state = false;
        })
        .catch((e) => {
          if (e.request.status === 404) {
            this.$q.notify({
              color: 'red',
              position: 'top',
              message: 'Address not found.',
              timeout: 5000,
              progress: true,
              icon: 'mdi-cancel',
            });
            void this.$router.push({ path: '/explorer/addresses' });
          } else {
            this.$q.notify({
              color: 'red',
              position: 'top',
              message: `Failed to fetch block context from the chain, please try again later. Reason: ${e.message}`,
              timeout: 5000,
              progress: true,
              icon: 'mdi-cancel',
            });

            this.associated_tx_loading_state = false;
          }
        });
    },
  },
  mounted() {
    this.getAddressContext();
  },
});
</script>

<style scoped>
h5 {

  font-weight: 500;
  margin: 0.5%;
  margin-left: 4%;
}

h3 {

  font-weight: 500;
  margin-top: 7%;
  line-height: 25px;
}

p {

  font-size: 1.5em;
}

.usericon {
  font-size: 200px;
}

.user {

  font-size: 1.5em;
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

.first-header {
  display: grid;
  margin: 3%;
  margin-top: 1%;
  width: 10%
}

.second-header {
  margin: 3%;
  margin-top: 1%;
  margin-left: 4%;
}

.wrap-content {
  inline-size: auto;
  overflow-wrap: break-word;
}

@media (max-width: 90em) {
  .usericon {
    font-size: 150px;
  }

  .user {

    font-size: 1.5em;
    font-weight: 600;
    line-height: 0px;
  }

  h3 {

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

    font-size: 1em;
    font-weight: 600;
    line-height: 0px;
  }

  h3 {
    font-size: 1.5em;

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

    font-size: 1em;
  }

  .my-card {
    margin-left: 6%;
    margin-right: 6%;
    margin-bottom: 2%;
  }
}
</style>
