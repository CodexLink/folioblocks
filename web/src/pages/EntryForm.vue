<template>
  <img
    class="background"
    src="~assets/pagebackground.png"
    style="background-attachment: fixed"
  />
  <body>
    <RegisterContainer>
      <q-card>
        <q-linear-progress
          v-if="isProcessing"
          query
          color="secondary"
          class="q-mt-sm"
        />
        <q-tabs
          v-model="tab"
          class="text-grey tabs"
          active-color="secondary"
          indicator-color="secondary"
          align="justify"
        >
          <q-tab name="login" label="Login" />
          <q-tab name="register" label="Register" />
        </q-tabs>

        <q-separator />

        <q-tab-panels v-model="tab" animated>
          <q-tab-panel name="login">
            <q-form
              @submit.prevent="submitLoginRequest"
              @validation-error="errorOnSubmit"
              :autofocus="true"
            >
              <div>
                <h2>Hello! Welcome Back!</h2>
                <h4>
                  Please login to get started. Or renew your token from logging
                  in.
                </h4>
              </div>
              <q-input
                class="user"
                color="secondary"
                outlined
                :disable="isProcessing"
                v-model="login_username"
                label="Username"
                :rules="[
                  (val) => (val && val.length > 0) || 'This is required.',
                ]"
              />

              <q-input
                class="password"
                outlined
                :disable="isProcessing"
                color="secondary"
                v-model="login_password"
                label="Password"
                :type="login_show_password ? 'password' : 'text'"
                :rules="[
                  (val) => (val && val.length > 0) || 'This is required.',
                ]"
              >
                <template v-slot:append>
                  <q-icon
                    :name="
                      login_show_password ? 'visibility_off' : 'visibility'
                    "
                    class="cursor-pointer"
                    @click="login_show_password = !login_show_password"
                  />
                </template>
              </q-input>

              <div class="btn">
                <q-btn class="login" rounded color="red" label="Back" to="/" />

                <q-btn
                  class="login"
                  rounded
                  color="secondary"
                  label="Login"
                  type="submit"
                  :disable="isProcessing"
                />
              </div>
            </q-form>
          </q-tab-panel>

          <q-tab-panel name="register">
            <q-form
              @submit.prevent="submitRegisterRequest"
              @validation-error="errorOnSubmit"
              :autofocus="true"
            >
              <div>
                <h2>Thank you for taking interest!</h2>
                <h4>
                  Fill the fields below. Remember,
                  <strong>get the authentication code</strong>
                  from your supervisor for you to proceed your regisration.
                </h4>
              </div>
              <q-separator />
              <div>
                <h4><strong>Personal Information</strong></h4>
                <h4>
                  Following fields are required to identify you
                  <strong>internally</strong>. Don't worry, your identity will
                  not be exposed <strong>except</strong> the contact form which
                  is the <strong>email</strong> you inputted from this form.
                </h4>
              </div>
              <div class="row">
                <q-input
                  class="double"
                  outlined
                  color="secondary"
                  v-model="first_name"
                  label="First Name"
                  counter
                  :rules="[
                    (val) =>
                      (val.length >= 2 && val.length <= 32) ||
                      'Invalid, this is required. Should contain 2 to 32 characters.',
                  ]"
                  lazy-rules
                  :disable="isProcessing"
                />
                <q-input
                  class="double"
                  outlined
                  color="secondary"
                  v-model="last_name"
                  label="Last Name"
                  counter
                  :rules="[
                    (val) =>
                      (val.length >= 2 && val.length <= 32) ||
                      'Invalid, this is required. Should contain 2 to 32 characters.',
                  ]"
                  lazy-rules
                  :disable="isProcessing"
                />
              </div>
              <q-input
                class="data"
                outlined
                color="secondary"
                v-model="email"
                type="email"
                label="E-mail"
                :error="register_email_invalid"
                @focus="register_email_invalid = false"
                counter
                lazy-rules
                :disable="isProcessing"
                :rules="[(val) => val.includes('@') || 'Invalid email format.']"
              >
                <template v-slot:error>
                  E-mail may be already used. Please contact your administrator
                  on this issue.
                </template>
              </q-input>
              <q-separator />
              <div>
                <h4><strong>Organization Information</strong></h4>
                <h4>
                  Following fields require to specify your organization as a new
                  entity from the system. Should there be an existing
                  organization must
                  <strong>only fill the organization address</strong> as well as
                  setting the organization type as <strong>Existing</strong> and
                  nothing else.
                </h4>
                <h4>
                  Note that, you have to be <strong>very careful</strong> from
                  your inputs as these are unmodifiable due to nature of
                  blockchain.
                </h4>
              </div>
              <div class="row">
                <q-input
                  class="double"
                  outlined
                  color="secondary"
                  counter
                  v-model="org_name"
                  :error="register_org_name_invalid"
                  @focus="register_org_name_invalid = false"
                  label="Organization Name"
                  hint="Must be in Title Case."
                  :rules="[
                    (val) =>
                      !val.length ||
                      (val.length >= 2 && val.length <= 64) ||
                      'Name should not be less than 1 character or more than 64 characters.',
                  ]"
                  lazy-rules
                  :disable="isProcessing"
                >
                  <template v-slot:error>
                    If you are inserting an existing organization, please clear
                    this field.
                  </template>
                </q-input>

                <q-input
                  class="double"
                  outlined
                  counter
                  color="secondary"
                  v-model="org_address"
                  :error="register_org_address_invalid"
                  @focus="register_org_address_invalid = false"
                  label="Organization Address"
                  hint="Must
                start with 'fl:'."
                  :rules="[
                    (val) =>
                      !val.length ||
                      (val.length == 35 && val.startsWith('fl:')) ||
                      'Invalid format, should start with prefix `fl:` and should be exactly 35 characters.',
                  ]"
                  lazy-rules
                  :disable="isProcessing"
                >
                  <template v-slot:error>
                    This may be required. If you are inserting a new
                    organization, please clear this field, otherwise, proceed.
                  </template>
                </q-input>
              </div>

              <q-select
                class="data"
                color="secondary"
                outlined
                v-model="org_type_chosen"
                :options="org_options"
                :error="register_org_type_invalid"
                @focus="register_org_type_invalid = false"
                label="Organization Type"
                :disable="isProcessing"
              >
                <template v-slot:error>
                  For existing organization, please choose
                  <strong>existing</strong> and fill up
                  <strong>ONLY</strong> the organization address, otherwise,
                  fill other fields that shows an error.
                </template>
              </q-select>

              <q-input
                class="data"
                outlined
                color="secondary"
                v-model="org_description"
                type="textarea"
                label="Organization Description"
                counter
                :error="register_org_description_invalid"
                @focus="register_org_description_invalid = false"
                hint="Be careful, content should be finalized before submitting."
                :rules="[
                  (val) =>
                    !val.length ||
                    (val.length >= 8 && val.length <= 256) ||
                    'Cannot go less than 8 characters or more than 256 characters.',
                ]"
                lazy-rules
                :disable="isProcessing"
              >
                <template v-slot:error>
                  This may be required. If you are inserting an existing
                  organization, please clear this field, otherwise, add a date.
                </template>
              </q-input>

              <q-input
                filled
                v-model="org_date"
                class="data"
                mask="date"
                prefix="Organization Founded"
                readonly
                :error="register_org_founded_invalid"
                hint="The date from where your institution or your organization was founded."
                :disable="isProcessing"
              >
                <template v-slot:append>
                  <q-icon
                    name="cancel"
                    v-if="org_date"
                    @click.stop="
                      org_date = '';
                      register_org_founded_invalid = false;
                    "
                    class="cursor-pointer"
                  />
                  <q-icon name="event" class="cursor-pointer">
                    <q-popup-proxy
                      ref="qDateProxy"
                      cover
                      transition-show="scale"
                      transition-hide="scale"
                    >
                      <q-date
                        v-model="org_date"
                        @click="register_org_founded_invalid = false"
                        color="secondary"
                        today-btn
                        :options="optionsFn"
                        :disable="isProcessing"
                      >
                        <div class="row items-center justify-end">
                          <q-btn
                            v-close-popup
                            label="Close"
                            color="primary"
                            flat
                          />
                        </div>
                      </q-date>
                    </q-popup-proxy>
                  </q-icon>
                </template>
                <template v-slot:error>
                  This may be required. If you are inserting an existing
                  organization, please clear this field, otherwise, check for
                  other fields.
                </template>
              </q-input>

              <q-separator />

              <q-input
                class="data"
                outlined
                color="secondary"
                v-model="register_username"
                label="Username"
                counter
                hint="This will be used to login."
                :disable="isProcessing"
                :rules="[
                  (val) =>
                    (val.length >= 8 && val.length <= 24) ||
                    'This should contain not less than 8 characters or more than 24 characters.',
                ]"
                lazy-rules
              />
              <div class="row">
                <q-input
                  class="double"
                  outlined
                  color="secondary"
                  v-model="register_password"
                  label="Password"
                  counter
                  :type="register_show_password ? 'text' : 'password'"
                  :disable="isProcessing"
                  :rules="[
                    (val) =>
                      (val.length >= 8 && val.length <= 64) ||
                      'This should contain not less than 8 characters or more than 64 characters.',
                  ]"
                  lazy-rules
                >
                  <template v-slot:append>
                    <q-icon
                      :name="
                        register_show_password ? 'visibility' : 'visibility_off'
                      "
                      class="cursor-pointer"
                      @click="register_show_password = !register_show_password"
                    /> </template
                ></q-input>
                <q-input
                  class="double"
                  outlined
                  color="secondary"
                  v-model="register_confirm_password"
                  label="Confirm Password"
                  counter
                  :type="register_show_confirm_password ? 'text' : 'password'"
                  :rules="[
                    (val) =>
                      (val.length >= 8 &&
                        val.length <= 64 &&
                        val == register_password) ||
                      'This should match your password to confirm your password.',
                  ]"
                  :disable="isProcessing"
                >
                  <template v-slot:append>
                    <q-icon
                      :name="
                        register_show_confirm_password
                          ? 'visibility'
                          : 'visibility_off'
                      "
                      class="cursor-pointer"
                      @click="
                        register_show_confirm_password =
                          !register_show_confirm_password
                      "
                    />
                  </template>
                </q-input>
              </div>
              <q-input
                class="data"
                outlined
                color="secondary"
                v-model="register_auth_code"
                type="text"
                label="Authentication Code"
                hint="Remember, talk to your representatives to get your authentication code."
                :disable="isProcessing"
                :error="register_auth_code_invalid"
                @focus="register_auth_code_invalid = false"
                :rules="[(val) => val.length || 'This cannot be empty!']"
              >
                <template v-slot:error>
                  Authentication code is invalid. Check your email inbox and try
                  again.
                </template>
              </q-input>

              <q-separator />

              <q-card-section>
                <h4><strong>Notice</strong></h4>
                Please ensure your inputs are correct before proceeding, there's
                no going back or be able to change them once submitted.
              </q-card-section>
              <div class="registerbtn">
                <q-btn
                  class="backbtn"
                  rounded
                  color="red"
                  label="Back"
                  to="/"
                />

                <q-btn
                  class="register"
                  rounded
                  color="secondary"
                  label="Register"
                  type="submit"
                  :disable="isProcessing"
                />
              </div>
            </q-form>
          </q-tab-panel>
        </q-tab-panels>
      </q-card>
    </RegisterContainer>
  </body>
