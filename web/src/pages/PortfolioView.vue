<template>
  <div class="header text-h6">
    <p class="q-pt-md">
      <span class="text-weight-bold q-ma-sm q-mb-sm q-pt-md q-ml-lg">
        Address:
      </span>
      <router-link
        :to="'/explorer/address/' + portfolio_user_address"
        style="text-decoration: none"
      >
        {{ portfolio_user_address }}
      </router-link>

      <span class="text-weight-bold q-ma-sm q-mb-sm q-ml-xl">
        Institution Reference:
      </span>
      {{ portfolio_user_association }}
    </p>
    <p>
      <span class="text-weight-bold q-ma-sm q-mb-sm q-ml-lg">
        Email Contact:</span
      >{{ portfolio_user_email_contact }}
    </p>
    <p>
      <span class="text-weight-bold q-ma-sm q-mb-sm q-ml-lg"> Program:</span>
      {{ portfolio_user_program }}
      <span class="text-weight-bold q-ma-sm q-mb-sm q-ml-lg">
        Role Preference in Field:</span
      >
      {{ portfolio_user_preferred_role }}
    </p>
    <p></p>
    <p>
      <span class="text-weight-bold q-ma-sm q-ml-lg">
        General Description:</span
      >
      {{ portfolio_user_description }}
    </p>
    <p>
      <span class="text-weight-bold q-ma-sm q-mb-sm q-ml-lg"> Skillset: </span>
      {{ portfolio_user_personal_skills }}
    </p>
  </div>

  <div class="row">
    <div class="logs">
      <q-linear-progress
        v-if="portfolio_log_info_rendering_state"
        query
        color="red"
        class="q-mt-sm"
      />
      <q-card-section style="margin-bottom: 0.5%">
        <div class="text-h6">Logs</div>
        <div class="text-subtitle1">
          A set of contentful information that can be known as
          <strong>logs</strong>, which should contains supporting context with
          documents (if given). The following are associated logs to you. Click
          them to get more infomration regarding this log.
        </div>
      </q-card-section>
      <q-scroll-area style="height: 100%; max-width: 100%">
        <q-item
          v-for="log in portfolio_log_container"
          :key="log.id"
          class="logdata"
        >
          <q-item-section class="text-h6">
            <q-item-label
              ><span class="text-weight-bold q-mb-sm">{{
                log.context.name
              }}</span>
              |

              <span class="text-weight-bold q-ma-md q-mb-sm"> Role: </span
              >{{ log.context.role }}
            </q-item-label>

            <q-item-label class="q-ml-md" style="margin-top: 2%">
              <span class="text-weight-bold text-justify q-mb-sm q-mr-md">
                Description: </span
              >{{ log.context.description }}</q-item-label
            >
            <q-item-label style="margin-top: 2%">
              <span class="text-weight-bold q-ma-md q-mb-sm"> By:</span>
              <router-link
                :to="'/explorer/address/' + log.context.validated_by"
                style="text-decoration: none"
                >{{ log.context.validated_by }}</router-link
              >
            </q-item-label>
            <q-item-label class="q-ml-md" style="margin-top: 2%">
              <span class="text-weight-bold text-justify q-mb-sm q-mr-md">
                Duration Start:</span
              >{{ log.context.duration_start }}
              <span v-if="log.context.duration_end">|</span>
              <span
                class="text-weight-bold text-justify q-mb-sm q-mr-md"
                v-if="log.context.duration_end"
              >
                Duration End:</span
              >{{ log.context.duration_end }}
              <q-card-actions align="right">
                <q-btn
                  outline
                  right
                  color="black"
                  label="View More"
                  class="q-mt-md"
                  @click="getLogInfo(log.id)"
                />
              </q-card-actions>
            </q-item-label>
          </q-item-section>
        </q-item>
      </q-scroll-area>
    </div>

    <div class="logs">
      <q-linear-progress
        v-if="portfolio_extra_info_rendering_state"
        query
        color="red"
        class="q-mt-sm"
      />

      <q-card-section style="margin-bottom: 0.5%">
        <div class="text-h6">Extras</div>
        <div class="text-subtitle1">
          A set of information that can be known as <strong>remarks</strong>. It
          may contain judgements that reflects the state of this student. Click
          them to get to the transaction proof.
        </div>
      </q-card-section>
      <q-scroll-area style="height: 100%; max-width: 100%">
        <q-item
          v-for="extra in portfolio_extra_container"
          :key="extra.tx_hash"
          :to="'/explorer/transaction/' + extra.tx_hash"
          style="text-decoration: none"
          clickable
          class="logdata"
        >
          <q-item-section class="text-h6">
            <q-item-label class="q-mb-sm">
              <span class="text-bold"> {{ extra.context.title }}</span> |
              <span class="text-bold q-ma-sm q-mb-sm q-ml-sm"> Timestamp:</span
              >{{ extra.context.timestamp }}</q-item-label
            >
            <q-item-label
              class="q-ml-sm text-justify q-mb-sm q-ml-lg"
              style="margin-top: 2%"
            >
              <span class="text-weight-bold q-mb-sm q-mr-sm"> Description:</span
              >{{ extra.context.description }}
            </q-item-label>
            <q-item-label
              class="q-ml-sm text-justify q-mb-sm q-ml-lg"
              style="margin-top: 2%"
            >
              <span class="text-weight-bold q-mb-sm q-mr-sm"> By:</span>
              <router-link
                :to="'/explorer/address/' + extra.context.inserter"
                style="text-decoration: none"
                >{{ extra.context.inserter }}</router-link
              >
            </q-item-label>
          </q-item-section>
        </q-item>
      </q-scroll-area>
    </div>
  </div>

  <q-dialog v-model="logModalState" class="modal">
    <q-card class="my-card-log">
      <q-card-section>
        <div class="text-h6">Log Detailed Information</div>
        <div class="text-subtitle1">
          Other fields not shown from the list were shown here. Not that some of
          the properties are not available for access, for instance, the file.
          Contact the student for the permission.
        </div>
      </q-card-section>
      <q-card-section class="wrap-content">
        <q-item>
          <q-item-section class="text-h6">
            <q-item-label class="q-mb-md"
              ><span class="text-weight-bold q-ma-sm q-mb-sm">Title:</span
              >{{ selectedLog.context.name }}</q-item-label
            >
            <q-item-label class="q-mb-md">
              <span class="text-weight-bold q-ma-sm q-mb-sm">Transaction:</span>

              <router-link
                :to="'/explorer/transaction/' + selectedLog.tx_hash"
                style="text-decoration: none"
                >{{ selectedLog.tx_hash }}</router-link
              >
            </q-item-label>
            <q-item-label class="q-mb-md">
              <span class="text-weight-bold q-ma-sm q-mb-sm">Description:</span
              >{{ selectedLog.context.description }}</q-item-label
            >
            <q-item-label class="q-mb-md">
              <span class="text-weight-bold q-ma-sm q-mb-sm">Role:</span
              >{{ selectedLog.context.role }}</q-item-label
            >

            <q-item-label class="q-mb-md">
              <span class="text-weight-bold q-ma-sm q-mb-sm">
                Inserter / Validated by:</span
              >

              <router-link
                :to="'/explorer/address/' + selectedLog.context.validated_by"
                style="text-decoration: none"
                >{{ selectedLog.context.validated_by }}</router-link
              >
            </q-item-label>
            <q-item-label class="q-mb-md">
              <span class="text-weight-bold q-ma-sm q-mb-sm"> File:</span>
              <q-btn
                outline
                color="black"
                label="View / Download"
                class="q-mr-md"
                @click="
                  getFile(
                    selectedLog.context.address_origin,
                    selectedLog.context.file
                  )
                "
                :disable="selectedLog.context.file === null"
              />
            </q-item-label>

            <q-item-label class="q-mb-md">
              <span class="text-weight-bold q-ma-sm q-mb-sm">
                Duration Start:</span
              >{{ selectedLog.context.duration_start }}</q-item-label
            >
            <q-item-label
              class="q-mb-md"
              v-if="selectedLog.context.duration_end !== null"
            >
              <span class="text-weight-bold q-ma-sm q-mb-sm">
                Duration End:</span
              >{{ selectedLog.context.duration_end }}</q-item-label
            >
            <q-item-label class="q-mb-md">
              <span class="text-weight-bold q-ma-sm q-mb-sm">
                Transaction Timestamp:</span
              >{{ selectedLog.context.timestamp }}</q-item-label
            >
          </q-item-section>
        </q-item>
      </q-card-section>

      <q-card-actions align="right" style="padding-bottom: 3%">
        <q-btn
          v-close-popup
          flat
          v-ripple
          label="Close Modal"
          style="color: #f44336"
          class="q-mr-md"
        />
      </q-card-actions>
    </q-card>
  </q-dialog>

  <q-page-sticky position="bottom-right" :offset="[24, 24]">
    <q-btn
      fab
      v-ripple
      icon="mdi-file-cog"
      color="red"
      v-if="isStudent"
      @click="portfolio_modal = true"
    >
      <q-tooltip
        class="bg-indigo"
        :offset="[10, 10]"
        anchor="center left"
        self="center right"
      >
        Portfolio Settings
      </q-tooltip>
    </q-btn>
  </q-page-sticky>

  <q-dialog v-model="portfolio_modal" class="modal">
    <q-card style="width: 100%">
      <q-linear-progress
        v-if="isProcessing"
        rounded
        query
        indeterminate
        color="red"
      />
      <q-tabs
        v-model="selected_settings"
        dense
        class="text-grey"
        active-color="secondary"
        indicator-color="secondary"
        align="justify"
        style="height: 50px"
      >
        <q-tab
          name="share_settings"
          label="Settings"
          class="tab"
          :disable="isProcessing"
        />
        <q-tab
          name="editable_infos"
          label="Editables"
          class="tab"
          :disable="isProcessing"
        />
      </q-tabs>

      <q-separator />

      <q-tab-panels
        v-model="selected_settings"
        v-if="isStudent"
        animated
        class="panels"
      >
        <q-tab-panel name="share_settings">
          <q-card-section>
            <div class="text-h6 text-weight-bold">Share Settings</div>
          </q-card-section>

          <q-card-section class="text-justify">
            The following switches are states that can affect the output of your
            portfolio. Which means everyone who access your portfolio is
            affected, <strong>including you</strong>.
          </q-card-section>
          <q-card-section class="text-justify">
            <strong>Be careful</strong>, by applying changes (in the means of
            clicking the apply button) will subject you to rate-limitation of
            <strong>3 minutes.</strong>
          </q-card-section>

          <q-list style="padding-top: 3%">
            <q-item tag="label" v-ripple>
              <q-item-section>
                <q-item-label>Enable Portfolio Sharing</q-item-label>
                <q-item-label caption
                  >Allow others to see this portfolio by explicitly referring to
                  your address.</q-item-label
                >
              </q-item-section>
              <q-item-section side>
                <q-toggle
                  color="red"
                  :disable="isProcessing"
                  v-model="portfolio_sharing_state"
                />
              </q-item-section>
            </q-item>

            <q-item tag="label" v-ripple>
              <q-item-section>
                <q-item-label>Show Email Info</q-item-label>
                <q-item-label caption
                  >Allow others to see your email for contacting purposes. We
                  recommend doing this <strong>ONLY</strong> when you are
                  currently at job application.</q-item-label
                >
              </q-item-section>
              <q-item-section side top>
                <q-toggle
                  color="red"
                  :disable="isProcessing"
                  v-model="portfolio_show_email_state"
                />
              </q-item-section>
            </q-item>

            <q-item tag="label" v-ripple>
              <q-item-section>
                <q-item-label>Allow Files</q-item-label>
                <q-item-label caption
                  >Allow others to view and download your files.
                  <strong>Note that</strong>, these are your proof or supporting
                  context behind these logs and extra information.
                  <strong>You are not liable</strong> when there's a data
                  leakage as you are not the one who inserts these
                  information.</q-item-label
                >
              </q-item-section>
              <q-item-section side top>
                <q-toggle
                  color="red"
                  :disable="isProcessing"
                  v-model="portfolio_allow_file_state"
                />
              </q-item-section>
            </q-item>

            <q-card-actions align="right">
              <q-btn
                flat
                style="color: #3700b3"
                label="Close Modal"
                @click="portfolio_modal = false"
              />
              <q-btn
                flat
                class="red"
                :disable="portfolio_setting_btn_click_state"
                label="Apply Settings"
                @click="submitPortfolioSettings"
              />
            </q-card-actions>
          </q-list>
        </q-tab-panel>

        <q-tab-panel name="editable_infos">
          <q-form
            @submit.prevent="submitEditableInfo"
            @validation-error="submitEditableInfoOnError"
            :autofocus="true"
          >
            <q-card-section>
              <div class="text-h6 text-weight-bold">Editable Information</div>
            </q-card-section>

            <q-card-section class="text-justify">
              Here are the fields that you can interchange even when blockchain
              already imprints the initial state of these fields.
              <strong>Be careful</strong>, change only if necessary.
            </q-card-section>

            <q-card-section>
              <q-input
                class="input"
                outlined
                dense
                color="secondary"
                v-model="editable_info_preferred_role"
                label="Preferred Role"
                counter
                lazy-rules
                hint="Your preferred role in the industry or in works."
                :disable="isProcessing"
                :rules="[
                  (val) =>
                    (val.length >= 4 && val.length <= 32) ||
                    'This should contain not less than 4 characters or more than 32 characters.',
                ]"
              />
              <q-input
                class="input"
                outlined
                dense
                color="secondary"
                v-model="editable_info_personal_skills"
                label="Personal Skills"
                counter
                hint="Similar to description but is specified to student's capability. Seperate the contents in comma. Please note only important or significant skills that you have."
                :rules="[
                  (val) =>
                    (val && val.length >= 8) ||
                    'This is required. Must have 8 characters and above.',
                ]"
                lazy-rules
                :disable="isProcessing"
              />

              <q-input
                class="input"
                outlined
                dense
                color="secondary"
                v-model="editable_info_description"
                type="textarea"
                label="Description"
                hint="Literally, the description about you, but keep it professional as it was shown in your portfolio."
                :disable="isProcessing"
                counter
                :rules="[
                  (val) =>
                    (val && val.length >= 8) ||
                    'This is required. Must have 8 characters and above.',
                ]"
                lazy-rules
              />
            </q-card-section>

            <q-card-actions align="right">
              <q-btn
                flat
                style="color: #3700b3"
                label="Close Modal"
                @click="portfolio_modal = false"
              />
              <q-btn
                flat
                type="submit"
                style="color: #ff0080"
                label="Apply New Info"
                :disable="editable_info_btn_click_state"
              />
            </q-card-actions>
          </q-form>
        </q-tab-panel>
      </q-tab-panels>
    </q-card>
  </q-dialog>
