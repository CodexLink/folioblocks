<template>
  <q-layout view="hHh lpR lFf">
    <body>
      <div class="header">
        <q-card
          class="profile"
          style="
            background-image: url(https://cdn.quasar.dev/img/parallax2.jpg);
            object-fit: cover;
            -webkit-filter: brightness(95%);
            filter: brightness(95%);
          "
        >
          <q-card-section>
            <h2 class="text-white">Hello {{ first_name }} {{ last_name }}!</h2>
            <h4 class="alias text-white">
              <strong>{{ user_role }}</strong>
            </h4>
            <p class="alias text-white">
              Identified as <strong>{{ user_address }}</strong> or
              <strong>{{ user_name }}</strong>
            </p>
            <div :class="is_org_creator ? 'btn-extended' : 'btn'">
              <q-btn
                v-if="user_role === 'Administrator' || is_org_creator"
                outline
                rounded
                @click="authModal = true"
                color="white"
                :label="exclusive_button"
              />
              <q-btn
                v-if="user_role !== 'Administrator'"
                outline
                rounded
                color="white"
                :label="button_left"
                :to="button_left_link"
              />
              <q-btn
                outline
                rounded
                color="white"
                :label="button_right"
                :to="button_right_link"
                :disable="
                  user_role === 'Student Dashboard User' ||
                  user_role === 'Administrator'
                "
              />
            </div>
          </q-card-section>
        </q-card>
      </div>

      <q-dialog v-model="authModal" class="modal">
        <q-card style="width: 100%">
          <q-linear-progress
            v-if="isProcessing"
            rounded
            query
            indeterminate
            color="red"
          />

          <q-card-section>
            <div class="text-h6 text-weight-bold">
              Authentication Code Generation
            </div>
          </q-card-section>

          <q-card-section class="text-justify">
            This modal form <strong>allows you</strong> to send authentication
            code from any of the emails within the specific role. Note that,
            <strong>you cannot alter or delete your entries</strong> once you
            proceed. So please be careful.
          </q-card-section>

          <q-form
            @submit.prevent="submitAuthRequest"
            @validation-error="errorOnSubmit"
            :autofocus="true"
          >
            <div class="row">
              <q-input
                class="double"
                color="secondary"
                outlined
                :disable="isProcessing"
                v-model="auth_email"
                type="email"
                :error="auth_email_invalid"
                @focus="auth_email_invalid = false"
                hint="The email that you want give an authentication code for the registration."
                label="E-Mail"
                :rules="[
                  (val) =>
                    val.length > 0 ||
                    'This is required. Please match this one from the equivalent fields.',
                ]"
              >
                <template v-slot:error>
                  This email may either contain the authentication code or is
                  already been used. Please try again.
                </template>
              </q-input>
              <q-input
                class="double"
                color="secondary"
                outlined
                :disable="isProcessing"
                v-model="auth_confirm_email"
                type="email"
                :error="auth_confirm_email_invalid"
                @focus="auth_confirm_email_invalid = false"
                hint="Match this field from the email field."
                label="Confirm E-Mail"
                :rules="[
                  (val) =>
                    !val ||
                    val == auth_email ||
                    'This is required. Please match this one from the equivalent fields.',
                ]"
              >
                <template v-slot:error>
                  Please match this email from the first email field (<em
                    >left field</em
                  >).
                </template>
              </q-input>
            </div>

            <q-select
              class="data"
              color="secondary"
              style="font-size: unset !important; font-weight: unset !important"
              outlined
              v-model="auth_user_type_chosen"
              :options="auth_user_types"
              :error="auth_user_type_invalid"
              @focus="auth_user_type_invalid = false"
              label="User Type"
              hint="The type of user that this user (from the email) will get upon registration."
              :disable="isProcessing"
            >
              <template v-slot:error>
                Please reselect the user type and try again.
              </template>
            </q-select>

            <q-input
              class="data"
              color="secondary"
              outlined
              type="number"
              style="font-size: unset !important; font-weight: unset !important"
              :disable="isProcessing"
              :error="auth_passcode_invalid"
              @focus="auth_passcode_invalid = false"
              v-model="auth_passcode"
              hint="The passcode that authorize this request. You need QR code and an authenticator app for this."
              label="Passcode"
              :rules="[
                (val) =>
                  val.length == 6 ||
                  'This requires 6-digit passcode. Check your Authenticator App.',
              ]"
            >
              <template v-slot:error>
                Your authentication code is incorrect. Please recheck your
                authenticator app and try again.
              </template>
            </q-input>

            <q-slide-transition>
              <div v-show="qr_expand_info">
                <q-separator />
                <q-card-section>
                  <div class="text-h6 text-weight-bold">
                    Scan the QR Code for Authentication
                  </div>
                </q-card-section>
                <vue-qrcode
                  v-if="user_role === 'Administrator' || is_org_creator"
                  :value="qr_code_context"
                  style="width: 128; height: 128; display: block; margin-left: auto; margin-right: auto; }"
                ></vue-qrcode>
                <q-card-section class="text-justify">
                  Please download any mobile-based authenticator (<strong
                    >like the
                    <a
                      href="https://play.google.com/store/apps/details?id=com.google.android.apps.authenticator2"
                      target="_blank"
                      rel="noopener"
                      >Google Authenticator</a
                    ></strong
                  >) app and scan the QR code. Once scanned, get the 6 digits on
                  the screen and place it on the
                  <strong>Passcode</strong> field.
                </q-card-section>
              </div>
            </q-slide-transition>

            <q-card-actions align="right">
              <q-btn
                flat
                v-ripple
                style="color: #ee9102; margin-right: 2%"
                label="Don't have QR?"
                @click="qr_expand_info = !qr_expand_info"
              />
              <q-btn
                flat
                v-ripple
                style="color: #3700b3"
                label="Close Modal"
                @click="authModal = false"
              />
              <q-btn
                v-ripple
                flat
                style="color: #ff0080"
                :disable="
                  isProcessing ||
                  auth_email === null ||
                  auth_email === '' ||
                  auth_confirm_email === null ||
                  auth_confirm_email === '' ||
                  auth_passcode === null ||
                  auth_passcode === '' ||
                  auth_user_type_chosen === null ||
                  auth_user_type_chosen === ''
                "
                label="Send Auth Code"
                type="submit"
              />
            </q-card-actions>
          </q-form>
        </q-card>
      </q-dialog>

      <div class="main">
        <q-card class="blocks">
          <q-linear-progress
            :value="context_right_progress_top"
            rounded
            reverse
            color="red"
          />
          <q-icon
            :name="context_right_top_icon"
            color="red"
            size="6em"
            style="padding-left: 20px; padding-top: 10px"
          />
          <div class="output">
            <p class="data">{{ context_right_top }}</p>
            <p class="title">{{ context_right_top_primary }}</p>
          </div>
        </q-card>

        <q-card class="seminar">
          <q-card-section>
            <div class="text-h6">{{ context_left }}</div>
          </q-card-section>

          <q-card-section class="q-pt-none">
            {{ context_left_primary }}
          </q-card-section>

          <q-card-section class="q-pt-none">
            <q-linear-progress
              :value="context_left_progress_top"
              rounded
              color="red"
              class="q-mt-sm"
            />
            <p class="text-caption" v-if="user_role !== 'Administrator'">
              Log Percentage by Bar
            </p>
            <p class="text-caption" v-if="user_role === 'Administrator'">
              Average Transactions Per Block
            </p>
            <q-linear-progress
              :value="context_left_progress_bottom"
              rounded
              color="secondary"
              class="q-mt-sm"
            />
            <p class="text-caption" v-if="user_role !== 'Administrator'">
              Extra Percentage by Bar
            </p>
            <p class="text-caption" v-if="user_role === 'Administrator'">
              Mappings over Transactions
            </p>
          </q-card-section>
          <q-separator />
          <q-card-section style="transform: translateY(5%)">
            {{ context_left_secondary }}
          </q-card-section>
        </q-card>

        <q-card class="transaction">
          <q-linear-progress
            :value="context_right_progress_bottom"
            rounded
            reverse
            color="secondary"
          />
          <q-icon
            :name="context_right_bottom_icon"
            class="secondary"
            size="6em"
            color="secondary"
            style="padding-left: 20px; padding-top: 12px"
          />
          <div class="output">
            <p class="data">{{ context_right_bottom }}</p>
            <p class="title">
              {{ context_right_bottom_primary }}
            </p>
          </div>
        </q-card>
      </div>
    </body>
  </q-layout>
