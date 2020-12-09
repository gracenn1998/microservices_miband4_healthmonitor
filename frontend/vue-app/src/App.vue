<template>
  <div id="app">
    <Navbar :key="navKey" @login-status-change="loginUpdate"/>
    <!-- <Sidebar v-if="this.$session.exists()"/> -->
    <router-view @login-status-change="loginUpdate"/>
    <!-- <PairDeviceForm />
    <Data />
    <SignUpForm />
    <DeviceList /> -->
  </div>
  
</template>

<script>
import Navbar from './components/Navbar'
// import Sidebar from './components/Sidebar'
export default {
  name: 'app',
  data() {
    return {
      navKey: false
    }
  },
  components: {
    Navbar,
    // Sidebar,
  },
  methods: {
    loginUpdate() {
      this.navKey = !this.navKey
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