</template>

<script>
import { defineComponent, ref } from 'vue';

import { useQuasar } from 'quasar';
import axios from 'axios';
import { MASTER_NODE_BACKEND_URL } from '/utils/utils.js';
import { useRoute, useRouter } from 'vue-router';

export default defineComponent({
  data() {
    return {
      // * Card on Top.
      portfolio_user_address: ref('—'),
      portfolio_user_association: ref('—'),

      portfolio_user_program: ref('—'),

      portfolio_user_description: ref('—'),
      portfolio_user_personal_skills: ref('—'),
      portfolio_user_preferred_role: ref('—'),

      // * Containers.
      portfolio_extra_container: ref([]),
      portfolio_log_container: ref([]),

      portfolio_user_email_contact: ref('—'),

      // * State and Field Variables
      portfolio_modal: ref(false),
      selected_settings: ref('share_settings'),
      portfolio_extra_info_rendering_state: ref(true),
      portfolio_log_info_rendering_state: ref(true),
      isProcessing: ref(false),

      portfolio_sharing_state: ref(false),
      portfolio_show_email_state: ref(false),
      portfolio_allow_file_state: ref(false),

      portfolio_setting_btn_click_state: ref(false),
      editable_info_btn_click_state: ref(false),

      editable_info_description: ref(''),
      editable_info_preferred_role: ref(''),
      editable_info_personal_skills: ref(''),

      // * Switch Variables
      isStudent: ref(false),
      isOrg: ref(false),
      isAnonymous: ref(false),
    };
  },

  setup() {
    const $q = useQuasar();
    const $route = useRoute();
    const $router = useRouter();

    return {
      logModalState: ref(false),
      selectedLog: ref(null),
    };
  },
  mounted() {
    this.getPortfolio();

    if (this.isStudent) {
      this.loadPortfolioSettings();
      this.loadEditableInfo();
    }
  },
  methods: {
    loadPortfolioSettings() {
      this.isProcessing = true;
      this.portfolio_setting_btn_click_state = false;
      axios
        .get(`http://${MASTER_NODE_BACKEND_URL}/dashboard/portfolio_settings`, {
          headers: {
            'X-Token': this.$q.localStorage.getItem('token'),
          },
        })
        .then((response) => {
          this.portfolio_sharing_state = response.data.enable_sharing;
          this.portfolio_show_email_state = response.data.expose_email_info;
          this.portfolio_allow_file_state = response.data.show_files;

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
            message: `There was an error when fetching your information. Due to this, switches will be disabled. Please refresh and try again. Reason: ${responseDetail}`,
            timeout: 10000,
            progress: true,
            icon: 'report_problem',
          });
        });
    },
    loadEditableInfo() {
      this.isProcessing = true;
      axios
        .get(`http://${MASTER_NODE_BACKEND_URL}/dashboard/user_profile`, {
          headers: {
            'X-Token': this.$q.localStorage.getItem('token'),
          },
        })
        .then((response) => {
          this.editable_info_description = response.data.description;
          this.editable_info_preferred_role = response.data.preferred_role;
          this.editable_info_personal_skills = response.data.personal_skills;

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
            message: `There was an error when fetching your information. Due to this, fields will be disabled. Please refresh and try again. Reason: ${responseDetail}`,
            timeout: 10000,
            progress: true,
            icon: 'report_problem',
          });
        });
    },
    submitEditableInfo() {
      this.editable_info_btn_click_state = true;
      this.isProcessing = true;

      // ! Set up the FormData(), this was intended for avatar reuse purposes.
      // - Though it's implementation is not yet added.
      let editableInfoForm = new FormData();

      editableInfoForm.append('description', this.editable_info_description);
      editableInfoForm.append(
        'personal_skills',
        this.editable_info_personal_skills
      );
      editableInfoForm.append(
        'preferred_role',
        this.editable_info_preferred_role
      );
      axios
        .post(
          `http://${MASTER_NODE_BACKEND_URL}/dashboard/apply_profile_changes`,
          editableInfoForm,
          {
            headers: {
              'X-Token': this.$q.localStorage.getItem('token'),
              'Content-Type': 'multipart/form-data',
            },
          }
        )
        .then((response) => {
          this.$q.notify({
            color: 'green',
            position: 'top',
            message:
              'Editable information has been saved! Refreshing in 3 seconds ...',
            timeout: 10000,
            progress: true,
            icon: 'report_problem',
          });
          setTimeout(() => {
            this.$router.go();
          }, 3000);
        })
        .catch((e) => {
          const responseDetail =
            e.response.data === undefined
              ? `${e.message}. Server may be unvailable. Please try again later.`
              : e.response.data.detail;

          this.$q.notify({
            color: 'negative',
            position: 'top',
            message: `There was an error when submitting new information. Reason: ${responseDetail}`,
            timeout: 10000,
            progress: true,
            icon: 'report_problem',
          });
        });
      this.isProcessing = false;
    },
    submitEditableInfoOnError() {
      this.$q.notify({
        color: 'negative',
        position: 'top',
        message:
          'There was an error from one of the fields. Please check and try again.',
        timeout: 10000,
        progress: true,
        icon: 'report_problem',
      });
    },
    submitPortfolioSettings() {
      this.isProcessing = true;
      this.portfolio_setting_btn_click_state = true;

      axios
        .post(
          `http://${MASTER_NODE_BACKEND_URL}/dashboard/apply_portfolio_settings`,
          {
            enable_sharing: this.portfolio_sharing_state,
            expose_email_info: this.portfolio_show_email_state,
            show_files: this.portfolio_allow_file_state,
          },
          {
            headers: {
              'X-Token': this.$q.localStorage.getItem('token'),
            },
          }
        )
        .then((response) => {
          this.$q.notify({
            color: 'green',
            position: 'top',
            message:
              'Portfolio settings has been saved! Refreshing in 3 seconds ...',
            timeout: 10000,
            progress: true,
            icon: 'report_problem',
          });
          setTimeout(() => {
            this.$router.go();
          }, 3000);
        })
        .catch((e) => {
          const responseDetail =
            e.response.data === undefined
              ? `${e.message}. Server may be unvailable. Please try again later.`
              : e.response.data.detail;

          this.$q.notify({
            color: 'negative',
            position: 'top',
            message: `There was an error when submitting portfolio settings. Due to this, lease refresh and try again. Reason: ${responseDetail}`,
            timeout: 10000,
            progress: true,
            icon: 'report_problem',
          });
        });
      this.isProcessing = false;
    },
    getPortfolio() {
      // ! Reset states.
      // this.isStudent = false;
      // this.isOrg = false;
      // this.isAnonymous = false;

      // - Resolve origin of the address.
      let portfolioURL = `http://${MASTER_NODE_BACKEND_URL}/dashboard/portfolio`;

      // * Check if 'address' was existing from the localStorage along with the 'token'.
      // * If both does not exist, then check if 'address' is specified via URL path parameter. This was for the case of being accessed by an anonymous user.
      // - Resolve user data.
      // - Resolve list of logs data.
      // - Resolve list of extra data.

      // - Condition for allowing students to access their own portfolio.
      if (
        this.$route.query.address === undefined &&
        this.$q.localStorage.getItem('token') !== null &&
        this.$q.localStorage.getItem('role') === 'Student Dashboard User'
      ) {
        this.isStudent = true;
      }
      // - Condition for allowing organizations to access a particular portfolio
      else if (
        this.$route.query.address !== undefined &&
        this.$q.localStorage.getItem('token') !== null &&
        this.$q.localStorage.getItem('role') == 'Organization Dashboard User'
      ) {
        this.isOrg = true;
        portfolioURL += `?address=${this.$route.query.address}`;
      }

      // - Condition for allowing anonymous users from accessing a particular portfolio.
      else if (
        this.$route.query.address !== undefined &&
        this.$q.localStorage.getItem('token') === null
      ) {
        this.isAnonymous = true;
        portfolioURL += `?address=${this.$route.query.address}`;
      } else {
        void this.$router.push({
          path:
            this.$q.localStorage.getItem('role') ===
            'Organization Dashboard User '
              ? '/dashboard'
              : '/',
        });

        this.$q.notify({
          color: 'negative',
          position: 'top',
          message:
            'You are not allowed to access this view. If you are an anonymous, please ensure that the address you copied is exactly 35 characters or the address were not found.',
          timeout: 10000,
          progress: true,
          icon: 'report_problem',
        });

        return;
      }

      // ! Prepare the payload.
      let headerForAuth = {
        headers: {
          'X-Token': this.$q.localStorage.getItem('token'),
        },
      };

      axios
        .get(portfolioURL, this.isOrg || this.isStudent ? headerForAuth : {})
        .then((response) => {
          this.$q.notify({
            color: 'blue',
            position: 'top',
            message: this.isAnonymous
              ? 'You are accessing this portfolio as an anonymous.'
              : this.isOrg
              ? "You are accessing this student's portfolio as a preview. Note that you cannot modify these entries anymore."
              : "You are accessing this as a student, please check your portfolio settings on the bottom-right to adjust your portfolio's output.",
            timeout: 10000,
            progress: true,
            icon: 'info',
          });

          // - Assign User's Information
          this.portfolio_user_address = response.data.address;
          this.portfolio_user_association = response.data.association;
          this.portfolio_user_program = response.data.program;
          this.portfolio_user_description =
            response.data.description === null
              ? 'No information'
              : response.data.description;
          this.portfolio_user_personal_skills =
            response.data.personal_skills === null
              ? 'No information.'
              : response.data.personal_skills;
          this.portfolio_user_preferred_role = response.data.preferred_role;
          this.portfolio_user_email_contact =
            response.data.email === null
              ? 'Not Available.'
              : response.data.email;

          // - Add extra information from the container.
          // ! We don't need to assign an ID since there's no need of modal.
          this.portfolio_extra_container = response.data.extra;
          this.portfolio_extra_info_rendering_state = false;

          // - Add log information from the container.
          let log_info_counter = 1;
          let log_temp_container = [];

          // Process the transaction.
          for (let log_info of response.data.logs) {
            log_info.id = log_info_counter;

            log_info.context.duration_start = new Date(
              log_info.context.duration_start
            ).toLocaleDateString();

            if (log_info.context.duration_end !== null) {
              log_info.context.duration_end = new Date(
                log_info.context.duration_end
              ).toLocaleDateString();
            }

            log_temp_container.push(log_info);
            log_info_counter++;
          }
          this.portfolio_log_container = log_temp_container;
          this.portfolio_log_info_rendering_state = false;
        })
        .catch((e) => {
          const responseDetail =
            e.response.data === undefined
              ? `${e.message}. Server may be unvailable. Please try again later.`
              : e.response.data.detail;

          this.$q.notify({
            color: 'negative',
            position: 'top',
            message: `There was an error when fetching portfolio. Reason: ${responseDetail}`,
            timeout: 10000,
            progress: true,
            icon: 'report_problem',
          });
          this.$router.go(-1);
        });
    },
    getLogInfo(id) {
      this.logModalState = true;

      this.selectedLog = this.portfolio_log_container[id - 1];
    },
    getFile(address_origin, file_hash) {
      let portfolioFileURL = `http://${MASTER_NODE_BACKEND_URL}/dashboard/portfolio/${address_origin}/file/${file_hash}`;

      axios.get(portfolioFileURL, { responseType: 'blob' }).then((response) => {
        let blob = new Blob([response.data], { type: 'application/pdf' });
        let url = window.URL.createObjectURL(blob);

        window.open(url);
      });
    },
  },
});
</script>

