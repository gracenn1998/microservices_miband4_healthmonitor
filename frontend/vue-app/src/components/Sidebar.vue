<template>
<div >
  <b-nav vertical id="sidebar">
    <b-nav-item><router-link to="/data">Data</router-link></b-nav-item>
    <b-nav-item><router-link to="/device">Device</router-link></b-nav-item>
    <b-nav-item>Community</b-nav-item>
    <b-nav-item disabled>Disabled</b-nav-item>
  </b-nav>
</div>
</template>

<style scoped>
#sidebar {
    background-color:Gainsboro;
    height: 100vh;
    width: 15vw;
    float: left;
}
</style>