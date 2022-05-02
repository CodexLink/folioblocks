<template>
  <div class="q-pa-md q-gutter-sm">
    <q-btn
      outline
      class="add"
      color="secondary"
      label="New User"
      @click="
        newuser = true;
        existing = false;
      "
    />

    <div class="users">
      <q-scroll-area style="height: 100%; max-width: 100%">
        <q-item
          v-for="list in lists"
          :key="list.id"
          clickable
          v-ripple
          @click="
            existing = true;
            newuser = false;
          "
        >
          <q-item-section avatar>
            <q-avatar class="icon" icon="account_circle"> </q-avatar>
          </q-item-section>
          <q-item-section class="text-h6"
            >{{ list.name }}
            <q-item-label caption>{{ list.address }}</q-item-label>
          </q-item-section>
        </q-item>
      </q-scroll-area>
    </div>

    <div class="form absolute-center">
      <div class="absolute-center insertdata">
        <q-card v-show="existing" class="my-card">
          <q-tabs
            v-model="tab"
            dense
            class="text-grey"
            active-color="black"
            indicator-color="black"
            align="justify"
          >
            <q-tab name="addinfo" label="Add Document" class="tab" />
            <q-tab name="addremarks" label="Add Remarks" class="tab" />
          </q-tabs>

          <q-separator />

          <q-tab-panels v-model="tab" animated class="panels">
            <q-tab-panel name="addinfo">
              <form>
                <q-input
                  class="input"
                  outlined
                  color="secondary"
                  v-model="name"
                  label="Name"
                />

                <q-input
                  class="input"
                  outlined
                  color="secondary"
                  v-model="description"
                  label="Description"
                />

                <q-select
                  class="input"
                  color="secondary"
                  outlined
                  v-model="model"
                  :options="options"
                  label="Role"
                />

                <q-file
                  class="input"
                  v-model="files"
                  label="Upload files"
                  filled
                  multiple
                >
                  <template v-slot:prepend>
                    <q-icon name="attach_file" />
                  </template>
                </q-file>

                <q-input
                  class="input"
                  v-model="datestart"
                  filled
                  type="date"
                  prefix="Duration Start"
                />

                <q-input
                  class="input"
                  v-model="dateend"
                  filled
                  type="date"
                  prefix="Duration End"
                />

                <div class="text-center q-ma-md">
                  <q-btn
                    outline
                    class="close"
                    color="secondary"
                    label="Close"
                    @click="existing = false"
                  />

                  <q-btn
                    outline
                    class="insert"
                    color="secondary"
                    label="Insert"
                  />
                </div>
              </form>
            </q-tab-panel>

            <q-tab-panel name="addremarks">
              <form>
                <q-input
                  class="input"
                  outlined
                  color="secondary"
                  v-model="title"
                  label="Title"
                />

                <q-input
                  class="input"
                  outlined
                  color="secondary"
                  v-model="extradescription"
                  label="Description"
                />

                <div class="text-center q-ma-md">
                  <q-btn
                    outline
                    class="close"
                    color="secondary"
                    label="Close"
                    @click="existing = false"
                  />

                  <q-btn
                    outline
                    class="insert"
                    color="secondary"
                    label="Insert"
                  />
                </div>
              </form>
            </q-tab-panel>
          </q-tab-panels>
        </q-card>
      </div>

      <div class="absolute-center text-center">
        <q-card class="my-card-newuser" v-show="newuser">
          <div class="title">
            <p>Insert New User</p>
          </div>
          <form>
            <q-file
              class="input"
              dense
              outlined
              v-model="avatar"
              label="Avatar"
            >
              <template v-slot:prepend>
                <q-icon name="cloud_upload" />
              </template>
            </q-file>

            <div class="row">
              <q-input
                class="inputnew"
                outlined
                dense
                color="secondary"
                v-model="FirstName"
                label="First Name"
              />

              <q-input
                class="inputnew"
                outlined
                dense
                color="secondary"
                v-model="LastName"
                label="Last Name"
              />
            </div>

            <div class="row">
              <q-input
                class="inputnew"
                outlined
                dense
                color="secondary"
                v-model="inserter"
                label="Inserter"
              />

              <q-input
                class="inputnew"
                outlined
                dense
                color="secondary"
                v-model="institution"
                label="Institution"
              />
            </div>
            <q-input
              class="input"
              outlined
              dense
              color="secondary"
              v-model="descriptioninput"
              label="Description"
            />

            <div class="row">
              <q-input
                class="inputnew"
                outlined
                dense
                color="secondary"
                v-model="email"
                label="E-mail"
              />

              <q-input
                class="inputnew"
                outlined
                dense
                color="secondary"
                v-model="Username"
                label="Username"
              />
            </div>

            <q-input
              class="input"
              outlined
              dense
              color="secondary"
              v-model="personalskills"
              label="Personal Skills"
            />
            <div class="row">
              <q-input
                class="inputnew"
                outlined
                dense
                color="secondary"
                v-model="course"
                label="Course"
              />

              <q-input
                class="inputnew"
                outlined
                dense
                color="secondary"
                v-model="yearlevel"
                label="Year Level"
              />
            </div>

            <q-input
              class="input"
              outlined
              dense
              color="secondary"
              v-model="preferrole"
              label="Prefer Role"
            />

            <q-input
              class="input"
              outlined
              dense
              color="secondary"
              v-model="password"
              type="password"
              label="Password"
            />

            <div class="text-center q-ma-md">
              <q-btn
                outline
                class="close"
                color="secondary"
                label="Close"
                @click="newuser = false"
              />

              <q-btn outline class="insert" color="secondary" label="Insert" />
            </div>
          </form>
        </q-card>
      </div>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue';

