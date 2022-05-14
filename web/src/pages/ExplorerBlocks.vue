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
      <h5>Blocks</h5>
      <q-separator color="black" />

      <div class="q-pa-md">
        <q-table
          :rows="block_rows"
          :columns="block_cols"
          row-key="id"
          :loading="block_loading_state"
          :rows-per-page-options="[default_block_rows]"
          no-data-label="Failed to fetch from the chain or theres no blocks from chain to render."
        >
          <template v-slot:top-right>
            <q-btn
              color="green"
              icon-right="refresh"
              label="Refresh"
              no-caps
              @click="getBlocks"
            />
          </template>
          <template v-slot:body="props">
            <q-tr :props="props">
              <q-td key="Block ID" :props="props">
                <router-link
                  :to="'/explorer/block/' + props.row.id"
                  style="text-decoration: none"
                  >{{ props.row.id }}</router-link
                ></q-td
              >

              <q-td key="Block Content Byte Size" :props="props">{{
                props.row.content_bytes_size
              }}</q-td>

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
import { defineComponent, ref } from 'vue';
import { useQuasar } from 'quasar';
import axios from 'axios';
import {
  MASTER_NODE_BACKEND_URL,
  resolveTransactionActions,
  TABLE_DEFAULT_ROW_COUNT,
} from '/utils/utils.js';
import { useRoute, useRouter } from 'vue-router';

const block_cols = [
  {
    name: 'Block ID',
    align: 'center',
    label: 'Block ID',
    field: 'id',
    sortable: true,
  },
  {
    name: 'Block Content Byte Size',
    align: 'center',
    label: 'Block Content Byte Size',
    field: 'content_bytes_size',
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

export default defineComponent({
  name: 'ExplorerTransaction',
  components: {},

  data() {
    return {
      block_loading_state: ref(false),
      first_instance: ref(true),
    };
  },

  setup() {
    return {
      block_cols,
      block_rows: ref([]),
      default_block_rows: ref(TABLE_DEFAULT_ROW_COUNT),
    };
  },
  mounted() {
    this.getBlocks();
  },
  methods: {
    getBlocks() {
      this.block_loading_state = true;
      axios
        .get(`${MASTER_NODE_BACKEND_URL}/explorer/blocks`)
        .then((response) => {
          // * Assign from the tmeporary variable to modify transaction actions.
          let resolved_blocks = [];

          // ! Resolve transaction actions to understandable context.
          for (let fetched_block of response.data) {
            fetched_block.action = resolveTransactionActions(
              fetched_block.action
            );

            resolved_blocks.push(fetched_block);
          }

          this.block_rows = resolved_blocks;
          this.block_loading_state = false;

          if (!this.first_instance)
            this.$q.notify({
              color: 'green',
              position: 'top',
              message: 'Blocks has been updated.',
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

          this.block_loading_state = false;
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
