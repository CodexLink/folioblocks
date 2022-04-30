<template>
  <div class="main">
    <q-card class="my-card">
      <q-card-section class="row q-pt-xl q-px-xl q-ma-md">
        <div class="text-h6 text-weight-bold">Settings</div>
        <q-space></q-space>
        <q-btn v-close-popup flat dense round color="black" icon="close" />
      </q-card-section>

      <q-card-section>
        <div class="q-pl-xl q-mr-xl text-h7 text-justify">
          Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do
          eiusmod tempor incididunt ut labore et dolore magna aliqua. Lorem
          ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod
          tempor incididunt ut labore et dolore magna aliqua. Lorem ipsum dolor
          sit amet, consectetur adipiscing elit, sed do eiusmod tempor
          incididunt ut labore et dolore magna aliqua.
        </div>
      </q-card-section>

      <q-card-section class="row q-ml-xl">
        <div class="q-pt-xl q-pl-xl row">
          <q-avatar
            square
            size="110px"
            font-size="82px"
            color="teal"
            text-color="white"
            icon="directions"
          />
          <div class="text-h6 text-weight-bold q-mx-xl q-pt-xl q-pr-xl">
            Avatar
          </div>

          <q-file
            class="q-mt-xl"
            v-model="file"
            color="secondary"
            label="Change Avatar"
            outlined
          />
        </div>
      </q-card-section>

      <q-card-section class="row q-ml-xl">
        <div class="q-pt-xl q-pl-xl row">
          <div style="width: 40%; margin-right: 13%">
            <p class="text-h6 text-weight-bold">Description</p>
            <p class="text-justify text-h7">
              Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do
              eiusmod tempor incididunt ut labore et dolore magna aliqua. Lorem
              ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod
              tempor incididunt ut l
            </p>
          </div>
          <q-input
            v-model="description"
            outlined
            color="secondary"
            type="textarea"
            label="Description..."
          />
        </div>
      </q-card-section>

      <q-card-section class="row q-ml-xl">
        <div class="q-pt-xl q-pl-xl row">
          <div style="width: 40%; margin-right: 13%">
            <p class="text-h5 text-weight-bold">Skills</p>
            <p class="text-justify text-h7">
              Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do
              eiusmod tempor incididunt ut labore et dolore magna aliqua. Lorem
              ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod
              tempor incididunt ut l
            </p>
          </div>
          <q-input
            v-model="skills"
            outlined
            color="secondary"
            type="textarea"
            label="Description..."
          />
        </div>
      </q-card-section>

      <q-card-actions align="right">
        <q-btn
          v-close-popup
          outline
          color="black"
          label="Apply"
          class="q-ma-md q-mr-xl"
          style="width: 30%"
        />
      </q-card-actions>
    </q-card>
  </div>
</template>

<script>
import { ref } from 'vue';
export default {
  data() {
    return {
      description: ref(''),
      skills: ref(''),
      file: ref(''),
    };
  },
};
</script>

<style scoped>
* {
  font-family: 'Poppins';
}
.btn {
  margin-left: 100px;
}

.main {
  background-color: #a7eaff;
  padding: 1%;
  margin: auto;
  margin-top: 1%;
  margin-bottom: 1%;
  width: 70%;
  border-style: solid;
  border-radius: 5px;
  box-shadow: 0 0 20px #999999;
}

.my-card {
  width: 75%;
  height: 50%;
  margin: auto;
  margin-bottom: 1%;
  margin-top: 1%;
}

@media (max-width: 90em) {
  .my-card {
    width: 100%;
  }
}

@media (max-width: 60em) {
  .main {
    background-color: #a7eaff;
    padding: 1%;
    margin-top: 1%;
    margin-bottom: 1%;
    width: 100%;
    border-style: solid;
    border-radius: 5px;
    box-shadow: 0 0 20px #999999;
  }
}
</style>
>
