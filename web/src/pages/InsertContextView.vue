<template>
  <div class="q-pa-md q-gutter-sm">
    <q-btn
      outline
      class="add"
      color="secondary"
      label="New Student"
      icon="mdi-plus"
      :disable="isProcessing"
      @click="
        new_user = true;
        existing_user = false;
      "
    />

    <q-card class="users">
      <q-linear-progress v-if="isFetchingStudent" query color="red" />
      <q-scroll-area style="height: 100%; max-width: 100%">
        <q-item
          v-for="student in students"
          :key="student.id"
          clickable
          v-ripple
          :disable="isProcessing"
          @click="
            existing_user = true;
            new_user = false;
            setActiveFieldForForm(student.id);
          "
        >
          <q-item-section avatar>
            <q-avatar class="icon" icon="account_circle" size="3em" />
          </q-item-section>
          <q-item-section class="text-h6"
            >{{ student.first_name }} {{ student.last_name }}
            <q-item-label overline>{{ student.program }}</q-item-label>
            <q-item-label caption>{{ student.address }}</q-item-label>
          </q-item-section>
        </q-item>
      </q-scroll-area>
    </q-card>

    <div class="form absolute-center">
      <div class="absolute-center insertdata">
        <q-card v-show="existing_user" class="my-card">
          <q-linear-progress
            v-if="isProcessing"
            query
            color="secondary"
            class="q-mt-sm"
          />
          <q-tabs
            v-model="selected_section"
            dense
            class="text-grey"
            active-color="secondary"
            indicator-color="secondary"
            align="justify"
          >
            <q-tab
              name="insert_docs"
              label="Add Document"
              class="tab"
              :disable="isProcessing"
            />
            <q-tab
              name="insert_remarks"
              label="Add Remarks"
              class="tab"
              :disable="isProcessing"
            />
          </q-tabs>

          <q-separator />

          <q-tab-panels v-model="selected_section" animated class="panels">
            <q-tab-panel name="insert_docs">
              <q-form
                @submit.prevent="submitLog"
                @validation-error="errorOnLog"
                :autofocus="true"
              >
                <q-card-section class="title">
                  <p class="text-left">
                    Insert a Document or a Information to Refer at Student
                  </p>
                </q-card-section>
                <p class="text-justify" style="padding: 2%">
                  This form allows you to insert a reference with a
                  <strong>proof</strong> from the student. It can be a
                  certification, work experience, promotion, and any other proof
                  that a document or an information can infer.
                </p>
                <p class="text-justify" style="padding: 0 2%">
                  <strong>Note that</strong>, it is your
                  <strong>responsibility</strong> to mask out any detailed
                  information regarding this student. This system does not
                  pseudonymize information within the document and is only
                  designed as a source origin of this claim.
                </p>
                <q-input
                  class="input"
                  outlined
                  color="secondary"
                  v-model="new_log_name"
                  :disable="isProcessing"
                  counter
                  label="Log Name"
                  hint="The name of this log or the general context of it, please keep it concise and easy to understand."
                  :rules="[
                    (val) =>
                      (val && val.length >= 8) ||
                      'This is required. Must have 8 characters and above.',
                  ]"
                  lazy-rules
                />

                <q-input
                  class="input"
                  outlined
                  color="secondary"
                  v-model="new_log_description"
                  label="Log Description"
                  :disable="isProcessing"
                  counter
                  hint="The context of this log. Please provide enough information as possible, but keep it clean."
                  :rules="[
                    (val) =>
                      (val && val.length >= 8) ||
                      'This is required. Must have 8 characters and above.',
                  ]"
                  lazy-rules
                />

                <q-input
                  class="input"
                  outlined
                  color="secondary"
                  v-model="new_log_role"
                  label="Student's Role"
                  :disable="isProcessing"
                  counter
                  hint="The student's role from this log, generally more of a role from the job, keep it concise as possible."
                  :rules="[
                    (val) =>
                      (val && val.length >= 4) ||
                      'This is required. Must have 4 characters and above.',
                  ]"
                  lazy-rules
                />

                <q-file
                  class="input"
                  v-model="new_log_file"
                  label="Document Proof (PDF Files Only)"
                  hint="This is optional but is recommended as this can be used as a supporting context. Also, must contain no sensitive information."
                  filled
                  multiple
                  clearable
                  counter
                  :disable="isProcessing"
                  accept=".pdf"
                  max-file-size="5242880"
                >
                  <template v-slot:prepend>
                    <q-icon name="attach_file" />
                  </template>
                </q-file>

                <q-input
                  class="input"
                  filled
                  v-model="new_log_date_start"
                  mask="date"
                  :rules="['new_log_date_start']"
                  label="Log Date Start"
                  :disable="isProcessing"
                  hint="The date from where this log has started."
                >
                  <template v-slot:append>
                    <q-icon name="event" class="cursor-pointer">
                      <q-popup-proxy
                        ref="qDateProxy"
                        cover
                        transition-show="scale"
                        transition-hide="scale"
                      >
                        <q-date
                          v-model="new_log_date_start"
                          today-btn
                          :options="optionsFn"
                          color="secondary"
                        >
                          <div class="row items-center justify-end">
                            <q-btn
                              v-close-popup
                              label="Close"
                              color="primary"
                              flat
                            />
                          </div>
                        </q-date>
                      </q-popup-proxy>
                    </q-icon>
                  </template>
                </q-input>

                <q-input
                  class="input"
                  filled
                  v-model="new_log_date_end"
                  mask="date"
                  :disable="isProcessing"
                  :rules="['new_log_date_end']"
                  label="Log Date End"
                  hint="The date from where this log has ended. This is optional. However, when it contains a date, it should not start as early as the `Log Date Start`!"
                >
                  <template v-slot:append>
                    <q-icon name="event" class="cursor-pointer">
                      <q-popup-proxy
                        ref="qDateProxy"
                        cover
                        transition-show="scale"
                        transition-hide="scale"
                      >
                        <q-date
                          v-model="new_log_date_end"
                          today-btn
                          :options="optionsFn"
                          color="secondary"
                        >
                          <div class="row items-center justify-end">
                            <q-btn
                              v-close-popup
                              label="Close"
                              color="primary"
                              flat
                            />
                          </div>
                        </q-date>
                      </q-popup-proxy>
                    </q-icon>
                  </template>
                </q-input>

                <div class="text-center q-ma-md">
                  <q-btn
                    outline
                    class="close"
                    color="red"
                    label="Clear Fields"
                    @click="clearLogForm"
                    :disable="isProcessing"
                  />

                  <q-btn
                    outline
                    type="submit"
                    class="insert"
                    color="secondary"
                    :disable="isProcessing"
                    label="Insert"
                  />
                </div>
              </q-form>
            </q-tab-panel>

            <q-tab-panel name="insert_remarks">
              <q-form
                @submit.prevent="submitRemark"
                @validation-error="errorOnRemark"
                :autofocus="true"
              >
                <q-card-section class="title">
                  <p class="text-left">
                    Insert Extra Information / Remarks from the Student
                  </p>
                </q-card-section>
                <p class="text-justify" style="padding: 2%">
                  This form allows you to insert an extra information that
                  wasn't significant but is necessary for other people to know.
                  <strong>Note that,</strong> regardless of the context,
                  professionalism must be invoked as this extra information is
                  <strong>NOT interchangeable</strong> as it was imprinted in
                  blockchain.
                </p>
                <p class="text-justify" style="padding: 0 2%">
                  Any mistakes or misconceptions regarding the representation of
                  this context towards to the student will be held liable to
                  you, as the
                  <strong>source origin was also recorded</strong>. Please be
                  careful and make it sure the context was finalized before
                  submitting this form.
                </p>
                <q-input
                  class="input"
                  outlined
                  color="secondary"
                  v-model="new_remark_title"
                  :disable="isProcessing"
                  label="Remark Title"
                  counter
                  hint="The general context of this remark. Make it concise but minimal as possible."
                  :rules="[
                    (val) =>
                      (val && val.length >= 4) ||
                      'This is required. Must have 4 characters and above.',
                  ]"
                  lazy-rules
                />

                <q-input
                  class="input"
                  outlined
                  color="secondary"
                  type="textarea"
                  :disable="isProcessing"
                  hint="Please describe in detail regarding this context."
                  counter
                  v-model="new_remark_description"
                  label="Remark Description"
                  :rules="[
                    (val) =>
                      (val && val.length >= 8) ||
                      'This is required. Must have 8 characters and above.',
                  ]"
                  lazy-rules
                />

                <div class="text-center q-ma-md">
                  <q-btn
                    outline
                    class="close"
                    color="red"
                    @click="clearRemarkForm"
                    :disable="isProcessing"
                    label="Clear Fields"
                  />

                  <q-btn
                    outline
                    class="insert"
                    color="secondary"
                    type="submit"
                    :disable="isProcessing"
                    label="Insert"
                  />
                </div>
              </q-form>
            </q-tab-panel>
          </q-tab-panels>
        </q-card>
      </div>

      <div class="absolute-center text-center">
        <q-card class="my-card-new_user" v-show="new_user">
          <q-linear-progress
            v-if="isProcessing"
            query
            color="secondary"
            class="q-mt-sm"
          />
          <q-card-section class="title">
            <p class="text-left">Insert a New Student</p>
          </q-card-section>
          <p class="text-justify" style="padding: 2%">
            This form was intended for providing students the capability to
            store and access their credentials for job application purposes.
            Note that the information you enter is unchangeable due to
            blockchain nature.
          </p>
          <p class="text-justify" style="padding: 0 2%">
            <strong>Note that</strong>, any students who was recently inserted
            won't be shown immediately as it needs to be
            <strong>processed</strong> by blockchain first! They are accessible
            but they cannot be referred until that account contains
            <strong>transaction mapping</strong>.
          </p>
          <q-form
            @submit.prevent="submitNewStudent"
            @validation-error="submitStudentFormError"
            :autofocus="true"
          >
            <div class="row">
              <q-input
                class="inputnew"
                outlined
                dense
                color="secondary"
                counter
                v-model="new_student_first_name"
                label="First Name"
                :rules="[
                  (val) =>
                    (val.length >= 2 && val.length <= 32) ||
                    'Invalid, this is required. Should contain 2 to 32 characters.',
                ]"
                lazy-rules
                :disable="isProcessing"
              />

              <q-input
                class="inputnew"
                outlined
                dense
                color="secondary"
                counter
                v-model="new_student_last_name"
                label="Last Name"
                :rules="[
                  (val) =>
                    (val.length >= 2 && val.length <= 32) ||
                    'Invalid, this is required. Should contain 2 to 32 characters.',
                ]"
                lazy-rules
                :disable="isProcessing"
              />
            </div>

            <q-input
              class="input"
              outlined
              dense
              color="secondary"
              v-model="new_student_description"
              label="Description"
              counter
              hint="Make the description formalized as the first entry will be imprinted in blockchain, student can change this information when logged on."
              :rules="[
                (val) =>
                  !val.length ||
                  (val.length >= 8 && val.length <= 256) ||
                  'Cannot go less than 8 characters or more than 256 characters.',
              ]"
              lazy-rules
              :disable="isProcessing"
            />

            <div class="row">
              <q-input
                class="inputnew"
                outlined
                dense
                color="secondary"
                type="email"
                v-model="new_student_email"
                label="E-mail"
                counter
                lazy-rules
                hint="Ask the student regarding what email to use as this will be exposed for contacting purposes."
                :disable="isProcessing"
                :rules="[(val) => val.includes('@') || 'Invalid email format.']"
              />

              <q-input
                class="inputnew"
                outlined
                dense
                color="secondary"
                v-model="new_student_username"
                label="Username"
                hint="This will be wary of this as it will be used to login."
                :disable="isProcessing"
                counter
                :rules="[
                  (val) =>
                    (val.length >= 8 && val.length <= 24) ||
                    'This should contain not less than 8 characters or more than 24 characters.',
                ]"
                lazy-rules
              />
            </div>

            <q-input
              class="input"
              outlined
              dense
              color="secondary"
              v-model="new_user_personal_skills"
              label="Personal Skills"
              counter
              hint="Similar to description but is specified to student's capability. Seperate the contents in comma. Be wary of the initial input as it will be imprinted in blockchain. Student can change this later on."
              :rules="[
                (val) =>
                  !val.length ||
                  (val.length >= 8 && val.length <= 256) ||
                  'Cannot go less than 8 characters or more than 256 characters.',
              ]"
              lazy-rules
              :disable="isProcessing"
            />
            <div class="row">
              <q-input
                class="inputnew"
                outlined
                dense
                color="secondary"
                v-model="new_student_recent_program"
                label="Program"
                hint="Do not use acronym, and do not prefix it with BS or Bachelor."
                :disable="isProcessing"
                counter
                :rules="[
                  (val) =>
                    (val.length >= 8 && val.length <= 64) ||
                    'This should contain not less than 8 characters or more than 24 characters.',
                ]"
                lazy-rules
              />

              <q-input
                class="inputnew"
                outlined
                dense
                color="secondary"
                v-model="new_student_recorded_year_level"
                label="Year Level"
                type="number"
                :disable="isProcessing"
                hint="Reference hint whether this student graduated in 4th year or 5th year."
                counter
                :rules="[
                  (val) =>
                    (val >= 1 && val <= 6) ||
                    'Year level cannot go below 1 or 7 and above.',
                ]"
                lazy-rules
              />
            </div>

            <q-input
              class="input"
              outlined
              dense
              color="secondary"
              v-model="new_student_prefer_role"
              label="Preferred Employment Role"
              :disable="isProcessing"
              hint="The preferred role the student infers. Please note that it is NOT changeable due to implementation issues. Please ask the student first before inputting values here."
              counter
              :rules="[
                (val) =>
                  (val.length >= 4 && val.length <= 32) ||
                  'This should contain not less than 4 characters or more than 32 characters.',
              ]"
              lazy-rules
            />

            <q-input
              class="input"
              outlined
              dense
              color="secondary"
              v-model="new_student_password"
              type="password"
              label="Password"
              :disable="isProcessing"
              hint="The password that the student uses. The developers recommends random generation of password to avoid bias."
              counter
              :rules="[
                (val) =>
                  (val.length >= 8 && val.length <= 64) ||
                  'This should contain not less than 8 characters or more than 64 characters.',
              ]"
              lazy-rules
            />

            <div class="text-center q-ma-md">
              <q-btn
                outline
                class="close"
                color="red"
                label="Clear Fields"
                @click="clearRegistrationForm"
                :disable="isProcessing"
              />

              <q-btn
                outline
                class="insert"
                type="submit"
                color="secondary"
                :disable="isProcessing"
                label="Insert"
              />
            </div>
          </q-form>
        </q-card>
      </div>
    </div>
  </div>