export default {
  setup() {
    return {
      basic: ref(false),
      existing: ref(false),
      newuser: ref(false),
      tab: ref('addinfo'),
      tabinsert: ref('insertnewuser'),
      model: ref(null),
      options: ['Institution', 'Applicant'],
      datestart: ref(''),
      dateend: ref(''),
    };
  },

  data() {
    return {
      lists: [
        {
          id: 1,
          name: 'Applicant 1',
          address: '0x7zd7a8ds6dsa',
        },
        {
          id: 2,
          name: 'Applicant 2',
          address: '0x7zd7a8ds6dsa',
        },
        {
          id: 3,
          name: 'Applicant 3',
          address: '0x7zd7a8ds6dsa',
        },
        {
          id: 4,
          name: 'Applicant 4',
          address: '0x7zd7a8ds6dsa',
        },
        {
          id: 5,
          name: 'Applicant 5',
          address: '0x7zd7a8ds6dsa',
        },
        {
          id: 6,
          name: 'Applicant 5',
          address: '0x7zd7a8ds6dsa',
        },
        {
          id: 7,
          name: 'Applicant 5',
          address: '0x7zd7a8ds6dsa',
        },
        {
          id: 8,
          name: 'Applicant 5',
          address: '0x7zd7a8ds6dsa',
        },
        {
          id: 9,
          name: 'Applicant 4',
          address: '0x7zd7a8ds6dsa',
        },
        {
          id: 10,
          name: 'Applicant 5',
          address: '0x7zd7a8ds6dsa',
        },
      ],

      name: '',
      description: '',
      title: '',
      extradescription: '',

      files: ref(''),
      avatar: ref(''),

      FirstName: ref(''),
      LastName: ref(''),
      Username: ref(''),
      email: ref(''),
      username: ref(''),
      password: ref(''),
      inserter: ref(''),
      institution: ref(''),
      descriptioninput: ref(''),
      personalskills: ref(''),
      course: ref(''),
      yearlevel: ref(''),
      preferrole: ref(''),
    };
  },
};
</script>

<style scoped>
.my-card-newuser {
  width: 600px;
  padding-bottom: 2%;
}

.title {
  padding: 2%;
  font-size: 1.5em;
  font-family: 'Poppins';
  font-weight: 600;
}
.input {
  margin: 2%;
}

.inputnew {
  width: 275px;
  margin: 2%;
}

.users {
  width: 20%;
  height: 880px;
  border-style: solid;
  background-color: #a7eaff;
  box-shadow: 0 0 20px #999999;
  overflow: hidden;
}

.form {
  background-color: #a7eaff;
  border-style: solid;
  height: 90%;
  width: 50%;
  margin-left: 10%;
  margin-top: 2%;
  box-shadow: 0 0 20px #999999;
}

.my-card {
  width: 100%;
}

.tab {
  height: 50px;
  width: 350px;
}

.add {
  width: 20%;
  font-family: 'Poppins';
}

.insert {
  margin-left: 3%;
  width: 150px;
  margin-top: 5%;
  font-family: 'Poppins';
}

.close {
  margin-right: 3%;
  width: 150px;
  margin-top: 5%;
  font-family: 'Poppins';
}

@media (max-width: 90em) {
  .text-h6 {
    font-size: 0.8em;
  }

  .list {
    overflow: hidden;
  }

  .tab {
    width: 200px;
  }

  .inputnew {
    width: 184px;
    margin: 2%;
  }
  .my-card-newuser {
    width: 400px;
    padding-bottom: 2%;
  }
}

@media (max-width: 45em) {
  .form {
    position: absolute;
    top: 850px;
    width: 97%;
    margin: 1%;
    margin-top: 0%;
  }

  .users {
    height: 300px;
    width: 100%;
  }

  .users {
    width: 100%;
  }

  .my-card {
    width: 100%;
  }

  .add {
    width: 100%;
  }

  .tab {
    width: 100px;
  }

  .my-card-newuser {
    width: 300px;
    padding-bottom: 2%;
  }

  h1 {
    font-size: 1.5em;
    font-family: 'Poppins';
    font-weight: 600;
  }
  .input {
    margin: 2%;
  }

  .inputnew {
    width: 136px;
    margin: 2%;
  }

  .insert {
    margin-left: 0%;
    width: 150px;
    margin-top: 3%;
    font-family: 'Poppins';
  }

  .close {
    margin-right: 0%;
    width: 150px;
    margin-top: 3%;
    font-family: 'Poppins';
  }
}
</style>