</template>

<script>
import { defineComponent, ref } from 'vue';
import { useQuasar } from 'quasar';
import axios from 'axios';
import {
  MASTER_NODE_BACKEND_URL,
  QR_CODE_METADATA_AUTH_FOR_ORGS,
} from '/utils/utils.js';
import { useRoute, useRouter } from 'vue-router';
import VueQrcode from '@chenfengyuan/vue-qrcode';

let dashboardOptions = {
  student: {
    buttons: ['View Portfolio', '—'],
    links: ['/portfolio', '#'],
    context: {
      left: {
        title: 'Percentage of Logs vs Extra Info',
        subtitle:
          'Here contains the progress bar-based visualization on how much you have from both the logs and extra info.',
        another:
          'Note that this is the last state since the page has been loaded. Refresh to update this information.',
      },
      right_top: {
        title: 'Total Credentials Received',
        icon: 'mdi-file-star',
      },
      right_bottom: {
        title: 'Portfolio Current Settings',
        icon: 'mdi-file-cog',
      },
    },
  },
  organization: {
    buttons: [
      'Generate Student Users',
      'Refer Credentials',
      'Generate Auth Code',
    ],
    links: ['/org/insert/new', '/org/insert/standby', '#'],
    context: {
      left: {
        title: 'Logs vs Extra Info Dominance',
        subtitle:
          'The following visualization is a percetange-equivalent of logs vs extra information being inserted frequently.',
        another:
          'The progression bar only visualize these provided data in terms of ratio-to-ratio, and thurs an estimation was done per page refresh.',
      },
      right_top: {
        title: 'Total Associations',
        icon: 'mdi-account-group',
      },
      right_bottom: {
        title: 'Total Student Credentials Inserted',
        icon: 'mdi-file-multiple',
      },
    },
  },
  master: {
    buttons: ['Generate Auth Code', '—'],
    context: {
      left: {
        title: 'Node Entity Ratio Information',
        subtitle:
          'Here are some interesting information regarding the consistency of the transactions per block as well as the number of mappings with respect to the number of transactions.',
        another:
          'The progression bar only visualize these provided data in terms of ratio-to-ratio, some of these statistics are built to be a placeholder over an empty dashboard.',
      },
      right_top: {
        title: 'Currently Hashing?',
        icon: 'mdi-pound-box',
      },
      right_bottom: {
        title: 'Currently Sleeping?',
        icon: 'mdi-sleep',
      },
    },
  },
};