</template>

<script>
import { defineComponent, ref } from 'vue';
import { useQuasar } from 'quasar';
import axios from 'axios';
import { resolvedNodeAPIURL } from '/utils/utils.js';
import { useRoute, useRouter } from 'vue-router';

export default {
  setup() {
    const $q = useQuasar();
    const $route = useRoute();
    const $router = useRouter();

    return {
      selected_section: ref('insert_docs'),
      targetted_address: ref(null),
    };
  },

  data() {
    return {
      students: ref([]),

      new_student_first_name: ref(''),
      new_student_last_name: ref(''),
      new_student_username: ref(''),
      new_student_email: ref(''),
      new_student_password: ref(''),
      new_student_description: ref(''),
      new_user_personal_skills: ref(''),
      new_student_recent_program: ref(''),
      new_student_recorded_year_level: ref(''),
      new_student_prefer_role: ref(''),

      existing_user: ref(false),
      new_user: ref(false),
      isProcessing: ref(false),
      isFetchingStudent: ref(true),

      new_log_name: ref(''),
      new_log_description: ref(''),
      new_log_role: ref(''),
      new_log_file: ref(null),

      new_log_date_start: ref(null),
      new_log_date_end: ref(null),

      new_remark_title: ref(''),
      new_remark_description: ref(''),
    };
  },
  mounted() {
    if (this.$route.params.action === 'new') {
      this.existing_user = false;
      this.new_user = true;
    } else {
      this.existing_user = false;
      this.new_user = false;
    }
    this.getStudents();
  },
  methods: {
    submitNewStudent() {
      this.isProcessing = true;

      // ! Send a request.
      axios
        .post(
          `http://${resolvedNodeAPIURL}/node/receive_context`,
          {
            first_name: this.new_student_first_name,
            last_name: this.new_student_last_name,
            email: this.new_student_email,
            username: this.new_student_username,
            password: this.new_student_password,
            program: this.new_student_recent_program,
            year_level: this.new_student_recorded_year_level,
            preferred_role: this.new_student_prefer_role,
            description: this.new_student_description,
            skills: this.new_user_personal_skills,
          },
          {
            headers: {
              'x-token': this.$q.localStorage.getItem('token'),
            },
          }
        )
        .then((response) => {
          this.$q.notify({
            color: 'green',
            position: 'top',
            message: `Student registration finished! | Info: ${response.data.detail}`,
            timeout: 10000,
            progress: true,
            icon: 'report_problem',
          });
        })
        .catch((e) => {
          this.$q.notify({
            color: 'negative',
            position: 'top',
            message: `There was an error when submitting your credentials. Reason: ${
              e.response.data.detail || e.message
            }`,
            timeout: 15000,
            progress: true,
            icon: 'report_problem',
          });
        });

      this.isProcessing = false;
    },
    submitStudentFormError() {
      this.$q.notify({
        color: 'negative',
        position: 'top',
        message:
          'There was an error from one of the fields. Please check and try again.',
        timeout: 10000,
        progress: true,
        icon: 'report_problem',
      });
    },
    clearRegistrationForm() {
      this.new_student_first_name = '';
      this.new_student_last_name = '';
      this.new_student_username = '';
      this.new_student_email = '';
      this.new_student_password = '';
      this.new_student_description = '';
      this.new_user_personal_skills = '';
      this.new_student_recent_program = '';
      this.new_student_recorded_year_level = '';
      this.new_student_prefer_role = '';

      this.$q.notify({
        color: 'green',
        position: 'top',
        message: 'Student registration fields has been cleared!',
        timeout: 10000,
        progress: true,
        icon: 'mdi-account-check',
      });
    },
    submitLog() {
      this.isProcessing = true;

      // ! Force require `new_log_date_start` field.
      if (this.new_log_date_start == null) {
        this.$q.notify({
          color: 'negative',
          position: 'top',
          message: 'Duration start field is required!',
          timeout: 10000,
          progress: true,
          icon: 'report_problem',
        });
      } else {
        // ! Validate the date of the duration if 'new_log_date_end' is not None.
        if (this.new_log_date_end !== null) {
          let validateDateEnd = new Date(this.new_log_date_start);
          let validateDateStart = new Date(this.new_log_date_end);

          if (validateDateEnd > validateDateStart) {
            this.$q.notify({
              color: 'negative',
              position: 'top',
              message:
                'Duration start and end is impossible. Please ensure that the duration end doesnt start earlier than the duration start.',
              timeout: 10000,
              progress: true,
              icon: 'report_problem',
            });
            this.isProcessing = false;
            return;
          }
        }
        // * Handle the request.
        let logForm = new FormData();

        logForm.append('address_origin', this.targetted_address);
        logForm.append('content_type', 2); // * See TransactionContextMappingType.APPLICANT_LOG.
        logForm.append('name', this.new_log_name);
        logForm.append('description', this.new_log_description);
        logForm.append('role', this.new_log_role);
        logForm.append(
          'duration_start',
          new Date(this.new_log_date_start).toISOString()
        );

        if (this.new_log_date_end !== null) {
          logForm.append(
            'duration_end',
            new Date(this.new_log_date_end).toISOString()
          );
        }

        if (this.new_log_file !== null) {
          logForm.append('file', this.new_log_file[0]);
        }

        axios
          .post(
            `http://${resolvedNodeAPIURL}/node/receive_context_log`,
            logForm,
            {
              headers: {
                'X-Token': this.$q.localStorage.getItem('token'),
                'Content-Type': 'multipart/form-data',
              },
            }
          )
          .then((response) => {
            this.$q.notify({
              color: 'green',
              position: 'top',
              message: `Log information has been sent from the node to blockchain! Remember about the notice regarding taking the new information in-effect. | Info: ${response.data.detail}`,
              timeout: 10000,
              progress: true,
              icon: 'report_problem',
            });
          })
          .catch((e) => {
            this.$q.notify({
              color: 'negative',
              position: 'top',
              message: `There was an error when submitting log information. Reason: ${e.response.data.detail}`,
              timeout: 10000,
              progress: true,
              icon: 'report_problem',
            });
          });
      }
      this.isProcessing = false;
    },
    errorOnLog() {
      this.$q.notify({
        color: 'negative',
        position: 'top',
        message:
          'There was an error from one of the log fields. Please check and ensure that all conditions are met, then try again.',
        timeout: 10000,
        progress: true,
        icon: 'report_problem',
      });
    },
    clearLogForm() {
      this.new_log_name = '';
      this.new_log_description = '';
      this.new_log_role = '';
      this.new_log_file = null;
      this.new_log_date_start = null;
      this.new_log_date_end = null;

      this.$q.notify({
        color: 'green',
        position: 'top',
        message: 'Log referral fields has been cleared!',
        timeout: 10000,
        progress: true,
        icon: 'mdi-account-check',
      });
    },

    submitRemark() {
      this.isProcessing = true;

      if (this.targetted_address == null) {
        this.$q.notify({
          color: 'negative',
          position: 'top',
          message: `There was an error when submitting extra information. Reason: ${e.request.statusText}`,
          timeout: 10000,
          progress: true,
          icon: 'report_problem',
        });
      } else {
        axios
          .post(
            `http://${resolvedNodeAPIURL}/node/receive_context`,
            {
              address_origin: this.targetted_address,
              title: this.new_remark_title,
              description: this.new_remark_description,
            },
            {
              headers: {
                'X-Token': this.$q.localStorage.getItem('token'),
              },
            }
          )
          .then((response) => {
            this.$q.notify({
              color: 'green',
              position: 'top',
              message: `Extra information has been sent from the nodes to blockchain! Remember about the notice regarding taking the new information in-effect. | Info: ${response.data.detail}`,
              timeout: 10000,
              progress: true,
              icon: 'report_problem',
            });
          })
          .catch((e) => {
            this.$q.notify({
              color: 'negative',
              position: 'top',
              message: `There was an error when submitting extra information. Reason: ${e.response.data.detail}`,
              timeout: 10000,
              progress: true,
              icon: 'report_problem',
            });
          });
      }
      this.isProcessing = false;
    },
    errorOnRemark() {
      this.$q.notify({
        color: 'negative',
        position: 'top',
        message:
          'There was an error from one of the remark fields. Please check and ensure that all conditions are met, then try again.',
        timeout: 10000,
        progress: true,
        icon: 'report_problem',
      });
    },
    clearRemarkForm() {
      this.new_remark_title = '';
      this.new_remark_description = '';

      this.$q.notify({
        color: 'green',
        position: 'top',
        message: 'Student remark fields has been cleared!',
        timeout: 10000,
        progress: true,
        icon: 'mdi-account-check',
      });
    },
    optionsFn(org_date) {
      let datePlusOne = new Date();

      // * Modify the new instance, 'date' + 1.
      datePlusOne.setDate(datePlusOne.getDate() + 1);

      return (
        new Date(null).toISOString().slice(0, 10).replaceAll('-', '/') >=
          org_date ||
        org_date <= datePlusOne.toISOString().slice(0, 10).replaceAll('-', '/')
      );
    },
    setActiveFieldForForm(id) {
      this.targetted_address = this.students[id - 1].address;
    },
    getStudents() {
      this.isFetchingStudent = true;
      axios
        .get(`http://${resolvedNodeAPIURL}/dashboard/students`, {
          headers: {
            'X-Token': this.$q.localStorage.getItem('token'),
          },
        })
        .then((response) => {
          let student_index = 1;
          let resolved_students = [];

          for (let each_student of response.data) {
            each_student.id = student_index;
            student_index += 1;
            resolved_students.push(each_student);
          }
          this.students = resolved_students;
        })
        .catch((e) => {
          this.$q.notify({
            color: 'negative',
            position: 'top',
            message: `Cannot fetch students. Reason: ${e.message}`,
            timeout: 10000,
            progress: true,
            icon: 'report_problem',
          });
        });

      this.isFetchingStudent = false;
    },
  },
};
</script>

<style scoped>
.my-card-new_user {
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
  height: 95%;
  width: 60%;
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
  margin-bottom: 1%;
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
  .my-card-new_user {
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

  .my-card-new_user {
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
