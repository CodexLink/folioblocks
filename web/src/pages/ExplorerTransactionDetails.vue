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
          to="/explorer/transactions"
        />
      </div>
      <q-separator color="black" />
      <h5 class="wrap-content">Details of Transaction Hash {{ tx_hash }}</h5>
      <q-separator color="black" />

      <q-card class="my-card wrap-content">
        <q-linear-progress
          v-if="!isLoadingContextFinished"
          query
          color="secondary"
          class="q-mt-sm"
        />
        <q-card-section>
          <div class="text-h6">Transaction Information</div>
          <div class="text-subtitle1">
            Here contains extra information regarding this transaction. Note
            that some transaction contents are not decrypt since it may contain
            some sensitive information.
          </div>
        </q-card-section>

        <q-card-section class="details">
          <div>
            <router-link
              :to="'/explorer/block/' + at_block"
              style="text-decoration: none"
            >
              <p>Block Origin: {{ at_block }}</p>
            </router-link>

            <p>
              Action: <strong>{{ tx_action }}</strong>
            </p>

            <router-link
              :to="'/explorer/address/' + tx_source_address"
              style="text-decoration: none"
            >
              <p>From Address: {{ tx_source_address }}</p>
            </router-link>

            <router-link
              :to="'/explorer/address/' + tx_dest_address"
              style="text-decoration: none"
            >
              <p>To Address: {{ tx_dest_address }}</p>
            </router-link>

            <p>Timestamp: {{ tx_timestamp }}</p>
          </div>
        </q-card-section>
        <q-separator />
        <q-card-section>
          <div class="text-h6">Payload Context</div>
          <div class="text-subtitle1">
            The following transaction contains the following elements.
          </div>
        </q-card-section>
        <q-card-section class="details">
          <p>
            Context Type: <strong>{{ tx_context_type }}</strong
            >, classified as
            <code style="color: red">{{ tx_context_type_classification }}</code>
          </p>
          <p>
            Contents:
            <code class="text-justify" style="background: aliceblue">{{
              tx_literal_context
            }}</code>
          </p>
        </q-card-section>
        <q-separator />
        <q-card-section>
          <div class="text-h6">Transaction Context Signature</div>
          <div class="text-subtitle1">
            For validity, the following fields shows the hash integrity of the
            context, both in its <code style="color: red">encrypted</code> and
            <code style="color: red">raw</code> form. Note that, for the case of
            <code style="color: red">Internal Transaction</code>, you can verify
            the encrypted hash by encrypting the context provided. For the case
            of <code style="color: red">External Transaction</code>, you can
            verify the raw hash by decrypting its context.
          </div>
        </q-card-section>

        <q-card-section class="details">
          <p>
            Raw: <code>{{ tx_context_signature_raw }}</code>
          </p>
          <p>
            Encrypted: <code>{{ tx_context_signature_encrypted }}</code>
          </p>
        </q-card-section>
      </q-card>
    </q-page-container>
  </q-layout>
</template>

<script>
import { defineComponent, ref } from 'vue';
import { useQuasar } from 'quasar';
import axios from 'axios';
import {
  resolveContextType,
  resolvedNodeAPIURL,
  resolveTransactionActions,
} from '/utils/utils.js';
import { useRoute, useRouter } from 'vue-router';

export default defineComponent({
  name: 'ExplorerTransactionDetails',
  components: {},
  setup() {
    const $route = useRoute();
    const $router = useRouter();
    const $q = useQuasar();

    return {};
  },
  data() {
    return {
      at_block: ref('—'),
      isLoadingContextFinished: ref(false),
      tx_hash: ref('—'),
      tx_action: ref('—'),
      tx_source_address: ref('—'),
      tx_dest_address: ref('—'),
      tx_timestamp: ref('—'),
      tx_context_type: ref('—'),
      tx_context_type_classification: ref('—'),
      tx_literal_context: ref('—'),
      tx_context_signature_raw: ref('—'),
      tx_context_signature_encrypted: ref('—'),
    };
  },
  mounted() {
    this.getTransactionContext();
  },
  methods: {
    getTransactionContext() {
      this.isLoadingContextFinished = false;
      axios
        .get(
          `http://${resolvedNodeAPIURL}/explorer/transaction/${this.$route.params.tx_hash}`
        )
        .then((response) => {
          // * Destructure.
          let { identifiedType, resolvedTypeValue } = resolveContextType(
            response.data.transaction.payload
          );

          this.at_block = response.data.from_block;
          this.tx_hash = response.data.transaction.tx_hash;
          this.tx_action = resolveTransactionActions(
            response.data.transaction.action
          );
          this.tx_source_address = response.data.transaction.from_address;
          this.tx_dest_address = response.data.transaction.to_address;
          this.tx_timestamp = response.data.transaction.timestamp;
          this.tx_literal_context = response.data.transaction.payload.context;
          this.tx_context_signature_raw =
            response.data.transaction.signatures.raw;
          this.tx_context_signature_encrypted =
            response.data.transaction.signatures.encrypted;

          // * Bind it from the attribute.
          this.tx_context_type = resolvedTypeValue;
          this.tx_context_type_classification = identifiedType;

          this.isLoadingContextFinished = true;
        })
        .catch((e) => {
          if (e.request.status === 404) {
            this.$q.notify({
              color: 'red',
              position: 'top',
              message: 'Transactions not found.',
              timeout: 5000,
              progress: true,
              icon: 'mdi-cancel',
            });
            void this.$router.push({ path: '/explorer/transactions' });
          } else {
            this.$q.notify({
              color: 'red',
              position: 'top',
              message: `There was an error when fetching from the chain. Please come back and try again later. Reason: ${e.message}`,
              Interval: 10000,
              progress: true,
              icon: 'mdi-cancel',
            });
          }
          this.isLoadingContextFinished = true;
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
  min-width: 30%;
  max-width: 70%;
}

.details {
  font-size: 1.5em;
  padding: 2%;
  padding-left: 4%;
}

.wrap-content {
  inline-size: auto;
  overflow-wrap: break-word;
}
</style>
