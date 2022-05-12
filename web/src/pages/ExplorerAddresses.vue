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
      <h5>Addresses</h5>
      <q-separator color="black" />

      <div class="q-pa-md">
        <q-table
          :rows="addresses_rows"
          :columns="addresses_cols"
          row-key="id"
          :loading="addresses_loading_state"
          :rows-per-page-options="[default_addresses_rows]"
          no-data-label="Failed to fetch from the chain or theres no addresses from chain to render."
        >
          <template v-slot:top-right>
            <q-btn
              color="green"
              icon-right="refresh"
              label="Refresh"
              no-caps
              @click="getAddresses"
            />
          </template>
          <template v-slot:body="props">
            <q-tr :props="props">
              <q-td key="ID" :props="props">{{ props.row.id }}</q-td>

              <q-td key="User Address" :props="props">
                <router-link
                  :to="'/explorer/address/' + props.row.uuid"
                  style="text-decoration: none"
                  >{{ props.row.uuid }}</router-link
                ></q-td
              >

              <q-td key="Association Address" :props="props">
                <div class="disabled">
                  {{ props.row.association_uuid }}
                  <q-tooltip
                    v-if="props.row.association_uuid !== '<No Association>'"
                    class="bg-purple text-subtitle2"
                    max-width="30%"
                  >
                    Association addresses cannot be viewed in detail due to its
                    minimal information. Please check the user addresses context
                    to find more information about this association /
                    organization.
                  </q-tooltip>
                </div>
              </q-td>

              <q-td key="User Type" :props="props">{{
                props.row.entity_type
              }}</q-td>

              <q-td key="Transaction Map Bindings" :props="props">{{
                props.row.tx_bindings_count
              }}</q-td>

              <q-td key="Consensus Negotiations" :props="props">{{
                props.row.negotiations_count
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

const addresses_cols = [
  {
    name: 'ID',
    align: 'center',
    label: 'ID',
    field: 'id',
    sortable: true,
  },
  {
    name: 'User Address',
    align: 'center',
    label: 'User Address',
    field: 'uuid',
    sortable: true,
  },
  {
    name: 'Association Address',
    align: 'center',
    label: 'Association Address',
    field: 'association_uuid',
    sortable: true,
  },
  {
    name: 'User Type',
    align: 'center',
    label: 'User Type',
    field: 'entity_type',
    sortable: true,
  },
  {
    name: 'Transaction Map Bindings',
    align: 'center',
    label: 'Transaction Map Bindings',
    field: 'tx_bindings_count',
    sortable: true,
  },
  {
    name: 'Consensus Negotiations',
    align: 'center',
    label: 'Consensus Negotiations',
    field: 'negotiations_count',
  },
];

export default defineComponent({
  name: 'ExplorerTransaction',
  components: {},

  data() {
    return {
      addresses_loading_state: ref(false),
      first_instance: ref(true),
    };
  },

  setup() {
    return {
      addresses_cols,
      addresses_rows: ref([]),
      default_addresses_rows: ref(TABLE_DEFAULT_ROW_COUNT),
    };
  },
  mounted() {
    this.getAddresses();
  },
  methods: {
    getAddresses() {
      this.addresses_loading_state = true;
      axios
        .get(`https://${MASTER_NODE_BACKEND_URL}/explorer/addresses`)
        .then((response) => {
          // * Define the temporary container.
          let resolved_addresses = [];
          let nth_address = 1;

          for (let address_context of response.data) {
            address_context.association_uuid =
              address_context.association_uuid === null
                ? '<No Association>'
                : address_context.association_uuid;

            // * Increment index.
            address_context.id = nth_address;
            nth_address += 1;

            resolved_addresses.push(address_context);
          }

          this.addresses_rows = resolved_addresses;
          this.addresses_loading_state = false;

          if (!this.first_instance)
            this.$q.notify({
              color: 'green',
              position: 'top',
              message: 'Addresses has been updated.',
              timeout: 10000,
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
            timeout: 10000,
            progress: true,
            icon: 'mdi-cancel',
          });

          this.addresses_loading_state = false;
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
</style>
