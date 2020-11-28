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

            <b-card title="My miband">
                <b-button variant="outline-primary" class="w-100" @click="enterAddBandMode">+ Add device</b-button>
                <pair-device-form v-if="addBandMode" @exit-add-band-mode="exitAddBandMode"/>
                <device-list class="mt-1"/>
            </b-card>

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
import PairDeviceForm from '@/components/device/PairDeviceForm'
import DeviceList from '@/components/device/DeviceList'

export default {
    components: { 
        PairDeviceForm,
        DeviceList
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
            addBandMode: false
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

        enterAddBandMode() {
            this.addBandMode = true
        },
        exitAddBandMode() {
            this.addBandMode = false
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

        async updateNameApiCall(email, newName) {
            try {
                const response = await fetch('http://127.0.0.1:5000/updateuser/'+email, {
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
            this.updateNameApiCall(this.user.email, this.user.fullname).then((user)=>{
                this.$session.set('user', user)
                this.generateAvtStr()
                this.exitNameUpdateMode()
                // this.$forceUpdate
            })
        },
    }
}
</script>