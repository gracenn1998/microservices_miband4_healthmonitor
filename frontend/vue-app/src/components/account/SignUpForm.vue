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

        <b-form-group label="Username:">
            <b-form-input
              v-model="form.username"
              required
              placeholder="Enter name"
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

        <b-form-group label="Re-enter password:">
            <b-form-input
              v-model="form.repassword"
              type="password"
              required
              placeholder="Re-enter password"
            ></b-form-input>
        </b-form-group>

        <!-- <b-form-group label="Gender">
            <b-form-radio-group
                v-model="selected"
                :options="options"
                plain
                name="plain-inline"
            ></b-form-radio-group>
        </b-form-group> -->

        <b-form-group id="input-group-4">
            <b-form-checkbox-group v-model="form.checked" id="checkboxes-4">
            <b-form-checkbox value="me">Remember me</b-form-checkbox>
            </b-form-checkbox-group>
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
    data() {
      return {
        form: {
          email: '',
          username: '',
          password: '',
          repassword: '',
          checked: []
        },
        show: true,
        selected: 'first',
        options: [
          { text: 'Female', value: 'F' },
          { text: 'Male', value: 'M' },
          { text: 'Others', value: 'O' }
        ]
      }
    },
    methods: {
      async addUser(user) {
        try {
          const response = await fetch('http://127.0.0.1:5000/adduser', {
            method: 'POST',
            body: JSON.stringify(user),
            headers: { 'Content-type': 'application/json; charset=UTF-8' },
          })
          const data = await response.json()
          console.log(data)
        } catch (error) {
          console.error(error)
        }
      },
      onSubmit(evt) {
        evt.preventDefault()
        console.log(JSON.stringify(this.form))
        this.addUser(this.form)
      },
      
      onReset(evt) {
        evt.preventDefault()
        // Reset our form values
        this.form.email = ''
        this.form.username = ''
        this.form.password = ''
        this.form.repassword = ''
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
