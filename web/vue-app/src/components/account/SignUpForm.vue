<template>
  <div>
    <b-card class="w-50 mx-auto mt-3">
      <div class="d-flex justify-content-center mb-3">
        <b-button variant="outline-primary">Sign Up Form</b-button>
      </div>
      <div v-if="submitStatus === 'OK'">
        <b-alert variant="success" show>Signed up successfully. 
          <router-link to="/signin">Sign in now?</router-link>
        </b-alert>
      </div>
      <div v-if="submitStatus === 'ERROR'">
        <b-alert variant="danger" show>Please check all the fields again.</b-alert>
      </div>
      <div v-if="submitStatus === 'PENDING'">
        <b-alert variant="info" show>Sending request...</b-alert>
      </div>

      <b-form @submit="onSubmit" @reset="onReset" v-if="show">
      <b-form-group 
        label="Email address:"
        :invalid-feedback="invalidEmail"
        :state="emailState"
      >
          <b-form-input
            v-model="form.email"
            type="email"
            required
            placeholder="Enter email"
          ></b-form-input>
      </b-form-group>

      <b-form-group 
        label="Password:"
        :invalid-feedback="invalidPw"
        :state="pwState"
      >
          <b-form-input
            v-model="form.password"
            :state="pwState"
            type="password"
            required
            placeholder="Enter password"
          ></b-form-input>
      </b-form-group>

      <b-form-group 
        label="Confirm Password:"
        :invalid-feedback="invalidCfPw"
        :state="cfPwState"  
      >
          <b-form-input
            v-model="form.cfpassword"
            :state="cfPwState"
            type="password"
            required
            placeholder="Re-enter password"
          ></b-form-input>
      </b-form-group>

      <div class="d-flex justify-content-center">
        <b-button type="submit" variant="primary">SignUp</b-button>
        <b-button type="reset" variant="danger">Reset</b-button>
      </div>
      </b-form>
    </b-card>

    <b-modal id="service-error-modal" title="Server Error">
        <div class="d-block text-center">
            <h5>Some error happened...</h5>
            <h1>🛠️</h1>
            <h5>Please try again later</h5>
        </div>
    </b-modal>
  </div>
</template>

<script>
import * as user from '@/api_calls/User.js'

export default {
  computed: {
    emailState() {
      return this.validEmail
    },
    pwState() {
      if(this.form.password=='') {
        return null
      }
      return this.form.password.length >= 6
    },
    cfPwState() {
      if(this.form.cfpassword=='') {
        return null
      }
      return this.form.cfpassword == this.form.password
    },
    invalidEmail() {
      if(this.validEmail==false)
        return 'This email has been used. Please try another email'
      return null
    },
    invalidPw() {
      if (this.form.password.length > 0) {
        return 'Enter at least 6 characters.'
      }
      return null
    },
    invalidCfPw() {
      if (this.form.cfpassword.length > 0) {
        return 'Confirm password need to be same as password'
      }
      return null
    },
  },
  data() {
    return {
      form: {
        email: '',
        password: '',
        cfpassword: '',
      },
      show: true,
      validEmail: null,
      submitStatus: null,
    }
  },

  methods: {
    onSubmit(evt) {
      evt.preventDefault()
      //check if entered pw and cfpw are valid or not
      if(this.pwState && this.cfPwState) { //if both are valid
        user.getUserByEmailApiCall(this.form.email).then((result)=>{ 
          //check if email is valid (used) or not
          if(result['status-code']==204) { //if email hasnt been used -> create new user
            user.addUserApiCall(this.form).then(()=>{
              this.validEmail = true
              this.submitStatus = 'OK'
            })
            this.submitStatus = 'PENDING'
          }

          else if(result['status-code']==200) { //if email exists in dtb
            this.validEmail = false
            this.submitStatus = 'ERROR'
          }

          else if(result['status-code']==500) {
            this.$bvModal.show('service-error-modal')
            this.submitStatus = ''
          }
        })
      } else {
        this.submitStatus = 'ERROR'
      }
    },
    
    onReset(evt) {
      evt.preventDefault()
      // Reset our form values
      this.form.email = ''
      this.form.password = ''
      this.form.cfpassword = ''
      // Trick to reset/clear native browser form validation state
      this.show = false
      this.submitStatus = null
      this.$nextTick(() => {
        this.show = true
      })
    }
  }
}
</script>
