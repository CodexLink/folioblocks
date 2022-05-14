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
        targetted_address = null;
        targetted_number = 0;
      "
    />

    <q-card class="users">
      <q-linear-progress v-if="isFetchingStudent" query color="red" />
      <h5 class="text-body1" style="margin-left: 4%">
        <strong>Students Available</strong>
      </h5>
      <q-scroll-area style="height: 100%; max-width: 100%">
        <q-item
          v-for="student in students"
          :key="student.id"
          clickable
          v-ripple
          :active="targetted_number === student.id"
          active-class="selected_student"
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
                      val.length >= 2 ||
                      'This is required. Must have 2 characters above.',
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
                      val.length >= 8 ||
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
                      val.length >= 4 ||
                      'This is required. Must have 4 characters and above.',
                  ]"
                  lazy-rules
                />

                <q-file
                  class="input"
                  v-model="new_log_file"
                  label="Document Proof (PDF Only, 5MB Max)"
                  hint="This is optionally recommended as this can be used as a supporting context. Should contain no sensitive information."
                  filled
                  multiple
                  clearable
                  lazy-rules
                  :error="new_log_file_invalid"
                  @focus="new_log_file_invalid = false"
                  :disable="isProcessing"
                  accept=".pdf"
                  max-file-size="5242880"
                >
                  <template v-slot:prepend>
                    <q-icon name="attach_file" />
                  </template>
                  <template v-slot:error
                    >A document or a supporting context in a PDF form is
                    required!</template
                  >
                </q-file>

                <q-input
                  class="input"
                  filled
                  v-model="new_log_date_start"
                  mask="date"
                  label="Log Date Start"
                  :error="new_log_date_start_invalid"
                  readonly
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
                          @click="new_log_date_start_invalid = false"
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
                  <template v-slot:error>
                    The date may be missing or is colliding with the log date
                    end.
                  </template>
                </q-input>

                <q-input
                  class="input"
                  filled
                  v-model="new_log_date_end"
                  :error="new_log_date_end_invalid"
                  mask="date"
                  :disable="isProcessing"
                  label="Log Date End"
                  readonly
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
                          @click="new_log_date_end_invalid = false"
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
                  <template v-slot:error>
                    The date is colliding with the log date start.
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
                    :disable="
                      isProcessing ||
                      this.new_log_name === null ||
                      this.new_log_name === '' ||
                      this.new_log_description === null ||
                      this.new_log_description === '' ||
                      this.new_log_role === null ||
                      this.new_log_role === '' ||
                      this.new_log_file === null ||
                      this.new_log_file === '' ||
                      this.new_log_date_start === null ||
                      new_log_date_start === ''
                    "
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
                      val.length >= 4 ||
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
                      val.length >= 8 ||
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
                    :disable="
                      isProcessing ||
                      new_remark_title === null ||
                      new_remark_title === '' ||
                      new_remark_description === null ||
                      new_remark_description === ''
                    "
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
                :error="new_student_email_invalid"
                @focus="new_student_email_invalid = false"
                hint="Ask the student regarding what email to use as this will be exposed for contacting purposes."
                :disable="isProcessing"
                :rules="[(val) => val.includes('@') || 'Invalid email format.']"
                lazy-rules
              >
                <template v-slot:error>
                  Please change the value of this field as your input already
                  exists from the system.
                </template></q-input
              >

              <q-input
                class="inputnew"
                outlined
                dense
                color="secondary"
                v-model="new_student_username"
                label="Username"
                hint="This will be wary of this as it will be used to login."
                :error="new_student_username_invalid"
                :disable="isProcessing"
                @focus="new_student_username_invalid = false"
                counter
                :rules="[
                  (val) =>
                    (val.length >= 8 && val.length <= 24) ||
                    'This should contain not less than 8 characters or more than 24 characters.',
                ]"
                lazy-rules
              >
                <template v-slot:error>
                  Please change the value of this field as your input already
                  exists from the system.
                </template></q-input
              >
            </div>

            <q-input
              class="input"
              outlined
              dense
              color="secondary"
              v-model="new_student_personal_skills"
              label="Personal Skills"
              counter
              hint="Similar to description but is specified to student's capability. Seperate the contents in comma. Be wary of the initial input as it will be imprinted in blockchain. Student can change this later on."
              :rules="[
                (val) =>
                  val.length >= 8 ||
                  'This is required. Must have 8 characters and above.',
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
                    (val.length >= 4 && val.length <= 64) ||
                    'This should contain not less than 4 characters or more than 24 characters.',
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
                hint="Reference hint whether this student graduated in 3rd year or 5th year."
                counter
                :rules="[
                  (val) =>
                    (val >= 3 && val <= 5) || 'Year level cannot go below 2.',
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
              hint="The preferred role the student infers. This is interchangeable but please provide an initial input. Therefore, ask your student regarding one."
              counter
              :rules="[
                (val) =>
                  (val.length >= 2 && val.length <= 32) ||
                  'This should contain not less than 2 characters or more than 32 characters.',
              ]"
              lazy-rules
            />

            <div class="row">
              <q-input
                class="inputnew"
                outlined
                dense
                color="secondary"
                v-model="new_student_password"
                label="Student Password"
                :disable="isProcessing"
                :type="new_student_show_password ? 'text' : 'password'"
                hint="The password that the student will use to login."
                counter
                :rules="[
                  (val) =>
                    (val.length >= 8 && val.length <= 64) ||
                    'This should contain not less than 8 characters or more than 64 characters.',
                ]"
                lazy-rules
              >
                <template v-slot:append>
                  <q-icon
                    :name="
                      new_student_show_password
                        ? 'visibility'
                        : 'visibility_off'
                    "
                    class="cursor-pointer"
                    @click="
                      new_student_show_password = !new_student_show_password
                    "
                  />
                </template>
              </q-input>
              <q-input
                class="inputnew"
                outlined
                dense
                color="secondary"
                v-model="new_student_password_confirm"
                label="Student Password Confirm"
                :type="new_student_show_confirm_password ? 'text' : 'password'"
                :disable="isProcessing"
                hint="Repeat the password to confirm the password."
                counter
                :rules="[
                  (val) =>
                    (val.length >= 8 &&
                      val.length <= 64 &&
                      val == new_student_password) ||
                    'This should match your password to confirm your password.',
                ]"
                lazy-rules
              >
                <template v-slot:append>
                  <q-icon
                    :name="
                      new_student_show_confirm_password
                        ? 'visibility'
                        : 'visibility_off'
                    "
                    class="cursor-pointer"
                    @click="
                      new_student_show_confirm_password =
                        !new_student_show_confirm_password
                    "
                  />
                </template>
              </q-input>
            </div>

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
                :disable="
                  isProcessing ||
                  new_student_first_name === null ||
                  new_student_first_name === '' ||
                  new_student_last_name === null ||
                  new_student_last_name === '' ||
                  new_student_username === null ||
                  new_student_username === '' ||
                  new_student_email === null ||
                  new_student_email === '' ||
                  new_student_password === null ||
                  new_student_password === '' ||
                  new_student_password_confirm === null ||
                  new_student_password_confirm === '' ||
                  new_student_description === null ||
                  new_student_description === '' ||
                  new_student_personal_skills === null ||
                  new_student_personal_skills === '' ||
                  new_student_recent_program === null ||
                  new_student_recent_program === '' ||
                  new_student_prefer_role === null ||
                  new_student_prefer_role === ''
                "
                label="Insert"
              />
            </div>
          </q-form>
        </q-card>
      </div>
    </div>
    <q-page-sticky position="bottom-right" :offset="[24, 24]">
      <q-btn
        fab
        v-ripple
        icon="mdi-text-box-check"
        color="amber"
        v-if="targetted_number > 0 && targetted_address"
        @click="directToPortfolio"
      >
        <q-tooltip
          class="bg-indigo"
          :offset="[10, 10]"
          anchor="center left"
          self="center right"
        >
          View Portfolio of {{ targetted_address }}
        </q-tooltip>
      </q-btn>
    </q-page-sticky>
  </div>
