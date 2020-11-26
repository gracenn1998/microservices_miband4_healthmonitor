<template>
<div>
  <b-navbar toggleable="lg" type="dark" variant="dark">
    <b-avatar text="MB4" size="3em"></b-avatar>
    <b-navbar-toggle target="nav-collapse"></b-navbar-toggle>

    <b-collapse id="nav-collapse" is-nav>
      <b-navbar-nav>
        <b-nav-item href="#">Link</b-nav-item>
        <b-nav-item href="#" disabled>Disabled</b-nav-item>
      </b-navbar-nav>

      <!-- Right aligned nav items -->
      <b-navbar-nav class="ml-auto">
        <div>
          <b-button variant="outline-primary">
            <router-link to="/signup">Sign Up</router-link>
          </b-button>
          <b-button variant="outline-primary">
            <router-link to="/edit/accountinfo">Sign In</router-link>
          </b-button>
        </div>      
      </b-navbar-nav>
    </b-collapse>
  </b-navbar>
</div>
</template>

<script>
export default {
    
}
</script>

<style scoped>

</style>