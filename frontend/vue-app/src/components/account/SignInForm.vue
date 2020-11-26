<template>
  <div>
    <b-card class="w-50 mx-auto" style="margin-top: 5vh">
      <div class="w-25 mx-auto" >
        <b-button variant="outline-primary">Sign In Form</b-button>
      </div>
      <div v-if="submitStatus === 'OK'">
        <b-alert variant="success" show>Signed in successfully</b-alert>
      </div>
      <div v-if="submitStatus === 'ERROR'">
        <b-alert variant="danger" show>Email and password are incorrect. Please check again</b-alert>
      </div>
      <div v-if="submitStatus === 'PENDING'">
        <b-alert variant="info" show>Sending request...</b-alert>
      </div>
    
      <b-form @submit="onSubmit" @reset="onReset" v-if="show">
      <b-form-group 
        label="Email address:"
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
      >
          <b-form-input
            v-model="form.password"
            :state="pwState"
            type="password"
            required
            placeholder="Enter password"
          ></b-form-input>
      </b-form-group>

      <b-form-group>
          <b-form-checkbox-group v-model="form.checked">
          <b-form-checkbox value="remember">Remember me</b-form-checkbox>
          </b-form-checkbox-group>
      </b-form-group>

      <div class="w-25 mx-auto">
        <b-button type="signin" variant="primary">SignIn</b-button>
        <b-button type="reset" variant="danger">Reset</b-button>
      </div>
      </b-form>
    </b-card>
  </div>
</template>

<script>
export default {
  data() {
    return {
      form: {
        email: '',
        password: '',
        checked: []
      },
      show: true,
      validSignin: null,
      submitStatus: null
    }
  },
  methods: {
    async getEmail(email) {
      try {
        const response = await fetch('http://127.0.0.1:5000/getuser/'+email)
        const result = await response.json()
        if (result.user!=null) {
          return result.user.email
        }
        return null
      } catch (error) {
        console.error(error)
      }
    },
    async validatePassword(email, password) {
      try {
        const response = await fetch('http://127.0.0.1:5000/checkpassword/'+email, {
          method: 'POST',
          body: JSON.stringify({'password': password}),
          headers: { 'Content-type': 'application/json; charset=UTF-8' },
        })
        const result = await response.json()
        if (result.result!='correct') {
          return false
        }
        return true
      } catch (error) {
        console.error(error)
      }
    },
    onSubmit(evt) {
      evt.preventDefault()
      //check if email exist
      this.getEmail(this.form.email).then((email)=> {
        //if email exist
        if(email!=null) {
          this.validatePassword(email, this.form.password).then((isValid)=>{
            if(isValid) { //if password matched
              this.submitStatus = 'OK'
            } else { //if wrong password
              this.submitStatus = 'ERROR'
            }
          })
          this.submitStatus = 'PENDING'
        } else { //if email not exist
          this.submitStatus = 'ERROR'
        }
      })
    },
    
    onReset(evt) {
      evt.preventDefault()
      // Reset our form values
      this.form.email = ''
      this.form.password = ''
      this.form.checked = []
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