export default defineComponent({
  name: 'Dashboard',
  components: { VueQrcode },

  data() {
    return {
      authModal: ref(false),
      auth_passcode: ref(''),
      auth_passcode_invalid: ref(false),

      auth_email: ref(''),
      auth_email_invalid: ref(false),

      auth_confirm_email: ref(''),
      auth_confirm_email_invalid: ref(false),

      auth_user_type_invalid: ref(false),

      button_left: ref('—'),
      button_right: ref('—'),

      button_left_link: ref('#'),
      button_right_link: ref('#'),

      is_org_creator: ref(false),

      first_name: ref('—'),
      last_name: ref('—'),
      user_address: ref('—'),
      user_role: ref('—'),
      user_name: ref('—'),

      context_left: ref('—'),
      context_left_primary: ref('—'),
      context_left_secondary: ref('—'),

      context_right_top: ref('—'),
      context_right_bottom: ref('—'),

      context_right_top_primary: ref('—'),
      context_right_bottom_primary: ref('—'),

      context_right_top_secondary: ref('—'),
      context_right_bottom_secondary: ref('—'),

      context_left_progress_top: ref(0),
      context_left_progress_bottom: ref(0),

      context_right_top_icon: ref(''),
      context_right_bottom_icon: ref(''),

      context_right_progress_top: ref(0),
      context_right_progress_bottom: ref(0),

      isProcessing: ref(false),

      qr_expand_info: ref(false),
      qr_code_context: QR_CODE_METADATA_AUTH_FOR_ORGS,
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
      auth_user_types: [
        { label: 'Organization User', value: 'Organization Dashboard User' },
        { label: 'Archival Miner Node', value: 'Archival Miner Node User' },
      ],
      auth_user_type_chosen: ref({
        label: 'Organization User',
        value: 'Organization Dashboard User',
      }),
    };
  },
  mounted() {
    this.getUserDashboardContext();
  },
  methods: {
    getUserDashboardContext() {
      if (this.$q.localStorage.getItem('role') !== 'Administrator') {
        axios
          .get(`${MASTER_NODE_BACKEND_URL}/dashboard`, {
            headers: {
              'X-Token': this.$q.localStorage.getItem('token'),
            },
          })
          .then((response) => {
            this.first_name = response.data.first_name;
            this.last_name = response.data.last_name;
            this.user_address = response.data.address;
            this.user_role = response.data.role;
            this.user_name = response.data.username;

            if (this.user_role === 'Organization Dashboard User') {
              // * Adjust the context for the organization.
              // - Replace the button context.
              this.button_left = dashboardOptions.organization.buttons[0];
              this.button_left_link = dashboardOptions.organization.links[0];
              this.button_right = dashboardOptions.organization.buttons[1];
              this.button_right_link = dashboardOptions.organization.links[1];

              // ! Enable or disables the generate auth token button to modal.
              if (response.data.is_org_creator) {
                this.is_org_creator = response.data.is_org_creator;
                this.exclusive_button =
                  dashboardOptions.organization.buttons[2];
              }

              // # Replace the cards context.

              // - Update Card #1.
              this.context_right_top_icon =
                dashboardOptions.organization.context.right_top.icon;
              this.context_right_top =
                dashboardOptions.organization.context.right_top.title;
              this.context_right_top_primary = `Currently, there was ${response.data.reports.total_associated} out of ${response.data.reports.total_users} associated users from your organization.`;
              this.context_right_progress_top =
                response.data.reports.total_associated /
                response.data.reports.total_users;

              // - Update Card #2.
              this.context_left =
                dashboardOptions.organization.context.left.title;
              this.context_left_primary =
                dashboardOptions.organization.context.left.subtitle;
              this.context_left_secondary =
                dashboardOptions.organization.context.left.another;
              this.context_left_progress_top =
                response.data.reports.total_associated_logs /
                response.data.reports.total_overall_info_outside;
              this.context_left_progress_bottom =
                response.data.reports.total_associated_extra /
                response.data.reports.total_overall_info_outside;

              // - Update Card #3.
              this.context_right_bottom_icon =
                dashboardOptions.organization.context.right_bottom.icon;
              this.context_right_bottom =
                dashboardOptions.organization.context.right_bottom.title;
              this.context_right_bottom_primary = `Your organization was able to insert ${
                response.data.reports.total_associated_logs +
                response.data.reports.total_associated_extra
              } out of ${
                response.data.reports.total_overall_info_outside
              } student credentials.`;
              this.context_right_progress_bottom =
                (response.data.reports.total_associated_logs +
                  response.data.reports.total_associated_extra) /
                response.data.reports.total_overall_info_outside;
            } else {
              // * Adjust the context for the student.
              // - Replace the button context.
              this.button_left = dashboardOptions.student.buttons[0];
              this.button_left_link = dashboardOptions.student.links[0];
              this.button_right = dashboardOptions.student.buttons[1];
              this.button_right_link = dashboardOptions.student.links[1];

              // - Replace the cards context.

              // - Update Card #1.
              this.context_right_top =
                dashboardOptions.student.context.right_top.title;
              this.context_right_top_primary = `You currently have ${
                response.data.reports.logs_associated_count +
                response.data.reports.extra_associated_count
              } out of ${
                response.data.reports.total_txs_overall
              } given credential/s by your organization.`;
              this.context_right_progress_top =
                (response.data.reports.logs_associated_count +
                  response.data.reports.extra_associated_count) /
                response.data.reports.total_txs_overall;
              this.context_right_top_icon =
                dashboardOptions.student.context.right_top.icon;

              // - Update Card #2.
              this.context_left = dashboardOptions.student.context.left.title;
              this.context_left_primary =
                dashboardOptions.student.context.left.subtitle;
              this.context_left_secondary =
                dashboardOptions.student.context.left.another;

              this.context_left_progress_top =
                response.data.reports.logs_associated_count /
                response.data.reports.total_txs_overall;
              this.context_left_progress_bottom =
                response.data.reports.extra_associated_count /
                response.data.reports.total_txs_overall;

              // - Update Card #3.
              this.context_right_bottom =
                dashboardOptions.student.context.right_bottom.title;
              this.context_right_bottom_primary = `Currently '${
                response.data.reports.portfolio.enable_sharing
                  ? 'public'
                  : 'private'
              }', e-mail contact info is currently '${
                response.data.reports.portfolio.expose_email_info
                  ? 'exposed'
                  : 'hidden'
              }, and files were '${
                response.data.reports.portfolio.show_files
                  ? 'viewable'
                  : 'hidden'
              }'.`;
              this.context_right_bottom_icon =
                dashboardOptions.student.context.right_bottom.icon;

              // * Count the number of `true` over `false`.
              let portfolio_truthy_count = 0;
              let portfolio_total_props = 0;

              for (let portfolio_property in response.data.reports.portfolio) {
                if (portfolio_property) portfolio_truthy_count++;
                portfolio_total_props++;
              }

              this.context_right_progress_bottom =
                portfolio_truthy_count / portfolio_total_props;
            }
          })
          .catch((e) => {
            this.$q.notify({
              color: 'red',
              position: 'top',
              message:
                'Failed to parse data from the dashboard. Please try again.',
              timeout: 5000,
              progress: true,
              icon: 'mdi-cancel',
            });
          });
      } else {
        this.first_name = 'Administrator';
        this.last_name = '(Master Node)';
        this.user_address = this.$q.localStorage.getItem('address');
        this.user_role = this.$q.localStorage.getItem('role');
        this.exclusive_button = dashboardOptions.master.buttons[0];

        this.context_left = dashboardOptions.master.context.left.title;
        this.context_left_primary =
          dashboardOptions.master.context.left.subtitle;
        this.context_left_secondary =
          dashboardOptions.master.context.left.another;
        this.context_right_bottom =
          dashboardOptions.master.context.right_bottom.title;
        this.context_right_bottom_icon =
          dashboardOptions.master.context.right_bottom.icon;
        this.context_right_top =
          dashboardOptions.master.context.right_top.title;
        this.context_right_top_icon =
          dashboardOptions.master.context.right_top.icon;

        axios
          .get(`${MASTER_NODE_BACKEND_URL}/node/info`)
          .then((response) => {
            // ! The value 5 is the expected average of the transactions per block.
            this.context_left_progress_top =
              response.data.statistics.total_transactions /
              response.data.statistics.total_blocks /
              5;
            this.context_left_progress_bottom =
              response.data.statistics.total_tx_mappings /
              response.data.statistics.total_addresses /
              100;

            this.context_right_progress_top =
              (response.data.properties.is_hashing ? 100 : 0) / 100;
            this.context_right_progress_bottom =
              (response.data.properties.is_sleeping ? 100 : 0) / 100;

            this.context_right_top_primary = `The node is currently ${
              response.data.properties.is_hashing ? 'hashing' : 'not hashing'
            } as master nodes should only handle transactions.`;

            this.context_right_bottom_primary = `The node is currently ${
              response.data.properties.is_sleeping ? 'sleeping' : 'not sleeping'
            } as it only give consensus cooldown timer.`;
          })
          .catch((e) => {
            const responseDetail =
              e.response.data === undefined
                ? `${e.message}. Server may be unvailable. Please try again later.`
                : e.response.data.detail;

            this.$q.notify({
              color: 'negative',
              position: 'top',
              message: `There was an error when requesting data to the node. | Info: ${responseDetail}`,
              timeout: 5000,
              progress: true,
              icon: 'report_problem',
            });
          });
      }
    },
    submitAuthRequest() {
      this.isProcessing = true;

      // ! Clear fields.
      this.auth_email_invalid = false;
      this.auth_confirm_email_invalid = false;
      this.auth_user_type_invalid = false;
      this.auth_passcode_invalid = false;

      if (this.auth_email !== this.auth_confirm_email) {
        this.auth_email_invalid = true;
        this.auth_confirm_email_invalid = true;
        this.auth_user_type_invalid = false;
        this.auth_passcode_invalid = false;

        this.$q.notify({
          color: 'negative',
          position: 'top',
          message: 'Please match the email addresses and try again.',
          timeout: 5000,
          progress: true,
          icon: 'report_problem',
        });

        this.isProcessing = false;
        return;
      }

      axios
        .post(
          `${MASTER_NODE_BACKEND_URL}/admin/generate_auth`,
          {
            email: this.auth_email,
            role: this.auth_user_type_chosen.value,
          },
          {
            headers: {
              'X-Token': this.$q.localStorage.getItem('token'),
              'X-Passcode': this.auth_passcode,
            },
          }
        )
        .then((_response) => {
          this.$q.notify({
            color: 'green',
            position: 'top',
            message:
              'Authentication code has been sent to the email! Advise the user regarding email notification.',
            timeout: 5000,
            progress: true,
            icon: 'mdi-account-check',
          });

          this.auth_email = null;
          this.auth_user_type_chosen = this.auth_user_types[0].value;
          this.auth_confirm_email = null;
          this.auth_passcode = null;
          this.isProcessing = false;
        })
        .catch((e) => {
          const responseDetail =
            e.response.data === undefined
              ? `${e.message}. Server may be unvailable. Please try again later.`
              : e.response.data.detail;

          this.$q.notify({
            color: 'negative',
            position: 'top',
            message: `There was an error when requesting a new auth code. | Info: ${responseDetail}`,
            timeout: 5000,
            progress: true,
            icon: 'report_problem',
          });

          if (
            responseDetail.includes('Role not allowed!') ||
            responseDetail.includes(
              'Requesting an authentication code through this role'
            )
          ) {
            this.auth_email_invalid = false;
            this.auth_confirm_email_invalid = false;
            this.auth_user_type_invalid = true;
            this.auth_passcode_invalid = false;
          } else if (
            responseDetail.includes(
              'The email associated from this request already has an authentication code!'
            ) ||
            responseDetail.includes(
              'Cannot provide anymore authentication token to the requested user.'
            ) ||
            responseDetail.includes(
              'Cannot create authentication code due to the user already existing from the system'
            )
          ) {
            this.auth_email_invalid = true;
            this.auth_confirm_email_invalid = false;
            this.auth_user_type_invalid = false;
            this.auth_passcode_invalid = false;
          } else if (responseDetail.includes('Invalid TOTP passcode.')) {
            this.auth_email_invalid = false;
            this.auth_confirm_email_invalid = false;
            this.auth_user_type_invalid = false;
            this.auth_passcode_invalid = true;
          }
          this.isProcessing = false;
        });
    },
    errorOnSubmit() {
      this.$q.notify({
        color: 'negative',
        position: 'top',
        message:
          'There was an error from one of the fields. Please check and try again.',
        timeout: 5000,
        progress: true,
        icon: 'report_problem',
      });
    },
  },
});
</script>

