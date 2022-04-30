<template>
  <div class="header text-h6">
    <div class="avatar">
      <q-avatar class="usericon" icon="account_circle" />
    </div>

    <p class="q-pt-md">
      <span class="text-weight-bold q-ma-sm q-mb-sm q-pt-md q-ml-lg">
        Name:</span
      >
      {{ role }}

      <span class="text-weight-bold q-ma-sm q-mb-sm q-ml-xl"> Identity:</span>
      {{ role }}
    </p>
    <p>
      <span class="text-weight-bold q-ma-sm q-mb-sm q-ml-lg"> Email:</span
      >{{ role }}
    </p>

    <p>
      <span class="text-weight-bold q-ma-sm q-mb-sm q-ml-lg">
        Institution:</span
      >
      {{ role }}
    </p>
    <p>
      <span class="text-weight-bold q-ma-sm q-mb-sm q-ml-lg"> Course:</span>
      {{ role }}

      <span class="text-weight-bold q-ma-sm q-mb-sm q-ml-xl"> Year Level:</span>
      {{ role }}

      <span class="text-weight-bold q-ma-sm q-mb-sm q-ml-xl">
        Prefer Role:</span
      >
      {{ role }}
    </p>
    <p>
      <span class="text-weight-bold q-ma-sm q-mb-sm q-ml-lg">
        Personal Skills:</span
      >
      {{ role }}
    </p>
    <p>
      <span class="text-weight-bold q-ma-sm q-ml-lg"> Description:</span>
      {{ description }}
    </p>

    <div class="text-right q-pr-xl">
      <q-btn outline color="black" label="Log History" @click="card = true" />
    </div>
  </div>

  <q-dialog v-model="card" persistent>
    <q-card class="my-card">
      <div>
        <h2 class="text-h4 text-weight-medium q-ma-md">Logs</h2>
        <p class="text-h7 q-ma-md">
          Here are the recent logs from this user's portfolio.
        </p>
      </div>
      <q-card-section>
        <div class="log">
          <q-scroll-area style="height: 100%; max-width: 100%">
            <q-item
              class="logdata"
              v-for="list in lists"
              :key="list.id"
              clickable
              v-ripple
            >
              <q-item-section class="text-h6">
                <q-item-label class="q-mb-sm">
                  <span class="text-weight-bold q-ma-sm q-mb-sm"> Hash:</span
                  >{{ list.title }}</q-item-label
                >

                <q-item-label class="q-mb-sm">
                  <span class="text-weight-bold q-ma-sm q-mb-sm"> From:</span
                  >{{ list.title }}</q-item-label
                >
              </q-item-section>
              <q-item-section top side>
                <div class="text-grey-8 q-gutter-md">
                  <q-badge outline color="black" label="Type" />
                </div>
              </q-item-section>
            </q-item>
          </q-scroll-area>
        </div>
      </q-card-section>

      <q-card-actions align="right">
        <q-btn
          v-close-popup
          outline
          color="secondary"
          label="Close"
          class="q-mr-md"
        />
      </q-card-actions>
    </q-card>
  </q-dialog>

  <div class="row">
    <div class="logs">
      <q-scroll-area style="height: 100%; max-width: 100%">
        <q-item
          v-for="list in lists"
          :key="list.id"
          clickable
          class="logdata"
          @click="
            Clicked(list);
            log = true;
          "
        >
          <q-item-section class="text-h6">
            <q-item-label
              ><span class="text-weight-bold q-ma-md q-mb-sm"> Name:</span
              >{{ list.name }}</q-item-label
            >
            <q-item-label>
              <span class="text-weight-bold q-ma-md q-mb-sm"> Role:</span
              >{{ list.role }}</q-item-label
            >
            <q-item-label class="q-ml-md">
              <span class="text-weight-bold text-justify q-mb-sm q-mr-md">
                Description:</span
              >{{ list.description }}</q-item-label
            >
            <q-item-label>
              <span class="text-weight-bold q-ma-md q-mb-sm">
                Validated By:</span
              >{{ list.validatedby }}</q-item-label
            >
            <q-item-section side>
              <q-btn
                outline
                color="black"
                label="View More"
                class="q-mt-md view"
                @click="
                  Clicked(list);
                  log = true;
                "
              />
            </q-item-section>
          </q-item-section>
          <q-item-section top side>
            <div class="text-grey-8">
              <q-badge outline color="black" label="Type" />
            </div>
          </q-item-section>
        </q-item>
      </q-scroll-area>
    </div>

    <div class="logs">
      <q-scroll-area style="height: 100%; max-width: 100%">
        <q-item v-for="list in lists" :key="list.id" clickable class="logdata">
          <q-item-section class="text-h6">
            <q-item-label class="text-bold q-mb-sm">
              <span class="text-weight-bold q-ma-sm q-mb-sm"> Title:</span
              >{{ list.title }}</q-item-label
            >
            <q-item-label class="q-ml-sm text-justify q-mb-sm q-ml-lg">
              <span class="text-weight-bold q-mb-sm q-mr-sm"> Description:</span
              >{{ list.descriptioninfo }}</q-item-label
            >
            <q-item-label class="q-ml-md q-mb-sm">
              <span class="text-weight-bold q-ma-sm q-mb-sm q-ml-sm">
                Timestamp:</span
              >{{ list.timestamp
              }}<span class="text-weight-bold q-ma-sm q-mb-sm q-ml-xl">
                Inserted By:</span
              >{{ list.insertedby }}</q-item-label
            >
          </q-item-section>
        </q-item>
      </q-scroll-area>
    </div>
  </div>

  <q-dialog v-model="log" class="modal" persistent>
    <q-card class="my-card-log">
      <q-card-section>
        <div class="log">
          <q-item>
            <q-item-section class="text-h6">
              <q-item-label class="q-mb-md"
                ><span class="text-weight-bold q-ma-sm q-mb-sm"> Name:</span
                >{{ nameinfo }}</q-item-label
              >
              <q-item-label class="q-mb-md">
                <span class="text-weight-bold q-ma-sm q-mb-sm"> Address:</span
                >{{ addressinfo }}</q-item-label
              >
              <q-item-label class="q-mb-md">
                <span class="text-weight-bold q-ma-sm q-mb-sm"> Role:</span
                >{{ roleinfo }}</q-item-label
              >
              <q-item-label class="q-ml-sm q-mb-md">
                <span class="text-weight-bold text-justify q-mb-sm q-mr-sm">
                  Description:</span
                >{{ descriptioninfomodal }}</q-item-label
              >
              <q-item-label class="q-mb-md">
                <span class="text-weight-bold q-ma-sm q-mb-sm">
                  Validated By:</span
                >{{ validatedbyinfo }}</q-item-label
              >
              <q-item-label class="q-mb-md">
                <span class="text-weight-bold q-ma-sm q-mb-sm"> File:</span
                >{{ fileinfo }}
                <q-btn outline color="black" label="View" class="q-mr-md"
              /></q-item-label>
              <q-item-label class="q-mb-md">
                <span class="text-weight-bold q-ma-sm q-mb-sm">
                  Duration Start:</span
                >{{ durationstartinfo }}</q-item-label
              >
              <q-item-label class="q-mb-md">
                <span class="text-weight-bold q-ma-sm q-mb-sm">
                  Duration End:</span
                >{{ durationendinfo }}</q-item-label
              >
            </q-item-section>
          </q-item>
        </div>
      </q-card-section>

      <q-card-actions align="right">
        <q-btn
          v-close-popup
          outline
          color="secondary"
          label="Close"
          class="q-mr-md"
        />
      </q-card-actions>
    </q-card>
  </q-dialog>

  <q-page-sticky position="bottom-right" :offset="[18, 18]">
    <q-btn fab glossy icon="add" color="blue-10" @click="share = true" />
  </q-page-sticky>

  <q-dialog v-model="share" class="modal" persistent>
    <q-card style="width: 100%; height: 50%">
      <q-card-section class="row q-ma-md">
        <div class="text-h6 text-weight-bold">Share Settings</div>
        <q-space></q-space>
        <q-btn v-close-popup flat dense round color="black" icon="close" />
      </q-card-section>

      <div class="q-pa-md q-pl-xl q-mr-md text-h7 text-justify">
        Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod
        tempor incididunt ut labore et dolore magna aliqua.
      </div>

      <div>
        <q-item tag="label" v-ripple class="q-ml-xl q-mr-xl text-h6">
          <q-item-section>
            <q-item-label>Enable Sharing</q-item-label>
          </q-item-section>
          <q-item-section avatar>
            <q-toggle color="blue" v-model="sharing" />
          </q-item-section>
        </q-item>

        <q-item tag="label" v-ripple class="q-ml-xl q-mr-xl text-h6">
          <q-item-section>
            <q-item-label>Expose Email Info</q-item-label>
          </q-item-section>
          <q-item-section avatar>
            <q-toggle color="blue" v-model="exposeemail" />
          </q-item-section>
        </q-item>

        <q-item tag="label" v-ripple class="q-ml-xl q-mr-xl text-h6">
          <q-item-section>
            <q-item-label>Time-limit Sharing to 10 minutes</q-item-label>
          </q-item-section>
          <q-item-section avatar>
            <q-toggle color="blue" v-model="timelimit" />
          </q-item-section>
        </q-item>

        <q-item tag="label" v-ripple class="q-ml-xl q-mr-xl text-h6">
          <q-item-section>
            <q-item-label>Allow File View</q-item-label>
          </q-item-section>
          <q-item-section avatar>
            <q-toggle color="blue" v-model="allowfile" />
          </q-item-section>
        </q-item>
      </div>
    </q-card>
  </q-dialog>
