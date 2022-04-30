<template>
  <img class="background" src="~assets/pagebackground.png" />
  <body>
    <RegisterContainer>
      <q-card>
        <q-tabs
          v-model="tab"
          dense
          class="text-grey tabs"
          active-color="black"
          indicator-color="black"
          align="justify"
          narrow-indicator
        >
          <q-tab name="login" label="Login" />
          <q-tab name="register" label="Register" />
        </q-tabs>

        <q-separator />

        <q-tab-panels v-model="tab" animated>
          <q-tab-panel name="login">
            <q-form @submit.prevent="submitForm">
              <div>
                <h2>Hello and Welcome!</h2>
                <h4>Please provide your credentials to get started.</h4>
              </div>
              <q-input
                class="user"
                color="secondary"
                outlined
                v-model="login.username"
                label="Username"
              />

              <q-input
                class="password"
                outlined
                color="secondary"
                v-model="login.password"
                label="Password"
                type="password"
              />

              <q-checkbox
                class="qcheck"
                v-model="val"
                label="Remember Me"
                color="secondary"
              />
              <div class="btn">
                <q-btn
                  class="login"
                  rounded
                  color="secondary"
                  label="Back"
                  to="/"
                />

                <q-btn
                  class="login"
                  rounded
                  color="secondary"
                  label="Login"
                  type="submit"
                />
              </div>
              <q-separator class="gt-sm q-mb-sm" color="warning" />
              <p>
                Need an Account?<a @click="tab = 'register'" href="#/register"
                  >Sign Up</a
                >
              </p>
            </q-form>
          </q-tab-panel>

          <q-tab-panel name="register">
            <q-form>
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

              <q-checkbox
                class="qcheck"
                v-model="valterms"
                label="Terms and Conditions"
                color="secondary"
              />

              <div class="registerbtn">
                <q-btn
                  class="backbtn"
                  rounded
                  color="secondary"
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
              <q-separator class="gt-sm q-mb-sm" color="warning" />
              <p>
                Did you just got here with an account?<a
                  @click="tab = 'login'"
                  href="#/register"
                  >Login</a
                >
              </p>
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

export default defineComponent({
  name: 'Register',
  components: { RegisterContainer },
  data() {
    return {
      FirstName: ref(''),
      LastName: ref(''),
      Username: ref(''),
      email: ref(''),
      username: ref(''),
      password: ref(''),
      confirm: ref(''),
      code: ref(''),
      associationname: ref(''),
      associationaddress: ref(''),
      associationdescription: ref(''),

      login: {
        username: ref(''),
        password: ref(''),
      },
    };
  },

  setup() {
    return {
      tab: ref('login'),
      model: ref(null),
      options: ['Type', 'Type'],
      val: ref(false),
      valterms: ref(false),
      date: ref(''),
    };
  },
  methods: {
    submitForm() {
      if (!this.login.username || !this.login.password) {
        console.log('error');
      } else if (this.login.password.length < 6) {
        console.log('error');
      } else {
        void this.$router.push('/dashboard');
      }
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
