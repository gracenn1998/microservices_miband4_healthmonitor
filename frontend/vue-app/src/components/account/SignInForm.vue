<template>
  <div>
    <b-card class="w-50 mx-auto" style="margin-top: 5vh">
        <b-form @submit="onSubmit" @reset="onReset" v-if="show">
        <b-form-group label="Email address:">
            <b-form-input
              v-model="form.email"
              type="email"
              required
              placeholder="Enter email"
            ></b-form-input>
        </b-form-group>

        <b-form-group label="Password:">
            <b-form-input
              v-model="form.password"
              type="password"
              required
              placeholder="Enter password"
            ></b-form-input>
        </b-form-group>

        <b-form-group>
            <b-form-checkbox-group v-model="form.checked" id="checkboxes-4">
            <b-form-checkbox value="me">Remember me</b-form-checkbox>
            </b-form-checkbox-group>
        </b-form-group>

        <div class="w-25 mx-auto">
          <b-button type="signin" variant="primary">Submit</b-button>
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
      }
    },
    methods: {
      async validatePassword(email) {
        try {
          const response = await fetch('http://127.0.0.1:5000/checkpassword/'+email)
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
        if(this.validatePassword()) {
        //   ???
        }
      },
      
      onReset(evt) {
        evt.preventDefault()
        // Reset our form values
        this.form.email = ''
        this.form.password = ''
        this.form.checked = []
        // Trick to reset/clear native browser form validation state
        this.show = false
        this.$nextTick(() => {
          this.show = true
        })
      }
    }
  }
</script>
