<template>
    <div class="w-50 mx-auto mt-3 mb-3" v-if="this.$session.exists()">
        <b-card>
            <template #header>
                <div class="d-flex justify-content-center">
                    <b-avatar :text="avatarStr" size="6rem"></b-avatar>
                </div>
                <b-card-title v-if="user.fullname==null&&nameUpdateMode!=true" class="text-center mt-2">
                    <b-button variant="outline-primary" @click="enterNameUpdateMode">
                        Please tell us your name 📝
                    </b-button>
                </b-card-title>
                <b-card-title v-else-if="nameUpdateMode==true" class="text-center mt-2">
                    <b-form @submit.prevent="updateName" inline class="d-flex justify-content-around">
                        <b-form-input class="w-75"
                        v-model="user.fullname"
                        placeholder="Enter your name"
                    ></b-form-input>
                    <div>
                        <b-button @click="updateName" variant="success" class="mr-1">OK</b-button>
                        <b-button @click="exitNameUpdateMode" variant="danger">✖️</b-button>
                    </div>
                    </b-form>
                </b-card-title>
                <b-card-title v-else class="text-center mt-2">
                    {{user.fullname}}
                    <b-button variant="outline-primary" @click="enterNameUpdateMode">📝</b-button>
                </b-card-title>
                <b-card-sub-title class="text-center">{{user.email}}</b-card-sub-title>
                <div class="d-flex justify-content-center">
                    <b-card-text>🏆 Strike: 4days</b-card-text>
                </div>
            </template>

            <device-management />

            <b-card title="More" class="mt-1">
                <b-button variant="outline-primary" class="w-100">Set goal</b-button>
            </b-card>

            <b-card title="Account" class="mt-1">
                <b-button variant="outline-primary" class="w-100 mb-1">Change password</b-button>
                <b-button variant="outline-primary" class="w-100">Delete account</b-button>
            </b-card>

        </b-card>
    </div>
</template>


<script>
import DeviceManagement from '@/components/DeviceManagement'

export default {
    components: { 
        DeviceManagement
    },
    created() {
        // console.log(this.user)
        this.generateAvtStr()
        
    },
    data() {
        return {
            user: this.$session.get('user'),
            avatarStr: '',
            nameUpdateMode: false,
            user_db_host: this.$api_hosts['user_db_api'],
            user_db_port: this.$api_ports['user_db_api']
        }
    },
    methods: {
        enterNameUpdateMode() {
            this.nameUpdateMode = true
        },
        exitNameUpdateMode() {
            this.user.fullname=this.$session.get('user').fullname
            this.nameUpdateMode = false
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

        async updateNameApiCall(newName) {
            const uid = this.$session.get('user').id
            try {
                const response = await fetch(`http://${this.user_db_host}:${this.user_db_port}/users/${uid}/fullname`, {
                method: 'PUT',
                body: JSON.stringify({
                    'fullname': newName,
                    }),
                headers: { 'Content-type': 'application/json; charset=UTF-8' },
                })
                const user = await response.json()
                return user
            } catch (error) {
                console.error(error)
            }
        },
        updateName() {
            // this.updateNameApiCall(this.user.email, this.user.fullname)
            this.updateNameApiCall(this.user.fullname).then((user)=>{
                this.$session.set('user', user)
                this.generateAvtStr()
                this.exitNameUpdateMode()
                // this.$forceUpdate
            })
        },
    }
}
</script>