<style scoped>
* {
  font-family: 'Poppins';
}
.header {
  background-color: #a7eaff;
  margin: 2%;
  margin-top: 1%;
  margin-bottom: 1%;
  padding-bottom: 1%;
  border-style: solid;
  border-radius: 10px;
}

.wrap-content {
  inline-size: auto;
  overflow-wrap: break-word;
}

.avatar {
  height: 150px;
  width: 10%;
  float: left;
}

.input {
  margin-top: 3%;
}

.usericon {
  font-size: 9em;
}

.logs {
  height: 1000px;
  width: 47%;
  border-radius: 2%;
  margin-left: 2%;
}

.log {
  height: 470px;
  width: 100%;
  padding: 1%;
  border-style: solid;
  border-radius: 10px;
}

.my-card {
  width: 100%;
  height: 70%;
}
.my-card-log {
  width: 100%;
}

.logdata {
  border-style: solid;
  margin-bottom: 1%;
  border-width: 2px;
  border-radius: 10px;
  background-color: #a7eaff;
}

.view {
  margin-left: 90%;
  width: 20%;
}

@media (max-width: 80em) {
  .view {
    margin-left: 75%;
    width: 40%;
  }
}

@media (max-width: 60em) {
  * {
    font-size: 1em;
  }

  .view {
    margin-left: 70%;
    width: 50%;
  }
}
</style>
