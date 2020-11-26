<template>
  <div>
    <b-card class="w-50 mx-auto" style="margin-top: 5vh">
      <div class="w-25 mx-auto" >
        <b-button variant="outline-primary">Sign Up Form</b-button>
      </div>
      <div v-if="submitStatus === 'OK'">
        <b-alert variant="success" show>Signed up successfully. Sign in now?</b-alert>
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

      <div class="w-25 mx-auto">
        <b-button type="submit" variant="primary">Submit</b-button>
        <b-button type="reset" variant="danger">Reset</b-button>
      </div>
      </b-form>
    </b-card>
  </div>
</template>

<script>
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
      submitStatus: null
    }
  },

  methods: {
    async validateEmail(email) {
      try {
        const response = await fetch('http://127.0.0.1:5000/getuser/'+email)
        const result = await response.json()
        if (result.user!=null) {
          return false
        }
        return true
      } catch (error) {
        console.error(error)
      }
    },
    async addUser(user) {
      try {
        const response = await fetch('http://127.0.0.1:5000/adduser', {
          method: 'POST',
          body: JSON.stringify(user),
          headers: { 'Content-type': 'application/json; charset=UTF-8' },
        })
        const data = await response
        console.log(data)
      } catch (error) {
        console.error(error)
      }
    },
    onSubmit(evt) {
      evt.preventDefault()
      if(this.pwState && this.cfPwState) {
        this.validateEmail(this.form.email).then((ableToAdd)=>{
          if(ableToAdd) {
            this.addUser(this.form).then(()=>{
              this.submitStatus = 'OK'
            })
            this.submitStatus = 'PENDING'
          }
          else {
            this.validEmail = false
            this.submitStatus = 'ERROR'
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
