<template>
  <q-layout view="hHh Lpr lff">
    <q-header elevated class="bg-positive text-black">
      <q-toolbar>
        <q-btn dense flat round icon="menu" @click="toggleLeftDrawer" />

        <q-toolbar-title class="webtitle">
          <q-avatar class="logo">
            <img src="https://cdn.quasar.dev/logo-v2/svg/logo-mono-white.svg" />
          </q-avatar>
          Folioblocks
          <a class="toolbar-items gt-sm">Home</a>
          <a class="toolbar-items gt-sm">Team</a>
          <a class="toolbar-items gt-sm">Home</a>
          <a class="toolbar-items gt-sm">Home</a>
        </q-toolbar-title>
        <q-btn
          class="exit gt-sm"
          flat
          round
          color="black"
          icon="logout"
          to="/"
        />
      </q-toolbar>
    </q-header>

    <q-drawer dark v-model="leftDrawerOpen" :width="300" :breakpoint="600">
      <q-scroll-area
        style="
          height: calc(100% - 150px);
          margin-top: 150px;
          border-right: 1px solid #ddd;
        "
      >
        <q-list padding class="menu-list">
          <q-item clickable v-ripple to="/dashboard">
            <q-item-section avatar>
              <q-icon name="home" />
            </q-item-section>

            <q-item-section> Home </q-item-section>
          </q-item>

          <q-item
            clickable
            v-ripple
            to="/insert"
            v-if="role === !'institution'"
            class="hidden"
          >
            <q-item-section avatar>
              <q-icon name="upload" />
            </q-item-section>

            <q-item-section> Insert </q-item-section>
          </q-item>

          <q-item
            clickable
            v-ripple
            to="/insert"
            v-else-if="role === 'institution'"
          >
            <q-item-section avatar>
              <q-icon name="upload" />
            </q-item-section>

            <q-item-section> Insert </q-item-section>
          </q-item>

          <q-item clickable v-ripple to="/explorerdashboard">
            <q-item-section avatar>
              <q-icon name="dashboard" />
            </q-item-section>

            <q-item-section> Explorer </q-item-section>
          </q-item>

          <q-item class="lt-md" clickable v-ripple to="/explorerdashboard">
            <q-item-section avatar>
              <q-icon name="dashboard" />
            </q-item-section>

            <q-item-section> Home </q-item-section>
          </q-item>

          <q-item class="lt-md" clickable v-ripple to="/explorerdashboard">
            <q-item-section avatar>
              <q-icon name="dashboard" />
            </q-item-section>

            <q-item-section> Home </q-item-section>
          </q-item>

          <q-item class="lt-md" clickable v-ripple to="/explorerdashboard">
            <q-item-section avatar>
              <q-icon name="dashboard" />
            </q-item-section>

            <q-item-section> Home </q-item-section>
          </q-item>

          <q-item class="lt-md" clickable v-ripple to="/">
            <q-item-section avatar>
              <q-icon name="logout" />
            </q-item-section>

            <q-item-section> Logout </q-item-section>
          </q-item>
        </q-list>
      </q-scroll-area>
      <q-img
        class="absolute-top"
        src="https://cdn.quasar.dev/img/material.png"
        style="height: 150px"
      >
        <div class="absolute-bottom bg-transparent">
          <q-avatar size="56px" class="q-mb-sm">
            <img src="https://cdn.quasar.dev/img/boy-avatar.png" />
          </q-avatar>
          <div class="text-weight-bold">{{ user }}</div>
          <div>{{ alias }}</div>
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

export default defineComponent({
  name: 'Dashboard',
  components: {},

  data() {
    return {
      user: '0x593sdx107c',
      alias: 'Ronan',
      role: 'institution',
    };
  },
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
/* Navigation bar*/
.q-layout {
  background-color: rgb(255, 255, 255);
}

h2 {
  font-family: 'Poppins';
  font-size: 2.5em;
  font-weight: 500;
  text-align: center;
  margin-bottom: 1%;
}

h4 {
  font-family: 'Poppins';
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
  font-family: 'Poppins';
  margin-left: 5%;
}

.webtitle {
  font-family: 'Poppins';
  margin-left: 1%;
}

.logo {
  margin-right: 1.5%;
  margin: 0.5%;
}

.menu-list .q-item {
  border-radius: 0 32px 32px 0;
}
</style>