<style scoped>
.main {
  display: grid;
  margin: 6%;
  margin-bottom: 0%;
  padding-bottom: 3%;

  gap: 1.5rem;
  grid-template-columns: repeat(2, 1fr);
}

.data {
  margin: 3%;
}

.double {
  width: 44%;
  margin: 3%;
}

.header {
  display: grid;
  margin: 6%;
  margin-top: 3%;
  gap: 1.5rem;
}

.status {
  display: grid;
  grid-template-columns: 20% 30% 20% 30%;
  background-color: #54d6ff;
}

.profile {
  height: 100%;
}

.btn {
  display: grid;
  gap: 1em;
  grid-template-columns: repeat(2, 1fr);
  padding: 1%;
  font-size: 1em;
}

.btn-extended {
  display: grid;
  gap: 1em;
  grid-template-columns: repeat(3, 1fr);
  padding: 1%;
  font-size: 1em;
}

h2 {
  font-size: 2.5em;
  font-weight: 500;
  text-align: center;
  margin-bottom: 1%;
  word-break: break-all;
}

.alias {
  font-size: 1.3em;
  text-align: center;
  margin-bottom: 5%;
}

h4 {
  font-size: 1.8em;
  font-weight: 400;
  line-height: 15px;
}

.dataheader {
  font-size: 2em;

  font-weight: 500;
  line-height: 0px;
}

