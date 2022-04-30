<template>
  <q-header bordered class="bg-warning text-black nav">
    <q-toolbar>
      <div class="lt-md">
        <q-btn dense flat round icon="menu" @click="toggleLeftDrawer" />
      </div>
      <q-toolbar-title class="title">
        <q-avatar class="logo">
          <img src="https://cdn.quasar.dev/logo-v2/svg/logo-mono-white.svg" />
        </q-avatar>
        Folioblocks
      </q-toolbar-title>
      <a class="gt-sm toolbar-items" href="/">Home</a>
      <a class="gt-sm toolbar-items">Team</a>
      <a class="login gt-sm toolbar-items" href="#/register">Login </a>
    </q-toolbar>

    <q-drawer
      v-model="leftDrawerOpen"
      dark
      overlay
      :width="200"
      :breakpoint="500"
    >
      <q-scroll-area class="fit">
        <q-list padding class="menu-list">
          <q-item clickable v-ripple>
            <q-item-section avatar>
              <q-icon name="home" />
            </q-item-section>

            <q-item-section> Home </q-item-section>
          </q-item>

          <q-item clickable v-ripple>
            <q-item-section avatar>
              <q-icon name="people" />
            </q-item-section>

            <q-item-section> Team </q-item-section>
          </q-item>

          <q-item clickable v-ripple to="/login">
            <q-item-section avatar>
              <q-icon name="login" />
            </q-item-section>

            <q-item-section> Login </q-item-section>
          </q-item>
        </q-list>
      </q-scroll-area>
    </q-drawer>
  </q-header>

  <div class="main">
    <div class="intro">
      <div class="container text-white">
        <p class="mb-3">Get a trully skilled workers with Folioblocks!</p>
        <p class="mb-4">
          Tired of the tedious process of validating the credentials of workers?
          Blockchain can help you with that and with us!
        </p>
        <div class="btn">
          <q-btn
            class="loginbtn"
            outline
            color="primary"
            label="Login"
            to="/register"
          />
          <q-btn
            class="registerbtn"
            outline
            color="primary"
            label="Register"
            to="/register"
          />
        </div>
      </div>
    </div>
  </div>

  <div class="info">
    <img class="img" src="\img.jpg" />
    <div>
      <h5>
        Design of an Immutable Credential Verification System using Blockchain
        Technology
      </h5>

      <ul>
        <li>
          Immutable credential verification system using blockchain technology.
        </li>
        <li>Provides secure location and platform fo validated credentials.</li>
        <li>Suitable for people looking for trustworthy employees.</li>
      </ul>
    </div>
    <img class="img" src="\img2.jpg" />

    <div>
      <h5>Distributed Ledger Technology</h5>
      <p class="info-txt">
        The certificates and credentials of employees registered in FolioBlocks
        are recorded and stored on the blockchain. Blockchain is a distributed
        ledger that guarantees the authenticity of the stored credentials.
      </p>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref } from 'vue';

export default defineComponent({
  name: 'PageIndex',
  components: {},

  setup() {
    const leftDrawerOpen = ref(false);

    return {
      leftDrawerOpen,
      toggleLeftDrawer() {
        leftDrawerOpen.value = !leftDrawerOpen.value;
      },
    };
  },
});
</script>

<style scoped>
.main {
  background-image: url('~assets/pagebackground.png');
  background-repeat: no-repeat;
  background-size: cover;
  height: 100vh;
}

.intro {
  background-color: rgba(0, 0, 0, 0.555);
  height: 100vh;
}

.mb-3 {
  padding-top: 15%;
  text-align: center;
  font-family: 'Poppins';
  font-size: 3.5em;
}

.mb-4 {
  text-align: center;
  font-family: 'Poppins';
  font-size: 1.5em;
}

.btn {
  width: 250px;
  margin-left: auto;
  margin-right: auto;
  margin-top: 2%;
}
.loginbtn {
  font-size: 1.2em;
  margin-top: 2%;
}

.registerbtn {
  font-size: 1.2em;
  margin-top: 2%;
  margin-left: 24%;
}

h4 {
  font-size: 3.5em;
  width: auto;
  line-height: normal;
  font-weight: 800;
  margin-top: 200px;
  letter-spacing: 10px;
}

p {
  width: auto;
  font-size: 1.5em;
  font-weight: 500;
  text-align: justify;
  word-spacing: 5px;
}

.info {
  display: grid;
  gap: 5rem;
  grid-template-columns: repeat(2, 1fr);
  margin-top: 200px;
  margin-left: 6%;
  margin-right: 6%;
}

.img {
  width: 100%;
  height: 90%;
  border-radius: 5px;
  box-shadow: 0 0 30px #3d3d3d;
}

h5 {
  margin-top: 10%;
  font-weight: 700;
  font-family: 'Poppins';
}

ul,
.info-txt {
  font-family: 'Poppins';
  font-weight: 400;
  font-size: 1.5em;
  margin: 50px;
  text-align: justify;
}

.title {
  color: black;
  font-size: 2em;
  margin-left: 5%;
}

.logo {
  margin-right: 20px;
}

.toolbar-items {
  color: black;
  font-size: 1em;
  margin-left: 2%;
  margin-top: 20px;
  padding: 10px;
  font-family: 'Poppins';
  font-weight: 400;
}

.login {
  margin-right: 3%;
}

@media (max-width: 60em) {
  h4 {
    font-size: 1.5rem;
    letter-spacing: normal;
  }
  h5 {
    font-size: 1.5em;
    margin-top: 10%;
    font-weight: 700;
    font-family: 'Poppins';
  }
  p {
    font-size: 0.8rem;
    word-spacing: normal;
  }

  .title {
    font-size: 1rem;
  }

  .info {
    display: grid;
    gap: 5rem;
    grid-template-columns: repeat(1, 1fr);
    margin-top: 200px;
    margin-left: 6%;
    margin-right: 6%;
  }
  .mb-3 {
    padding-top: 30%;
    text-align: center;
    font-family: 'Poppins';
    font-size: 2em;
  }

  .mb-4 {
    text-align: center;
    font-family: 'Poppins';
    font-size: 1em;
  }
  .info-txt {
    font-family: 'Poppins';
    font-weight: 400;
    font-size: 1.3em;
    margin: 50px;
    text-align: justify;
  }
}
</style>
