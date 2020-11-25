<template>
  <div id="app">
    <Navbar />
    <Sidebar />
    <router-view />
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
  components: {
    Navbar,
    Sidebar,
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