</template>

<script>
import { ref } from 'vue';
import { useQuasar } from 'quasar';
import axios from 'axios';
import { MASTER_NODE_BACKEND_URL } from '/utils/utils.js';
import { useRoute, useRouter } from 'vue-router';

export default {
  setup() {
    const $q = useQuasar();
    const $route = useRoute();
    const $router = useRouter();

    return {
      selected_section: ref('insert_docs'),
      targetted_address: ref(null),
      targetted_number: ref(null),
    };
  },

  data() {
    return {
      students: ref([]),
      focused_portfolio_address: ref(''),

      new_student_first_name: ref(''),
      new_student_last_name: ref(''),
      new_student_username: ref(''),
      new_student_email: ref(''),
      new_student_password: ref(''),
      new_student_password_confirm: ref(''),
      new_student_description: ref(''),
      new_student_personal_skills: ref(''),
      new_student_recent_program: ref(''),
      new_student_recorded_year_level: ref(4),
      new_student_prefer_role: ref(''),

      new_student_username_invalid: ref(false),
      new_student_email_invalid: ref(false),

      new_log_date_start_invalid: ref(false),
      new_log_date_end_invalid: ref(false),
      new_log_file_invalid: ref(false),

      new_student_show_password: ref(false),
      new_student_show_confirm_password: ref(false),

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

    if (
      this.targetted_number === null &&
      this.existing_user === false &&
      this.new_user === false
    )
      this.$q.notify({
        color: 'blue',
        position: 'top',
        message:
          'Please select a student from the left side. Otherwise, create a new student.',
        timeout: 5000,
        progress: true,
        icon: 'info',
      });
  },
  methods: {
    submitNewStudent() {
      this.isProcessing = true;

      // ! Send a request.
      axios
        .post(
          `${MASTER_NODE_BACKEND_URL}/node/receive_context`,
          {
            first_name: this.new_student_first_name,
            last_name: this.new_student_last_name,
            email: this.new_student_email,
            username: this.new_student_username,
            password: this.new_student_password_confirm,
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
            timeout: 5000,
            progress: true,
            icon: 'report_problem',
          });
          this.clearRegistrationForm(false);

          this.isProcessing = false;
        })
        .catch((e) => {
          const responseDetail =
            e.response.data === undefined
              ? `${e.message}. Server may be unvailable. Please try again later.`
              : e.response.data.detail;

          this.$q.notify({
            color: 'negative',
            position: 'top',
            message: `There was an error when submitting your credentials. Reason: ${responseDetail}`,
            timeout: 15000,
            progress: true,
            icon: 'report_problem',
          });

          // ! Catch the error and render the field to change.
          // * Don't do this when error doesn't provide `detail` dictionary.
          if (e.response.data !== undefined) {
            let field_error = e.response.data.detail.split(
              'UNIQUE constraint failed: '
            )[1];

            if (field_error == 'users.email') {
              this.new_student_email_invalid = true;
            } else if (field_error == 'users.username') {
              this.new_student_username_invalid = true;
            }
          }
          this.isProcessing = false;
        });
    },
    submitStudentFormError() {
      this.$q.notify({
        color: 'negative',
        position: 'top',
        message:
          'There was an error from one of the fields. Please check and try again.',
        timeout: 5000,
        progress: true,
        icon: 'report_problem',
      });
    },
    clearRegistrationForm(showMessage = true) {
      // ! Clear Context
      this.new_student_first_name = null;
      this.new_student_last_name = null;
      this.new_student_username = null;
      this.new_student_email = null;
      this.new_student_password = null;
      this.new_student_password_confirm = null;
      this.new_student_description = null;
      this.new_student_personal_skills = null;
      this.new_student_recent_program = null;
      this.new_student_recorded_year_level = 1;
      this.new_student_prefer_role = null;

      this.new_student_show_password = false;
      this.new_student_show_confirm_password = false;

      this.new_student_email_invalid = false;
      this.new_student_username_invalid = false;

      if (showMessage)
        this.$q.notify({
          color: 'green',
          position: 'top',
          message: 'Student registration fields has been cleared!',
          timeout: 5000,
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
          timeout: 5000,
          progress: true,
          icon: 'report_problem',
        });

        this.isProcessing = false;
      } else {
        // ! Validate the date of the duration if 'new_log_date_end' is not None.
        if (this.new_log_date_end !== null) {
          let validateDateStart = new Date(this.new_log_date_start);
          let validateDateEnd = new Date(this.new_log_date_end);

          if (validateDateEnd.toTimeString() !== 'Invalid Date') {
            if (validateDateEnd < validateDateStart) {
              this.$q.notify({
                color: 'negative',
                position: 'top',
                message:
                  'Duration end seems to be earlier than the duration start. Please fix that.',
                timeout: 5000,
                progress: true,
                icon: 'report_problem',
              });

              this.new_log_date_start_invalid = true;
              this.new_log_date_end_invalid = true;

              this.isProcessing = false;
              return;
            }
          } else {
            this.new_log_date_end = null;
          }
        }
        // * Handle the request.
        let logForm = new FormData();

        logForm.append('address_origin', this.targetted_address);
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
            `${MASTER_NODE_BACKEND_URL}/node/receive_context_log`,
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
              timeout: 5000,
              progress: true,
              icon: 'report_problem',
            });
            this.clearLogForm(false);

            this.isProcessing = false;
          })
          .catch((e) => {
            const responseDetail =
              e.response.data === undefined
                ? `${e.message}. Server may be unvailable. Please try again later.`
                : e.response.data.detail;

            this.$q.notify({
              color: 'negative',
              position: 'top',
              message: `There was an error when submitting log information. Reason: ${responseDetail}`,
              timeout: 5000,
              progress: true,
              icon: 'report_problem',
            });

            this.isProcessing = false;
          });
      }
    },
    errorOnLog() {
      this.$q.notify({
        color: 'negative',
        position: 'top',
        message:
          'There was an error from one of the log fields. Please check and ensure that all conditions are met, then try again.',
        timeout: 5000,
        progress: true,
        icon: 'report_problem',
      });

      if (this.new_log_file === null || this.new_log_file === '') {
        this.new_log_file_invalid = true;
      }

      if (this.new_log_date_start === null || this.new_log_date_start === '') {
        this.new_log_date_start_invalid = true;
      }
    },
    clearLogForm(showMessage = true) {
      // ! Clear Context
      this.new_log_name = null;
      this.new_log_description = null;
      this.new_log_role = null;
      this.new_log_file = null;
      this.new_log_date_start = null;
      this.new_log_date_end = null;

      this.new_log_file_invalid = false;

      this.new_log_date_start_invalid = false;
      this.new_log_date_end_invalid = false;

      if (showMessage)
        this.$q.notify({
          color: 'green',
          position: 'top',
          message: 'Log referral fields has been cleared!',
          timeout: 5000,
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
          timeout: 5000,
          progress: true,
          icon: 'report_problem',
        });
      } else {
        axios
          .post(
            `${MASTER_NODE_BACKEND_URL}/node/receive_context`,
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
              timeout: 5000,
              progress: true,
              icon: 'report_problem',
            });
            this.clearRemarkForm(false);

            this.isProcessing = false;
          })
          .catch((e) => {
            const responseDetail =
              e.response.data === undefined
                ? `${e.message}. Server may be unvailable. Please try again later.`
                : e.response.data.detail;

            this.$q.notify({
              color: 'negative',
              position: 'top',
              message: `There was an error when submitting extra information. Reason: ${responseDetail}`,
              timeout: 5000,
              progress: true,
              icon: 'report_problem',
            });

            this.isProcessing = false;
          });
      }
    },
    errorOnRemark() {
      this.$q.notify({
        color: 'negative',
        position: 'top',
        message:
          'There was an error from one of the remark fields. Please check and ensure that all conditions are met, then try again.',
        timeout: 5000,
        progress: true,
        icon: 'report_problem',
      });
    },
    clearRemarkForm(showMessage = true) {
      // ! Clear Context
      this.new_remark_title = null;
      this.new_remark_description = null;

      if (showMessage)
        this.$q.notify({
          color: 'green',
          position: 'top',
          message: 'Student remark fields has been cleared!',
          timeout: 5000,
          progress: true,
          icon: 'mdi-account-check',
        });
    },
    optionsFn(org_date) {
      let datePlusOne = new Date();

      // * Modify the new instance, 'date' + 1.
      datePlusOne.setDate(datePlusOne.getDate());

      return (
        new Date(null).toISOString().slice(0, 10).replaceAll('-', '/') >=
          org_date ||
        org_date <= datePlusOne.toISOString().slice(0, 10).replaceAll('-', '/')
      );
    },
    setActiveFieldForForm(id) {
      this.targetted_number = id;
      this.targetted_address = this.students[id - 1].address;
      this.clearRemarkForm(false);
      this.clearLogForm(false);
    },
    getStudents() {
      this.isFetchingStudent = true;
      axios
        .get(`${MASTER_NODE_BACKEND_URL}/dashboard/students`, {
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

          this.isFetchingStudent = false;
        })
        .catch((e) => {
          this.$q.notify({
            color: 'negative',
            position: 'top',
            message: `Cannot fetch students. Reason: ${e.message}`,
            timeout: 5000,
            progress: true,
            icon: 'report_problem',
          });

          this.isFetchingStudent = false;
        });
    },
    directToPortfolio() {
      void this.$router.push({
        path: '/portfolio',
        query: { address: this.targetted_address },
      });
    },
  },
};
</script>

<style scoped>
.my-card-new_user {
  width: 600px;
  padding-bottom: 2%;
}

.selected_student {
  color: rgba(0, 0, 0, 0.7);
  background: #f2c037;
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
