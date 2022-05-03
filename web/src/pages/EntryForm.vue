<template>
  <img class="background" src="~assets/pagebackground.png" />
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
            <q-form @submit.prevent="submitLoginRequest">
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
                v-model="login.username"
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
                v-model="login.password"
                label="Password"
                :type="show_password ? 'password' : 'text'"
                :rules="[
                  (val) => (val && val.length > 0) || 'This is required.',
                ]"
              >
                <template v-slot:append>
                  <q-icon
                    :name="show_password ? 'visibility_off' : 'visibility'"
                    class="cursor-pointer"
                    @click="show_password = !show_password"
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
            <q-form>
              <div>
                <h2>Thank you for taking interest!</h2>
                <h4>
                  Fill the fields below. Remember, get the authentication code
                  from your supervisor for you to proceed your regisration.
                </h4>
              </div>
              <div class="row">
                <q-input
                  class="double"
                  outlined
                  color="secondary"
                  v-model="FirstName"
                  label="First Name"
                />
                <q-input
                  class="double"
                  outlined
                  color="secondary"
                  v-model="LastName"
                  label="Last Name"
                />
              </div>
              <div class="row">
                <q-input
                  class="username"
                  outlined
                  color="secondary"
                  v-model="Username"
                  label="Username"
                />
                <q-input
                  class="email"
                  outlined
                  color="secondary"
                  v-model="email"
                  label="E-mail"
                />
              </div>
              <div class="row">
                <q-input
                  class="username"
                  outlined
                  color="secondary"
                  v-model="associationname"
                  label="Association Name"
                />

                <q-input
                  class="email"
                  outlined
                  color="secondary"
                  v-model="associationaddress"
                  label="Association Address"
                />
              </div>

              <div class="row">
                <q-select
                  class="double"
                  color="secondary"
                  outlined
                  v-model="model"
                  :options="options"
                  label="Association Type"
                />

                <q-input
                  class="double"
                  outlined
                  color="secondary"
                  v-model="associationdescription"
                  label="Association Description"
                />
              </div>
              <q-input
                class="data"
                v-model="date"
                filled
                type="date"
                prefix="Association Founded"
              />

              <div class="row">
                <q-input
                  class="double"
                  outlined
                  color="secondary"
                  v-model="password"
                  type="password"
                  label="Password"
                />
                <q-input
                  class="double"
                  outlined
                  color="secondary"
                  v-model="confirm"
                  type="password"
                  label="Confirm Password"
                />
              </div>
              <q-input
                class="data"
                outlined
                color="secondary"
                v-model="code"
                type="password"
                label="Authentication Code"
              />

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
import { resolvedNodeAPIURL } from '/utils/utils.js';
export default defineComponent({
  name: 'EntryForm',
  components: { RegisterContainer },
  data() {
    return {
      firstName: ref(null),
      lastName: ref(null),
      username: ref(null),
      email: ref(null),
      password: ref(null),
      show_password: ref(true),
      confirm: ref(null),
      code: ref(null),
      associationname: ref(null),
      associationaddress: ref(null),
      associationdescription: ref(null),
      isProcessing: ref(false),

      login: {
        username: ref(null),
        password: ref(null),
      },
    };
  },

  setup() {
    const $route = useRoute();
    const $router = useRouter();
    const $q = useQuasar();

    return {
      tab: ref($route.params.action),
      model: ref(null),
      options: ['Type', 'Type'],
      val: ref(false),
      valterms: ref(false),
      date: ref(null),
    };
  },
  methods: {
    submitLoginRequest() {
      this.isProcessing = true;
      setTimeout(() => {
        console.log(1);
      }, 15000);
      axios
        .post(`http://${resolvedNodeAPIURL}/entity/login`, {
          username: this.login.username,
          password: this.login.password,
        })
        .then((response) => {
          try {
            // * Check condition wherein we prohibit other `ARCHIVAL_MINER_NODES` and `MASTER_NODES` from logging in since they have nothing to do with the dashboard.
            if (
              response.data.user_role == 'Master Node User' ||
              response.data.user_role == 'Archival Miner Node User'
            ) {
              this.$q.notify({
                color: 'negative',
                position: 'top',
                message:
                  'Node-related account is not allowed to use the dashboard. Your account can be used in logging at folioblocks-node-cli.',
                timeout: 10000,
                progress: true,
                icon: 'mdi-account-cancel-outline',
              });

              // * Logout the token gracefully, without handling the error since we didn't do anything regarding storing something from the localStorage..
              axios.post(`http://${resolvedNodeAPIURL}/entity/logout`, {
                headers: {
                  'X-Token': response.data.jwt_token,
                },
              });
              this.isProcessing = false;
            } else {
              // * Clear out the local storage first.
              this.$q.localStorage.clear();

              // * Then set the current token and the address.
              this.$q.localStorage.set('token', response.data.jwt_token);
              this.$q.localStorage.set('address', response.data.user_address);

              // * Some some toast.
              this.$q.notify({
                color: 'green',
                position: 'top',
                message: 'Login successful!',
                timeout: 10000,
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
            timeout: 10000,
            progress: true,
            icon: 'report_problem',
          });
          this.isProcessing = false;
        });
    },
  },
});
</script>

<style scoped>
body {
  background-color: rgba(0, 0, 0, 0.692);
  height: 100vh;
  padding-top: 4%;
}

.background {
  position: fixed;
  z-index: -1;
  width: 100%;
  height: 100%;
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
  font-family: 'Poppins';
  margin-left: 3%;
}

h4 {
  font-size: 1em;
  line-height: 20px;
  font-family: 'Poppins';
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
  height: 60px;
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
    font-family: 'Poppins';
    margin-left: 3%;
  }

  body {
    height: 150vh;
  }
}
</style>
