<template>
  <q-layout view="hHh lpR lFf">
    <body>
      <div class="header">
        <q-card
          class="profile"
          style="
            background-image: url(https://cdn.quasar.dev/img/parallax2.jpg);
            object-fit: cover;
            -webkit-filter: brightness(95%);
            filter: brightness(95%);
          "
        >
          <q-card-section>
            <h2 class="text-white">Hello {{ first_name }} {{ last_name }}!</h2>
            <h4 class="alias text-white">
              <strong>{{ user_role }}</strong>
            </h4>
            <p class="alias text-white">
              Identified as <strong>{{ user_address }}</strong> or
              <strong>{{ user_name }}</strong>
            </p>
            <div class="btn">
              <q-btn
                outline
                rounded
                color="white"
                :label="button_left"
                :to="button_left_link"
              />
              <q-btn
                outline
                rounded
                color="white"
                :label="button_right"
                :to="button_right_link"
              />
            </div>
          </q-card-section>
        </q-card>
      </div>

      <div class="main">
        <q-card class="blocks">
          <q-linear-progress
            :value="context_progress_top"
            rounded
            reverse
            color="red"
          />
          <q-icon
            name="mdi-account-group"
            color="red"
            size="6em"
            style="padding-left: 20px; padding-top: 10px"
          />
          <div class="output">
            <p class="data">{{ context_right_top }}</p>
            <p class="title">{{ context_right_top_primary }}</p>
          </div>
        </q-card>

        <q-card flat bordered class="seminar">
          <q-card-section>
            <div class="text-h6">{{ context_left }}</div>
          </q-card-section>

          <q-card-section class="q-pt-none">
            {{ context_left_primary }}
          </q-card-section>

          <q-card-section class="q-pt-none">
            <q-linear-progress
              :value="context_left_progress_top"
              rounded
              color="red"
              class="q-mt-sm"
            />
            <p class="text-caption">Log Percentage by Bar</p>
            <q-linear-progress
              :value="context_left_progress_bottom"
              rounded
              color="secondary"
              class="q-mt-sm"
            />
            <p class="text-caption">Extra Percentage by Bar</p>
          </q-card-section>
          <q-separator />
          <q-card-section>
            {{ context_left_secondary }}
          </q-card-section>
        </q-card>

        <q-card class="transaction">
          <q-linear-progress
            :value="context_progress_bottom"
            rounded
            reverse
            color="secondary"
          />
          <q-icon
            name="today"
            class="secondary"
            size="6em"
            color="secondary"
            style="padding-left: 20px; padding-top: 10px"
          />
          <div class="output">
            <p class="data">{{ context_right_bottom }}</p>
            <p class="title">{{ context_right_bottom_primary }}</p>
          </div>
        </q-card>
      </div>
    </body>
  </q-layout>
</template>

<script>
import { defineComponent, ref } from 'vue';
import { useQuasar } from 'quasar';
import axios from 'axios';
import { resolvedNodeAPIURL } from '/utils/utils.js';
import { useRoute, useRouter } from 'vue-router';

let dashboardOptions = {
  applicant: {
    buttons: ['View Portfolio', 'Edit Personal Info'],
    links: ['/portfolio', '/user_info'],
    context: {
      left: {
        title: 'Portfolio Current Settings',
        subtitle:
          'Here contains the settings of your portfolio, please check them in portfolio section to change these values.',
      },
      right_top: {
        title: 'Total Credentials',
        subtitle:
          'The number of credentials you received from your institution, out of other credentials.',
      },
      right_bottom: {
        title: 'Percentage of Logs vs Extra Info',
        subtitle:
          'You have the following percetange makes up of your portfolio.',
      },
    },
  },
  organization: {
    buttons: ['Generate User', 'Refer Credentials'],
    links: ['/org/insert/new', '/org/insert/standby'],
    context: {
      left: {
        title: 'Logs vs Extra Info Dominance',
        subtitle:
          'The following visualization is a percetange-equivalent of logs vs extra information being inserted frequently.',
        another:
          'The progression bar only visualizes and thurs an estimation as per page refresh.',
      },
      right_top: {
        title: 'Total Associations',
        subtitle:
          'The number of associations that associates to your organization.',
      },
      right_bottom: {
        title: 'Total Transactions Invoked',
        subtitle: 'The number of transactions you have thrown at the students',
      },
    },
  },
};

export default defineComponent({
  name: 'Dashboard',
  components: {},

  data() {
    return {
      button_left: ref('—'),
      button_right: ref('—'),

      button_left_link: ref('—'),
      button_right_link: ref('—'),

      first_name: ref('—'),
      last_name: ref('—'),
      user_address: ref('—'),
      user_role: ref('—'),
      user_name: ref('—'),

      context_left: ref('—'),
      context_right_top: ref('—'),
      context_right_bottom: ref('—'),

      context_left_primary: ref('—'),
      context_right_top_primary: ref('—'),
      context_right_bottom_primary: ref('—'),

      context_left_secondary: ref('—'),
      context_right_top_secondary: ref('—'),
      context_right_bottom_secondary: ref('—'),

      context_left_progress_top: ref(0.4),
      context_left_progress_bottom: ref(0.6),

      context_progress_top: ref(0.3),
      context_progress_bottom: ref(0.69),
    };
  },
  setup() {
    const $route = useRoute();
    const $router = useRouter();
    const $q = useQuasar();
  },
  mounted() {
    this.getUserDashboardContext();
  },
  methods: {
    getUserDashboardContext() {
      axios
        .get(`http://${resolvedNodeAPIURL}/dashboard`, {
          headers: {
            'X-Token': this.$q.localStorage.getItem('token'),
          },
        })
        .then((response) => {
          this.first_name = response.data.first_name;
          this.last_name = response.data.last_name;
          this.user_address = response.data.address;
          this.user_role = response.data.role;
          this.user_name = response.data.username;

          // * Adjust the context for the organization.
          // - Replace the button context.
          this.button_left = dashboardOptions.organization.buttons[0];
          this.button_left_link = dashboardOptions.organization.links[0];
          this.button_right = dashboardOptions.organization.buttons[1];
          this.button_right_link = dashboardOptions.organization.links[1];

          // - Replace the cards context.
          this.context_left = dashboardOptions.organization.context.left.title;
          this.context_left_primary =
            dashboardOptions.organization.context.left.subtitle;
          this.context_left_secondary =
            dashboardOptions.organization.context.left.another;

          // this.context_left_progress_top =
          // this.context_left_progress_bottom =

          // - Update Card #1.
          this.context_right_top =
            dashboardOptions.organization.context.right_top.title;
          this.context_right_top_primary = `Currently, there was ${response.data.reports.total_associated} out of ${response.data.reports.total_users} associated users from the system.`;
          this.context_progress_top =
            response.data.reports.total_associated /
            response.data.reports.total_users;

          // - Update Card #2.
          this.context_left_progress_top =
            response.data.reports.total_associated_logs /
            response.data.reports.total_overall_info_outside;
          this.context_left_progress_bottom =
            response.data.reports.total_associated_extra /
            response.data.reports.total_overall_info_outside;

          // - Update Card #3.
          this.context_right_bottom =
            dashboardOptions.organization.context.right_bottom.title;
          this.context_right_bottom_primary = `Your organization was able to insert ${
            response.data.reports.total_associated_logs +
            response.data.reports.total_associated_extra
          } out of ${
            response.data.reports.total_overall_info_outside
          } transactions.`;
          this.context_progress_bottom = '';
          // * Adjust the context for the applicant.
          // - Replace the button context.
          // this.button_left = dashboardOptions.applicant.buttons[0];
          // this.button_left_link = dashboardOptions.applicant.links[0];
          // this.button_right = dashboardOptions.applicant.buttons[1];
          // this.button_right_link = dashboardOptions.applicant.links[1];

          // - Replace the cards context.
        })
        .catch((_e) => {
          this.$q.notify({
            color: 'red',
            position: 'top',
            message:
              'Failed to parse data from the dashboard. Please try again.',
            timeout: 10000,
            progress: true,
            icon: 'mdi-cancel',
          });
        });
    },
  },
});
</script>

<style scoped>
.main {
  display: grid;
  margin: 6%;
  margin-bottom: 0%;
  padding-bottom: 3%;

  gap: 1.5rem;
  grid-template-columns: repeat(2, 1fr);
}

.header {
  display: grid;
  margin: 6%;
  margin-top: 3%;
  gap: 1.5rem;
}

.status {
  display: grid;
  grid-template-columns: 20% 30% 20% 30%;
  background-color: #54d6ff;
}

.profile {
  height: 100%;
}

.btn {
  display: grid;
  gap: 1em;
  grid-template-columns: repeat(2, 1fr);
  padding: 1%;
  font-size: 1em;
}

h2 {
  font-family: 'Poppins';
  font-size: 2.5em;
  font-weight: 500;
  text-align: center;
  margin-bottom: 1%;
  word-break: break-all;
}

.alias {
  font-family: 'Poppins';
  font-size: 1.3em;
  text-align: center;
  margin-bottom: 5%;
}

h4 {
  font-family: 'Poppins';
  font-size: 1.8em;
  font-weight: 400;
  line-height: 15px;
}

.dataheader {
  font-size: 2em;
  font-family: 'Poppins';
  font-weight: 500;
  line-height: 0px;
}

.icon {
  font-size: 130px;
  margin-left: 25%;
}

img {
  height: 50px;
  width: 50px;
  float: left;
  margin: 5%;
}

.seminar,
.activity {
  grid-row: span 2;
}
.seminar-activity-icon {
  height: 100px;
  width: 100px;
  float: left;
  margin: 5%;
  margin-top: 12%;
}

.dataseminar {
  margin-top: 15%;
  font-family: 'Poppins';
  font-weight: 600;
}

.titleseminar {
  font-family: 'Poppins';
  font-size: 1.5em;
  font-weight: 500;
}

.output {
  float: right;
  margin-right: 7%;
  margin-top: 4%;
  text-align: right;
}

.data {
  font-family: 'Poppins';
  font-size: 1.3em;
  font-weight: 700;
}

.title {
  font-family: 'Poppins';
  font-size: 1em;
  font-weight: 500;
}

@media (max-width: 100em) {
  .header {
    display: grid;
    margin: 6%;
    gap: 1.5rem;
    grid-template-columns: repeat(1, 1fr);
  }

  .status {
    display: grid;
    grid-template-columns: 15% 35% 15% 35%;
    background-color: #54d6ff;
  }

  .main {
    display: grid;
    margin: 6%;
    margin-bottom: 0%;
    padding-bottom: 3%;
    gap: 1.5rem;
    grid-template-columns: repeat(1, 1fr);
  }

  .icon {
    font-size: 100px;
    margin-left: 50%;
  }

  h4 {
    font-family: 'Poppins';
    font-size: 1em;
    font-weight: 400;
    line-height: 15px;
  }

  p {
    font-size: 1em;
    font-family: 'Poppins';
  }
  .dataheader {
    font-size: 1em;
    font-family: 'Poppins';
    font-weight: 500;
    line-height: 0px;
  }

  .seminar-activity-icon {
    height: 70px;
    width: 70px;
    float: left;
    margin: 4%;
    margin-top: 5%;
  }

  .dataseminar {
    margin-top: 0%;
    font-family: 'Poppins';
    font-weight: 600;
  }

  .titleseminar {
    font-family: 'Poppins';
    font-size: 1em;
    font-weight: 500;
  }

  .btn {
    display: grid;
    gap: 1em;
    grid-template-columns: repeat(1, 1fr);
    padding: 1%;
    line-height: 10%;
    font-size: 0.5em;
  }

  h2 {
    font-family: 'Poppins';
    font-size: 2em;
    font-weight: 500;
    text-align: center;
    margin-bottom: 1%;
  }

  .alias {
    font-family: 'Poppins';
    font-size: 1em;
    text-align: center;
    margin-bottom: 5%;
  }
}

@media (max-width: 60em) {
  .header {
    display: grid;
    margin: 6%;
    gap: 1.5rem;
    grid-template-columns: repeat(1, 1fr);
  }

  .status {
    display: grid;
    grid-template-columns: 25% 25% 25% 25%;
    background-color: #54d6ff;
  }

  .main {
    display: grid;
    margin: 6%;
    margin-bottom: 0%;
    padding-bottom: 3%;
    gap: 1.5rem;
    grid-template-columns: repeat(1, 1fr);
  }

  .icon {
    font-size: 90px;
    margin-left: 1%;
  }

  h4 {
    font-family: 'Poppins';
    font-size: 1em;
    font-weight: 400;
    line-height: 15px;
  }

  p {
    font-size: 1em;
    font-family: 'Poppins';
  }
  .dataheader {
    font-size: 1em;
    font-family: 'Poppins';
    font-weight: 500;
    line-height: 0px;
  }

  .seminar-activity-icon {
    height: 70px;
    width: 70px;
    float: left;
    margin: 4%;
    margin-top: 5%;
  }

  .dataseminar {
    margin-top: 0%;
    font-family: 'Poppins';
    font-weight: 600;
  }

  .titleseminar {
    font-family: 'Poppins';
    font-size: 1em;
    font-weight: 500;
  }

  .btn {
    display: grid;
    gap: 1em;
    grid-template-columns: repeat(1, 1fr);
    padding: 1%;
    font-size: 0.5em;
  }

  h2 {
    font-family: 'Poppins';
    font-size: 2em;
    font-weight: 500;
    text-align: center;
    margin-bottom: 1%;
  }

  .alias {
    font-family: 'Poppins';
    font-size: 1em;
    text-align: center;
    margin-bottom: 5%;
  }
}
</style>