.icon {
  font-size: 130px;
  margin-left: 25%;
}

img {
  height: 50px;
  width: 50px;
  float: left;
  margin: 5%;
}

.seminar,
.activity {
  grid-row: span 2;
}
.seminar-activity-icon {
  height: 100px;
  width: 100px;
  float: left;
  margin: 5%;
  margin-top: 12%;
}

.dataseminar {
  margin-top: 15%;

  font-weight: 600;
}

.titleseminar {
  font-size: 1.5em;
  font-weight: 500;
}

.output {
  float: right;
  margin-right: 7%;
  margin-top: 4%;
  text-align: right;
}

.data {
  font-size: 1.7em;
  font-weight: 700;
}

.title {
  font-size: 1em;
  font-weight: 500;
}

@media (max-width: 100em) {
  .header {
    display: grid;
    margin: 6%;
    gap: 1.5rem;
    grid-template-columns: repeat(1, 1fr);
  }

  .status {
    display: grid;
    grid-template-columns: 15% 35% 15% 35%;
    background-color: #54d6ff;
  }

  .main {
    display: grid;
    margin: 6%;
    margin-bottom: 0%;
    padding-bottom: 3%;
    gap: 1.5rem;
    grid-template-columns: repeat(1, 1fr);
  }

  .icon {
    font-size: 100px;
    margin-left: 50%;
  }

  h4 {
    font-size: 1em;
    font-weight: 400;
    line-height: 15px;
  }

  p {
    font-size: 1em;
  }
  .dataheader {
    font-size: 1em;

    font-weight: 500;
    line-height: 0px;
  }

  .seminar-activity-icon {
    height: 70px;
    width: 70px;
    float: left;
    margin: 4%;
    margin-top: 5%;
  }

  .dataseminar {
    margin-top: 0%;

    font-weight: 600;
  }

  .titleseminar {
    font-size: 1em;
    font-weight: 500;
  }

  .btn {
    display: grid;
    gap: 1em;
    grid-template-columns: repeat(1, 1fr);
    padding: 1%;
    line-height: 10%;
    font-size: 0.5em;
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
    background-color: #54d6ff;
  }

  .main {
    display: grid;
    margin: 6%;
    margin-bottom: 0%;
    padding-bottom: 3%;
    gap: 1.5rem;
    grid-template-columns: repeat(1, 1fr);
  }

  .icon {
    font-size: 90px;
    margin-left: 1%;
  }

  h4 {
    font-size: 1em;
    font-weight: 400;
    line-height: 15px;
  }

  p {
    font-size: 1em;
  }
  .dataheader {
    font-size: 1em;

    font-weight: 500;
    line-height: 0px;
  }

  .seminar-activity-icon {
    height: 70px;
    width: 70px;
    float: left;
    margin: 4%;
    margin-top: 5%;
  }

  .dataseminar {
    margin-top: 0%;

    font-weight: 600;
  }

  .titleseminar {
    font-size: 1em;
    font-weight: 500;
  }

  .btn {
    display: grid;
    gap: 1em;
    grid-template-columns: repeat(2, 1fr);
    padding: 1%;
    font-size: 0.5em;
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