</template>

<script>
import { defineComponent, ref } from 'vue';
import RegisterContainer from 'src/components/RegisterContainer.vue';
import { useRoute, useRouter } from 'vue-router';
import axios from 'axios';
import { useQuasar } from 'quasar';
import { MASTER_NODE_BACKEND_URL } from '/utils/utils.js';
export default defineComponent({
  name: 'EntryForm',
  components: { RegisterContainer },
  data() {
    return {
      first_name: ref(''),
      last_name: ref(''),
      email: ref(''),

      org_name: ref(''),
      org_address: ref(''),
      org_description: ref(''),

      isProcessing: ref(false),
      org_date: ref(''),

      register_username: ref(''),
      register_password: ref(''),
      register_confirm_password: ref(''),
      register_auth_code: ref(''),

      login_username: ref(''),
      login_password: ref(''),

      register_org_name_invalid: ref(false),
      register_email_invalid: ref(false),
      register_org_address_invalid: ref(false),
      register_org_type_invalid: ref(false),
      register_org_description_invalid: ref(false),
      register_org_founded_invalid: ref(false),
      register_username_invalid: ref(false),
      register_auth_code_invalid: ref(false),

      login_show_password: ref(true),
      register_show_password: ref(false),
      register_show_confirm_password: ref(false),
    };
  },

  setup() {
    const $route = useRoute();
    const $router = useRouter();
    const $q = useQuasar();

    return {
      tab: ref($route.params.action),
      org_options: [
        { label: 'Existing', value: null },
        { label: 'Institution', value: 1 },
        { label: 'Organization', value: 2 },
      ],
      org_type_chosen: ref({ label: 'Existing', value: null }),

      date: new Date().toISOString().slice(0, 10).replaceAll('-', '/'),
    };
  },
  methods: {
    submitLoginRequest() {
      this.isProcessing = true;

      axios
        .post(`${MASTER_NODE_BACKEND_URL}/entity/login`, {
          username: this.login_username,
          password: this.login_password,
        })
        .then((response) => {
          try {
            // * Check condition wherein we prohibit other `ARCHIVAL_MINER_NODES` and `MASTER_NODES` from logging in since they have nothing to do with the dashboard.
            if (response.data.user_role == 'Archival Miner Node User') {
              this.$q.notify({
                color: 'negative',
                position: 'top',
                message:
                  'Archival node accounts are not allowed to use the dashboard. Your account can only be used at logging in folioblocks-cli.',
                timeout: 5000,
                progress: true,
                icon: 'mdi-account-cancel-outline',
              });

              // * Logout the token gracefully, without handling the error since we didn't do anything regarding storing something from the localStorage..
              axios.post(
                `${MASTER_NODE_BACKEND_URL}/entity/logout`,
                {
                  /* ... data*/
                },
                {
                  headers: {
                    'X-Token': response.data.jwt_token,
                  },
                }
              );
              this.isProcessing = false;
            } else {
              // * Clear out the local storage first.
              this.$q.localStorage.clear();

              // * Then set the current token and the address.
              this.$q.localStorage.set('token', response.data.jwt_token);
              this.$q.localStorage.set('address', response.data.user_address);
              this.$q.localStorage.set(
                'role',
                response.data.user_role === 'Master Node User'
                  ? 'Administrator'
                  : response.data.user_role
              );

              // * Some some toast.
              this.$q.notify({
                color: 'green',
                position: 'top',
                message: 'Login successful!',
                timeout: 5000,
                progress: true,
                icon: 'mdi-account-check',
              });

              // * And redirect the user.
              this.$router.push({ path: '/dashboard' });
              this.isProcessing = false;
            }
          } catch (e) {
            this.$q.clear();
            this.isProcessing = false;
          }
        })
        .catch((e) => {
          const responseDetail =
            e.response.data === undefined
              ? `${e.message}. Server may be unvailable. Please try again later.`
              : e.response.data.detail;

          this.$q.notify({
            color: 'negative',
            position: 'top',
            message: `There was an error when submitting your credentials. | Info: ${responseDetail}`,
            timeout: 5000,
            progress: true,
            icon: 'report_problem',
          });

          this.isProcessing = false;
        });
    },
    optionsFn(org_date) {
      let datePlusOne = new Date();

      // * Modify the new instance, 'date' + 1.
      datePlusOne.setDate(datePlusOne.getDate() + 1);

      return (
        new Date(null).toISOString().slice(0, 10).replaceAll('-', '/') >=
          org_date ||
        org_date <= datePlusOne.toISOString().slice(0, 10).replaceAll('-', '/')
      );
    },
    submitRegisterRequest() {
      this.isProcessing = true;

      // * Create the base payload which should be modified later.
      let defaultPayload = {
        first_name: this.first_name,
        last_name: this.last_name,
        username: this.register_username,
        password: this.register_confirm_password,
        email: this.email,
        auth_code: this.register_auth_code,
      };
      let payloadConditionSufficient = false;

      // ! Check the fields from the organization.
      // - We need to ensure that both cases for referencing and creating a new organization should be handled here.
      console.log(this.org_date, typeof this.org_date);

      // * Case for creating an organization. Org address should contain nothing.
      if (
        this.org_name.length &&
        !this.org_address.length &&
        this.org_description.length &&
        this.org_type_chosen.value !== null &&
        this.org_date !== ''
      ) {
        defaultPayload.association_name = this.org_name;
        defaultPayload.association_type = this.org_type_chosen.value;
        defaultPayload.association_founded = new Date(
          this.org_date
        ).toISOString();
        defaultPayload.association_description = this.org_description;

        payloadConditionSufficient = true;
      }
      // * Case for creating an account with reference to the organization. Address should only be filled.
      else if (
        !this.org_name.length &&
        this.org_address.length &&
        !this.org_description.length &&
        this.org_type_chosen.value === null &&
        (this.org_date === null || this.org_date === '')
      ) {
        defaultPayload.association_address = this.org_address;

        payloadConditionSufficient = true;
      } else {
        this.$q.notify({
          color: 'negative',
          position: 'top',
          message:
            'Please keep the organization address filled only when the organization exists, otherwise, fill other fields except for the organization address.',
          timeout: 5000,
          progress: true,
          icon: 'report_problem',
        });

        // ! Condition for handling other fields (excluding the address) for the organization.
        if (this.org_type_chosen.value === null) {
          if (this.org_name !== '') this.register_org_name_invalid = true;
          else this.register_org_name_invalid = false;

          if (this.org_description !== '')
            this.register_org_description_invalid = true;
          else this.register_org_description_invalid = false;

          if (this.org_date !== '') this.register_org_founded_invalid = true;
          else this.register_org_founded_invalid = false;

          if (this.org_address !== '')
            this.register_org_address_invalid = false;
          else this.register_org_address_invalid = true;

          this.register_org_type_invalid = true;
          this.isProcessing = false;
          return;
        } else {
          if (this.org_name === '') this.register_org_name_invalid = true;
          else this.register_org_name_invalid = false;

          if (this.org_description === '')
            this.register_org_description_invalid = true;
          else this.register_org_description_invalid = false;

          if (this.org_date === '') this.register_org_founded_invalid = true;
          else this.register_org_founded_invalid = false;

          if (this.org_address === '')
            this.register_org_address_invalid = false;
          else this.register_org_address_invalid = true;

          this.register_org_type_invalid = true;
          this.isProcessing = false;
          return;
        }
      }

      if (payloadConditionSufficient) {
        // * Once the payload has been resolved (it's fields, ofc), do API call.
        axios
          .post(`${MASTER_NODE_BACKEND_URL}/entity/register`, {
            ...defaultPayload,
          })
          .then((_response) => {
            this.$q.notify({
              color: 'green',
              position: 'top',
              message:
                'Registration successful! Please check your email and login.',
              timeout: 5000,
              progress: true,
              icon: 'mdi-account-check',
            });
            this.isProcessing = false;
            void this.$router.push({ path: '/' });
          })
          .catch((e) => {
            const responseDetail =
              e.response.data === undefined
                ? `${e.message}. Server may be unvailable. Please try again later.`
                : e.response.data.detail;

            this.$q.notify({
              color: 'negative',
              position: 'top',
              message: `There was an error when submitting your credentials. Reason: ${responseDetail}`,
              timeout: 5000,
              progress: true,
              icon: 'report_problem',
            });

            // ! Clear previous errors.
            this.register_org_address_invalid = false;
            this.register_org_name_invalid = false;
            this.register_org_type_invalid = false;
            this.register_org_description_invalid = false;
            this.register_org_founded_invalid = false;

            if (e.response.data !== undefined) {
              if (
                e.response.data.detail.includes('`auth_token` were not found.')
              ) {
                this.register_auth_code_invalid = true;
              } else if (
                e.response.data.detail.includes(
                  'UNIQUE constraint failed: users.username'
                )
              ) {
                this.register_username_invalid = true;
              } else if (
                e.response.data.detail.includes(
                  'UNIQUE constraint failed: users.email'
                )
              ) {
                this.register_email_invalid = true;
              } else if (
                e.response.data.detail.includes(
                  'The supplied parameter for the `association` address reference does not exist'
                )
              ) {
                this.register_auth_code_invalid = true;
              }
            }

            this.isProcessing = false;
          });
      }
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
body {
  height: 100vh;
  padding: 3% 0%;
}

.background {
  position: fixed;
  z-index: -1;
  width: 100%;
  height: 100%;
  object-fit: cover;
  -webkit-filter: brightness(40%);
  filter: brightness(40%);
}

.user {
  margin: 2%;
  margin-top: 5%;
}
.password {
  margin: 2%;
  margin-top: 5%;
}

.btn {
  margin: 2%;
  display: grid;
  gap: 1em;
  grid-template-columns: repeat(2, 1fr);
  padding: 1%;
  font-size: 1em;
}

.login {
  height: 50px;
}

.registerbtn {
  margin: 2%;
  display: grid;
  gap: 1em;
  grid-template-columns: repeat(2, 1fr);
  padding: 1%;
  font-size: 1em;
}

p {
  text-align: center;
}

.qcheck {
  margin-left: 2%;
}

h2 {
  font-size: 1.7em;
  font-weight: 600;
  line-height: 5px;

  margin-left: 3%;
}

h4 {
  font-size: 1em;
  line-height: 20px;

  margin-left: 3%;
}

.data {
  margin: 3%;
}
.double {
  width: 44%;
  margin: 3%;
}

.username {
  width: 30%;
  margin: 3%;
}

.email {
  width: 58%;
  margin: 3%;
}

.tabs {
  height: 50px;
}

@media (max-width: 60em) {
  .btn {
    margin: 2%;
    display: grid;
    gap: 1em;
    grid-template-columns: repeat(1, 1fr);
    padding: 1%;
    font-size: 1em;
  }

  .registerbtn {
    margin: 2%;
    display: grid;
    gap: 1em;
    grid-template-columns: repeat(1, 1fr);
    padding: 1%;
    font-size: 1em;
  }

  h2 {
    font-size: 1.5em;
    font-weight: 600;
    line-height: 20px;

    margin-left: 3%;
  }

  body {
    height: 150vh;
  }
}
</style>
