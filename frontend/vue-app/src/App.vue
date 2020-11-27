<template>
  <div id="app">
    <Navbar :key="navKey" @loginStatusChange="loginUpdate"/>
    <Sidebar />
    <router-view @loginStatusChange="loginUpdate"/>
    <!-- <PairDeviceForm />
    <Data />
    <SignUpForm />
    <DeviceList /> -->
  </div>
  
</template>

<script>
import Navbar from './components/Navbar'
import Sidebar from './components/Sidebar'
// import PairDeviceForm from './components/PairDeviceForm'
// import DeviceList from './components/DeviceList'
export default {
  name: 'app',
  data() {
    return {
      navKey: 0
    }
  },
  components: {
    Navbar,
    Sidebar,
  },
  methods: {
    loginUpdate() {
      console.log('helo???')
      this.navKey+=1
      this.$forceUpdate
    }
  }
}
</script>


<style>
/* #app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
} */
</style>