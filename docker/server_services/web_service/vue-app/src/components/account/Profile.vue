<template>
    <div class="w-50 mx-auto mt-3 mb-3" v-if="this.$session.exists()">
        <b-card>
            <template #header>
                <div class="d-flex justify-content-center">
                    <b-avatar :text="avatarStr" size="6rem"></b-avatar>
                </div>
                <b-card-title v-if="user.fullname==null&&updateNameMode!=true" class="text-center mt-2">
                    <b-button variant="outline-primary" @click="enterUpdateNameMode">
                        Please tell us your name 📝
                    </b-button>
                </b-card-title>
                <b-card-title v-else-if="updateNameMode==true" class="text-center mt-2">
                    <b-form @submit.prevent="updateName" inline class="d-flex justify-content-around">
                        <b-form-input class="w-75"
                        v-model="user.fullname"
                        placeholder="Enter your name"
                    ></b-form-input>
                    <div>
                        <b-button @click="updateName" variant="success" class="mr-1">OK</b-button>
                        <b-button @click="exitUpdateNameMode" variant="danger">✖️</b-button>
                    </div>
                    </b-form>
                </b-card-title>
                <b-card-title v-else class="text-center mt-2">
                    {{user.fullname}}
                    <b-button variant="outline-primary" @click="enterUpdateNameMode">📝</b-button>
                </b-card-title>
                <b-card-sub-title class="text-center">{{user.email}}</b-card-sub-title>
                <!-- <div class="d-flex justify-content-center">
                    <b-card-text>🏆 Strike: 4days</b-card-text>
                </div> -->
            </template>

            <b-skeleton-wrapper :loading="deleteStatus === 'PENDING'">
                <template #loading>
                <b-card>
                <b-skeleton width="85%"></b-skeleton>
                <b-skeleton width="55%"></b-skeleton>
                <b-skeleton width="70%"></b-skeleton>
                </b-card>
            </template>
            <device-management />

            <!-- <b-card title="More" class="mt-1">
                <b-button variant="outline-primary" class="w-100">Set goal</b-button>
            </b-card> -->

            <b-card title="Account" class="mt-1">
                <b-button variant="outline-primary" class="w-100 mb-1"
                    @click="enterChangePwMode"
                >Change password</b-button>
                <ChangePasswordForm v-if="changePwMode==true" @exit-change-pw-mode="exitChangePwMode"/>
                <b-button variant="outline-primary" class="w-100" v-b-modal.confirm-delete-modal >Delete account</b-button>
                
            </b-card>
            
            <b-modal id="confirm-delete-modal" hide-footer title="Confirmation">
                <div class="d-block text-center">
                    <h4>Do you really want to delete this account?</h4>
                </div>
                <div class="d-flex justify-content-end">
                    <b-button class="mt-3 mr-3"  @click="$bvModal.hide('confirm-delete-modal')">Cancel</b-button>
                    <b-button class="mt-3 mr-4" variant="danger" @click="deleteAndCloseModal()">Delete</b-button>
                </div>
            </b-modal>
            </b-skeleton-wrapper>
        </b-card>
        
    </div>
</template>


<script>
import * as user from '@/api_calls/User.js'
import * as miband_conn from '@/api_calls/MibandConnection.js'
import * as miband_db from '@/api_calls/MibandDb.js'

import DeviceManagement from '@/components/DeviceManagement'
import ChangePasswordForm from '@/components/account/ChangePasswordForm.vue'

export default {
    components: { 
        DeviceManagement,
        ChangePasswordForm
    },
    created() {
        // console.log(this.user)
        this.generateAvtStr()
        
    },
    data() {
        return {
            user: this.$session.get('user'),
            avatarStr: '',
            updateNameMode: false,
            changePwMode: false,
            deleteStatus: '',
        }
    },
    methods: {
        enterUpdateNameMode() {
            this.updateNameMode = true
        },
        exitUpdateNameMode() {
            this.user.fullname=this.$session.get('user').fullname
            this.updateNameMode = false
        },
        enterChangePwMode() {
            this.changePwMode = true
        },
        exitChangePwMode() {
            this.changePwMode = false
        },

        generateAvtStr() {
            if(this.user.fullname!=null) {
                var str = String(this.$session.get('user').fullname)
                var seperateName = str.split(" ")
                if(seperateName.length==1){
                    this.avatarStr = seperateName[0][0]
                } else {
                    this.avatarStr=seperateName[0][0] + seperateName[seperateName.length-1][0]
                }
                
            }
            else{
                this.avatarStr=''
            }
        },

        updateName() {
            const uid = this.$session.get('user').id
            // this.updateNameApiCall(this.user.email, this.user.fullname)
            user.updateNameApiCall(uid, this.user.fullname).then((user)=>{
                this.$session.set('user', user)
                this.generateAvtStr()
                this.exitUpdateNameMode()
                // this.$forceUpdate
            })
        },


        async deleteAndCloseModal() {
            const user_id = this.$session.get('user').id
            const band_id = this.$session.get('miband').id

            this.$bvModal.hide('confirm-remove-modal')

            this.deleteStatus = 'PENDING'
            
            const deleteLogsResult = await miband_db.deleteUserLogsApiCall(user_id)
            var unpairBandResult = true
            var deleteUserResult
            if(deleteLogsResult) { //if succeeded
                console.log(this.$session.get('miband'))
                if(this.$session.get('miband')!=undefined) { //if pairing band exist
                    await miband_conn.disconnectApiCall()
                    unpairBandResult = await miband_db.unpairBandDbApiCall(band_id)
                }
            }
            if(unpairBandResult) {
                deleteUserResult = await user.deleteUserApiCall(user_id)
                if(deleteUserResult) {
                    this.deleteStatus = 'OK'
                    this.$session.destroy()
                    this.$emit('login-status-change')
                    this.$router.push('/')
                }
            }
        },
    }
}
</script>