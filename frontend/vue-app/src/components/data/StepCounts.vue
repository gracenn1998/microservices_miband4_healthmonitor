<template>
    <div>
        <div>
            <b-form inline class="d-flex justify-content-between">
                <b-form-datepicker id="example-datepicker" v-model="datevalue" class="mb-2 w-50"></b-form-datepicker>
                
                <div>
                    Hour range:
                    <b-form-spinbutton inline wrap min="0" max="23" v-model="hourvalue"></b-form-spinbutton>
                    <b-button class="ml-1" variant="success" @click="createChartData(hourvalue)">v</b-button>
                    <b-button class="ml-1" @click="removeHourRange">x</b-button>
                </div>
                
            </b-form>
        </div>

        <div v-if="getDataStatus === 'PENDING'">
            <b-alert variant="info" show>Getting data...</b-alert>
        </div>
        
        <b-skeleton-wrapper :loading="getDataStatus === 'PENDING'">
            <template #loading>
                <b-card>
                <b-skeleton width="85%"></b-skeleton>
                <b-skeleton width="55%"></b-skeleton>
                <b-skeleton width="70%"></b-skeleton>
                </b-card>
            </template>
            <div class="h-50">
                <DataChart :key="chartkey" :data="data" :labels="labels" :type="'steps'"/>
            </div>
        </b-skeleton-wrapper>
    </div>
</template>


<script>
import DataChart from '@/components/data/DataChart'

const miband_db_host='192.168.11.122'
const miband_db_port='5002'

var today = new Date()

export default {
    components: { DataChart },
    data(){
        return {
            activitydata: {},
            wholedayData: {},
            hourData: {},
            labels: [],
            data: [],
            mode: -1,
            datevalue: today.getFullYear() + '-' + String(today.getMonth()+1) + '-' + today.getDate(),
            hourvalue: null,
            chartkey: false,
            getDataStatus: ''
        }
    },
    mounted(){
        this.getDatabyDate(this.datevalue)
        this.getStepsData()
        // this.createChartData()
        // this.chartkey = !this.chartkey
    },

    watch: {
        datevalue: function() {
            this.getDatabyDate(this.datevalue)
        },
        getDataStatus: function() {
            if(this.getDataStatus=='OK') {
                this.getStepsData()
                this.createChartData()                    
            }
        },
        data: function() {
            this.chartkey = !this.chartkey
        },
    },

    methods: {
        getStepsData() {
            var logs = this.activitydata
            var hourData = {}

            for(var i in logs) {
                var timestamp = logs[i].timestamp
                var tmp = new Date(timestamp)
                var hour = tmp.getHours()
                var minute = tmp.getMinutes()
                // dataOfHour["asd"] = "asd"
                if(hourData[String(hour)]==undefined){
                    hourData[String(hour)] = {}
                    hourData[String(hour)]['sum'] = 0
                }
                var steps = logs[i].steps
                hourData[String(hour)][String(minute)] = steps
                hourData[String(hour)]['sum']+=steps
            }

            var wholedayData = {}
            for(var h=0; h<24; h++){
                if(hourData[h]!=undefined)
                    wholedayData[h] = hourData[h]['sum']
                else  wholedayData[h] = undefined
            }
            this.wholedayData = wholedayData
            this.hourData = hourData
        },

        createChartData(mode) {
            this.labels = []
            this.data = []
            var h
            if(mode==null) {
                for(h=0; h<24; h++) {
                    this.labels.push(String(h)+':00')
                    this.data.push(this.wholedayData[h])
                }
            }
            else {
                h = mode
                var minute
                for(var m=0; m<60; m++) {
                    if (String(m).length<2) {
                        minute = '0'+String(m)
                    }
                    else minute = m
                    this.labels.push(String(h)+':'+String(minute))
                    if(this.hourData[h]!=undefined){
                        var steps = this.hourData[h][m]
                        this.data.push(steps)
                    }
                        
                }
            }

        },

        async getDataByTimeApiCall(start, end) {
            const bandid = this.$session.get('miband').id
            try {
                const response = await fetch(`http://${miband_db_host}:${miband_db_port}/getlogsbytime/${bandid}`, {
                method: 'POST',
                body: JSON.stringify({
                    'start': start,
                    'end': end
                    }),
                headers: { 'Content-type': 'application/json; charset=UTF-8' },
                })
                
                const result = await response.json()
                if(result['get-logs-result']==='succeeded')
                    return result['logs']
                return false
            } catch (error) {
                // do something with `error`
            }
        },

        getDatabyDate(inputdatestr) {
            var date = new Date(inputdatestr)
            var day, month, year, datestr, startstr, endstr
            day = date.getDate()
            month = date.getMonth()+1
            year = date.getFullYear()
            datestr = day + '.' + month + '.' + year
            startstr = datestr + ' - 0:00'
            endstr = datestr + ' - 23:59'
            this.getDataByTimeApiCall(startstr, endstr).then((result)=>{
                this.activitydata  = result 
                this.getDataStatus = "OK"
            })
            this.getDataStatus = "PENDING"

        },

        removeHourRange(){
            this.hourvalue = null
            this.createChartData()
        }
    }
}
</script>