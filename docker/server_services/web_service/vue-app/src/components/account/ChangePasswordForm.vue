<template>
    <b-card-title class="text-center mt-2" >
        <div v-if="submitStatus === 'OK'">
            <b-alert variant="success" show>Changed password successfully</b-alert>
        </div>
        <div v-if="submitStatus === 'ERROR'">
            <b-alert variant="danger" show>Current password is incorrect. Please check again</b-alert>
        </div>
        <div v-if="submitStatus === 'PENDING'">
            <b-alert variant="info" show>Sending request...</b-alert>
        </div>

        <b-form @submit.prevent="updateName">
            <b-form-group >
                <b-form-input
                    v-model="form.currentPassword"
                    type="password"
                    required
                    placeholder="Enter current password"
                ></b-form-input>
            </b-form-group>
            
            <b-form-group 
                :invalid-feedback="invalidPw"
                :state="pwState"
            >
                <b-form-input
                    v-model="form.newPassword"
                    :state="pwState"
                    type="password"
                    required
                    placeholder="Enter new password"
                ></b-form-input>
            </b-form-group>
            
            <b-form-group
                :invalid-feedback="invalidCfPw"
                :state="cfPwState"  
            >
                <b-form-input
                    v-model="form.confirmNewPassword"
                    :state="cfPwState"
                    type="password"
                    required
                    placeholder="Re-enter new password"
                ></b-form-input>
            </b-form-group>
            <div>
              <b-button @click="changePassword" variant="outline-success" class="mr-1">➕</b-button>
              <b-button @click="$emit('exit-change-pw-mode')" variant="outline-danger">✖️</b-button>
          </div>
        </b-form>
    </b-card-title>
</template>

<script>
import * as user from '@/api_calls/User.js'

export default {
    data(){
        return {
            form: {
                currentPassword: '',
                newPassword: '',
                confirmNewPassword: ''
            },
            submitStatus: '',
        }
    },
    computed: {
        pwState() {
            if(this.form.newPassword=='') {
                return null
            }
            return this.form.newPassword.length >= 6
        },
        cfPwState() {
            if(this.form.confirmNewPassword=='') {
                return null
            }
            return this.form.confirmNewPassword == this.form.newPassword
        },
        invalidPw() {
            if (this.form.newPassword.length > 0) {
                return 'Enter at least 6 characters.'
            }
            return null
        },
        invalidCfPw() {
            if (this.form.confirmNewPassword.length > 0) {
                return 'Confirm password need to be same as password'
            }
            return null
        },
    },

    methods: {
        changePassword(){
            const uid = this.$session.get('user').id
            
            var cur_pw = this.form.currentPassword
            var new_pw = this.form.newPassword
            user.changePasswordApiCall(uid, cur_pw, new_pw).then((result)=>{
                if(result) {//if succeeded
                    this.submitStatus = 'OK'
                    // this.$emit('exit-change-pw-mode')
                }
                else {
                    this.submitStatus = 'ERROR'
                }
            })
            this.submitStatus = 'PENDING'
        }


    }
}
</script>