</template>

<script>
import { defineComponent, ref } from 'vue';

export default defineComponent({
  data() {
    return {
      role: 'Role',
      nameinfo: '',
      addressinfo: '',
      roleinfo: '',
      descriptioninfomodal: '',
      validatedbyinfo: '',
      fileinfo: '',
      durationstartinfo: '',
      durationendinfo: '',

      lists: [
        {
          id: 1,
          name: 'Applicant 1',
          address: '0x7zd7a8ds6dsa',
          role: 'Role',
          description:
            'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. ',
          validatedby: 'validated',
          file: '',
          durationstart: '24/04/22',
          durationend: '30/04/22',
          title: 'Title',
          descriptioninfo:
            'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. ',
          timestamp: '24/04/22',
          insertedby: 'insertedby',
        },
        {
          id: 2,
          name: 'Applicant 2',
          address: '0x7zd7a8ds6dsa',
          role: 'Role',
          description:
            'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. ',
          validatedby: 'validated',
          file: '',
          durationstart: '24/04/22',
          durationend: '30/04/22',
          title: 'Title',
          descriptioninfo:
            'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. ',
          timestamp: '24/04/22',
          insertedby: 'insertedby',
        },
        {
          id: 3,
          name: 'Applicant 3',
          address: '0x7zd7a8ds6dsa',
          role: 'Role',
          description:
            'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. ',
          validatedby: 'validated',
          file: '',
          durationstart: '24/04/22',
          durationend: '30/04/22',
          title: 'Title',
          descriptioninfo:
            'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. ',
          timestamp: '24/04/22',
          insertedby: 'insertedby',
        },
        {
          id: 4,
          name: 'Applicant 4',
          address: '0x7zd7a8ds6dsa',
          role: 'Role',
          description:
            'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. ',
          validatedby: 'validated',
          file: '',
          durationstart: '24/04/22',
          durationend: '30/04/22',
          title: 'Title',
          descriptioninfo:
            'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. ',
          timestamp: '24/04/22',
          insertedby: 'insertedby',
        },
      ],
    };
  },

  setup() {
    return {
      card: ref(false),
      log: ref(false),
      share: ref(false),
      sharing: ref(true),
      exposeemail: ref(true),
      timelimit: ref(true),
      allowfile: ref(true),
    };
  },
  methods: {
    Clicked: function (list) {
      // eslint-disable-next-line
      this.nameinfo = list.name;
      // eslint-disable-next-line
      this.addressinfo = list.address;
      // eslint-disable-next-line
      this.roleinfo = list.role;
      // eslint-disable-next-line
      this.descriptioninfomodal = list.description;
      // eslint-disable-next-line
      this.validatedbyinfo = list.validatedby;
      // eslint-disable-next-line
      this.fileinfo = list.file;
      // eslint-disable-next-line
      this.durationstartinfo = list.durationstart;
      // eslint-disable-next-line
      this.durationendinfo = list.durationend;
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
  height: 80%;
  margin: 2%;
  margin-top: 1%;
  margin-bottom: 1%;
  padding-bottom: 1%;
  border-style: solid;
  border-radius: 10px;
}

.avatar {
  height: 150px;
  width: 10%;
  float: left;
}

.usericon {
  font-size: 9em;
}

.logs {
  height: 530px;
  width: 47%;
  border-radius: 10px;
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
  height: 60%;
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
