<template>
  <q-layout view="hHh lpR lFf">
    <body>
      <div class="header">
        <q-card class="profile">
          <q-card-section>
            <h2>Hello {{ user }}</h2>
            <p class="alias">You are also known as {{ alias }}</p>
            <div class="btn">
              <q-btn
                outline
                rounded
                color="white"
                label="View Your Profile"
                to="/view"
              />
              <q-btn outline rounded color="white" label="Recruit People" />
              <q-btn
                outline
                rounded
                color="white"
                label="Generate Certificate"
              />
            </div>
          </q-card-section>
        </q-card>

        <q-card class="status">
          <q-avatar class="icon" icon="view_in_ar" />
          <div>
            <h4>Total Blocks</h4>
            <p class="dataheader">{{ blocks }}</p>
          </div>

          <q-avatar class="icon" icon="schedule" />
          <div>
            <h4>Block Time</h4>
            <p class="dataheader">{{ time }}</p>
          </div>

          <q-avatar class="icon" icon="swap_horiz" />
          <div>
            <h4>Total TXS</h4>
            <p class="dataheader">{{ txs }}</p>
          </div>

          <q-avatar class="icon" icon="person" />
          <div>
            <h4>Total Addresses</h4>
            <p class="dataheader">{{ addresses }}</p>
          </div>
        </q-card>
      </div>

      <div class="main">
        <q-card class="seminar">
          <img class="seminar-activity-icon" src="\icon7.jpg" />
          <div class="output">
            <p class="dataseminar">{{ seminars }}</p>
            <p class="titleseminar">Total Seminar Established</p>
            <p>On monthly basis</p>
          </div>
        </q-card>

        <q-card class="blocks">
          <img src="\icon1.jpg" />
          <div class="output">
            <p class="data">{{ newblock }}</p>
            <p class="title">New Blocks</p>
          </div>
        </q-card>

        <q-card class="transaction">
          <img src="\icon2.jpg" />
          <div class="output">
            <p class="data">{{ transactions }}</p>
            <p class="title">Transaction Rates</p>
          </div>
        </q-card>

        <q-card class="activity">
          <img class="seminar-activity-icon" src="\icon8.jpg" />
          <div class="output">
            <p class="dataseminar">{{ activity }}</p>
            <p class="titleseminar">Total Activity Elements</p>
            <p>On monthly basis</p>
          </div>
        </q-card>

        <q-card class="totalblocks">
          <img src="\icon3.jpg" />
          <div class="output">
            <p class="data">{{ totalblocks }}</p>
            <p class="title">Total Blocks</p>
          </div>
        </q-card>

        <q-card class="certificate">
          <div class="output">
            <p class="data">{{ certificates }}</p>
            <p class="title">Generated Certificates</p>
          </div>
          <img src="\icon4.jpg" />
        </q-card>

        <q-card class="bounce">
          <div class="output">
            <p class="data">{{ bouncerate }}</p>
            <p class="title">Bounce Rate</p>
          </div>
          <img src="\icon5.jpg" />
        </q-card>

        <q-card class="visits">
          <div class="output">
            <p class="data">{{ visits }}</p>
            <p class="title">Total Visits</p>
          </div>
          <img src="\icon6.jpg" />
        </q-card>
      </div>
    </body>
  </q-layout>
</template>

<script>
import { defineComponent } from 'vue';
export default defineComponent({
  name: 'Dashboard',
  components: {},

  data() {
    return {
      user: '0x593sdx107c',
      alias: 'Ronan',

      blocks: '100000',
      time: '2 ms',
      txs: '10000',
      addresses: '100000',

      newblock: '1000',
      transactions: '1000',
      totalblocks: '1000',
      certificates: '1000',
      bouncerate: '1000',
      visits: '1000',
      seminars: '1000',
      activity: '1000',
    };
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
  grid-template-columns: repeat(2, 1fr);
}

.status {
  display: grid;
  grid-template-columns: 20% 30% 20% 30%;
  background-color: #54d6ff;
}

.profile {
  background-color: #54d6ff;
  height: 100%;
}

.btn {
  display: grid;
  gap: 1em;
  grid-template-columns: repeat(3, 1fr);
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

p {
  font-size: 2em;
  font-family: 'Poppins';
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
