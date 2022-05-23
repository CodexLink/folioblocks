<template>
  <q-layout view="hHh Lpr lff">
    <q-header elevated class="bg-cyan text-white">
      <q-toolbar>
        <q-btn
          dense
          flat
          round
          v-if="!containsNoAuth"
          icon="menu"
          @click="toggleLeftDrawer"
        />

        <q-toolbar-title class="webtitle">
          <strong>FolioBlocks</strong>
        </q-toolbar-title>

        <q-btn
          flat
          rounded
          ripple
          color="white"
          icon="people"
          label="Addresses"
          v-if="onExplorer"
          to="/explorer/addresses"
        />

        <q-btn
          flat
          rounded
          ripple
          color="white"
          icon="home"
          label="Home"
          to="/"
        />
        <q-btn
          flat
          rounded
          ripple
          v-if="containsNoAuth"
          color="white"
          icon="login"
          label="Login"
          to="/entry/login"
        />

        <q-btn
          class="exit"
          flat
          rounded
          ripple
          v-if="!containsNoAuth"
          color="white"
          icon="logout"
          label="Logout"
          v-on:click="logoutSession"
        />
        <q-btn
          flat
          rounded
          ripple
          v-if="containsNoAuth"
          color="white"
          icon="mdi-account-plus"
          label="Register"
          to="/entry/register"
        />
      </q-toolbar>
    </q-header>

    <q-drawer
      v-if="!containsNoAuth"
      v-model="leftDrawerOpen"
      :width="300"
      :breakpoint="2000"
    >
      <q-scroll-area
        style="
          height: calc(100% - 200px);
          margin-top: 200px;
          border-right: 1px solid #ddd;
        "
      >
        <q-list padding>
          <q-item-label header>Main Menu</q-item-label>
          <q-item
            clickable
            v-ripple
            to="/dashboard"
            :active="activeLink === 'dashboard'"
            @click="activeLink = 'dashboard'"
            active-class="active-state"
          >
            <q-item-section avatar>
              <q-icon name="mdi-view-dashboard" />
            </q-item-section>

            <q-item-section> Dashboard </q-item-section>
          </q-item>

          <q-item
            clickable
            v-ripple
            round
            to="/explorer"
            :active="activeLink === 'explorer'"
            @click="activeLink = 'explorer'"
            active-class="active-state"
          >
            <q-item-section avatar>
              <q-icon name="mdi-checkbox-multiple-blank" />
            </q-item-section>

            <q-item-section> Explorer </q-item-section>
          </q-item>

          <div v-if="role === 'Organization Dashboard User'">
            <q-separator spaced />
            <q-item-label header>Organization Options</q-item-label>

            <q-item
              clickable
              v-ripple
              to="/org/insert/new"
              :active="activeLink === 'new-students'"
              @click="activeLink = 'new-students'"
              active-class="active-state"
            >
              <q-item-section avatar>
                <q-icon name="mdi-account-multiple-plus" />
              </q-item-section>

              <q-item-section> Generate Student Users </q-item-section>
            </q-item>
            <q-item
              clickable
              v-ripple
              to="/org/insert/standby"
              :active="activeLink === 'new-credentials'"
              @click="activeLink = 'new-credentials'"
              active-class="active-state"
            >
              <q-item-section avatar>
                <q-icon name="mdi-file-account" />
              </q-item-section>

              <q-item-section> Refer Credentials </q-item-section>
            </q-item>
          </div>

          <div v-if="role === 'Student Dashboard User'">
            <q-separator spaced />
            <q-item-label header>Student Options</q-item-label>

            <q-item
              clickable
              v-ripple
              to="/portfolio"
              :active="activeLink === 'portfolio'"
              @click="activeLink = 'portfolio'"
              active-class="active-state"
            >
              <q-item-section avatar>
                <q-icon name="mdi-file-account" />
              </q-item-section>

              <q-item-section> Portfolio </q-item-section>
            </q-item>
          </div>
        </q-list>
      </q-scroll-area>

      <q-img
        class="absolute-top"
        src="https://picsum.photos/id/10/2500/1667"
        style="height: 200px; width: 300px"
      >
        <div class="absolute-bottom bg-transparent">
          <q-avatar size="56px" class="q-mb-sm">
            <img alt="User Avatar" :src="html_user_avatar" />
          </q-avatar>
          <div class="text-weight-bold">{{ user }}</div>
          <div>{{ role }}</div>
        </div>
      </q-img>
    </q-drawer>

    <q-page-container>
      <router-view />
    </q-page-container>
  </q-layout>
</template>

<script>
import { defineComponent, ref } from 'vue';
import { useQuasar } from 'quasar';
import axios from 'axios';
import { MASTER_NODE_BACKEND_URL } from '/utils/utils.js';
import { useRoute, useRouter } from 'vue-router';

