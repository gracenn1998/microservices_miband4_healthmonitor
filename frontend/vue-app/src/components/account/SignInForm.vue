<template>
  <div v-if="!this.$session.exists()">
    <b-card class="w-50 mx-auto mt-3">
      <div class="d-flex justify-content-center mb-3" >
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

      <div class="d-flex justify-content-center">
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
    async signin(email, password) {
      try {
        const response = await fetch('http://127.0.0.1:5000/login', {
          method: 'POST',
          body: JSON.stringify({
            'email': email,
            'password': password
            }),
          headers: { 'Content-type': 'application/json; charset=UTF-8' },
        })
        const result = await response.json()
        if (result['login-result']=='succeeded') { //sign in successfully
          return result['user']
        }
        // if signin failed
        return false
      } catch (error) {
        console.error(error)
      }
    },

    onSubmit(evt) {
      evt.preventDefault()
      //sign in api
      this.signin(this.form.email, this.form.password).then((result)=>{
          if(result) { //if sign in succeeded
            this.submitStatus = 'OK'
            //start session
            this.$session.start()
            this.$session.set('user', result)
            console.log(this.$session.get('user'))
            //routing to homepage
            this.$emit("loginStatusChange")
            this.$router.push('/')
          } else { //if sign in failed
            this.submitStatus = 'ERROR'
          }
        })
        this.submitStatus = 'PENDING'
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