export default defineComponent({
  name: 'Dashboard',
  components: {},

  data() {
    return {
      user: ref('0x000000000000000'),
      html_user_avatar: ref(''),
      role: ref('Unidentified'),
      onExplorer: ref(false),
    };
  },
  setup() {
    const $q = useQuasar();
    const $router = useRouter();
    const $route = useRoute();
    const leftDrawerOpen = ref(false);
    const containsNoAuth =
      $q.localStorage.getItem('token') === null ? true : false;
    const isMaster =
      $q.localStorage.getItem('role') === 'Administrator' ? true : false;

    return {
      activeLink: ref(''),
      containsNoAuth,
      isMaster,
      leftDrawerOpen,
      toggleLeftDrawer() {
        leftDrawerOpen.value = !leftDrawerOpen.value;
      },
    };
  },
  mounted() {
    // ! Call the function from checking the path and the authentication.
    if (!this.containsNoAuth && !this.isMaster) {
      axios
        .get(`${MASTER_NODE_BACKEND_URL}/dashboard`, {
          headers: {
            'X-Token': this.$q.localStorage.getItem('token'),
          },
        })
        .then((response) => {
          this.user = `${response.data.first_name} ${response.data.last_name}`;
          this.html_user_avatar = `https://ui-avatars.com/api/?name=${response.data.first_name}+${response.data.last_name}`;
          this.role = response.data.role;

          this.checkPathAndAuth();
        })
        .catch((e) => {
          // * Go back to home page.
          this.$router.push({ path: '/' });

          const responseDetail =
            e.response.data === undefined
              ? `${e.message}. Server may be unvailable. Please try again later.`
              : e.response.data.detail;

          this.$q.notify({
            color: 'red',
            position: 'top',
            message: `There was an error when accessing the page. Info: ${responseDetail}`,
            timeout: 5000,
            progress: true,
            icon: 'mdi-cancel',
          });

          // * Clear the session.
          this.$q.localStorage.clear();
        });
    } else if (!this.containsNoAuth && this.isMaster) {
      this.user = '<No Name>';
      this.html_user_avatar = 'https://ui-avatars.com/api/?name=??';
      this.role = this.$q.localStorage.getItem('role');
    } else {
      this.checkPathAndAuth();
    }
  },
  methods: {
    async logoutSession() {
      if (this.containsNoAuth) return;

      await axios.post(
        `${MASTER_NODE_BACKEND_URL}/entity/logout`,
        {
          /* ... data */
        },
        {
          headers: {
            'X-Token': this.$q.localStorage.getItem('token'),
          },
        }
      );

      this.$q.localStorage.clear();
      await this.$router.push({ path: '/' });

      this.$q.notify({
        color: 'green',
        position: 'top',
        message: 'Logout successful! See you next time!',
        timeout: 5000,
        progress: true,
        icon: 'mdi-account-check',
      });
    },
    checkPathAndAuth() {
      if (
        // - Conditions for prohibiting non-student users from accessing respective pages, except for portfolio.
        (this.$route.path.includes('/dashboard') && this.containsNoAuth) ||
        // ! Condition for prohibiting students accessing `/org` endpoints.
        (this.$route.path.includes('/org') &&
          this.role !== 'Organization Dashboard User') ||
        // ! Condition for prohibiting organization members attempting to access portfolio endpoint with no path parameter.
        (this.$route.path.includes('/portfolio') &&
          this.$route.query.address === '' &&
          this.role === 'Organization Dashboard User') ||
        // ! Condition for prohibiting student users from accessing portfolio endpoint with path parameter, which may have the intention of checking other portfolio.
        (this.$route.path.includes('/portfolio') &&
          this.$route.query.address !== undefined &&
          this.role === 'Student Dashboard User') ||
        // ! Condition for prohibiting anonymous users from accessing the portfolio when its `address` query were invalid.
        (this.$route.path.includes('/portfolio') &&
          this.$route.query.address === undefined &&
          (this.role === 'Unidentified' || this.role === 'Administrator'))
      ) {
        void this.$router.push({
          path: this.containsNoAuth ? '/' : '/dashboard',
        });

        // * Notify the user regarding this issue.
        this.$q.notify({
          color: 'red',
          position: 'top',
          message: 'You are unauthorized to navigate the requested page.',
          timeout: 5000,
          progress: true,
          icon: 'mdi-cancel',
        });
      }

      // * Check if we are in explorer.
      this.onExplorer = this.$route.path.includes('/explorer') ? true : false;
    },
  },
  updated() {
    this.checkPathAndAuth();

    // * Ensure that other actions for the `org/insert/:action` endpoint is also handled.
    if (this.$route.path.includes('/org/insert'))
      this.activeLink = 'new-credentials';
  },
});
</script>

<style scoped>
/* Navigation bar*/

.active-state {
  color: white;
  background: #f44336;
}

.q-layout {
  background-color: rgb(255, 255, 255);
}

h2 {
  font-size: 2.5em;
  font-weight: 500;
  text-align: center;
  margin-bottom: 1%;
}

h4 {
  font-size: 1.4em;
}

p {
  font-size: 1.3em;
}

img {
  height: 50px;
  width: 50px;
  float: left;
  margin: 5%;
}

.toolbar-items {
  font-size: 0.8em;

  margin-left: 5%;
}

.webtitle {
  margin-left: 1%;
}

.logo {
  margin-right: 1.5%;
  margin-left: 0.5%;
  margin-top: 0.5%;
  margin-bottom: 0.5%;
}

.menu-list .q-item {
  border-radius: 0 32px 32px 0;
}
</style>
