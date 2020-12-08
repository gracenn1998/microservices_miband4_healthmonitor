<template>
<div>
  <b-navbar toggleable="lg" type="dark" variant="dark">
    <b-avatar text="MB4" size="3em"></b-avatar>
    <b-navbar-toggle target="nav-collapse"></b-navbar-toggle>

    <b-collapse id="nav-collapse" is-nav>
      <b-navbar-nav v-if="this.$session.exists()">
        <b-nav-item>
          <router-link to="/profile" class="text-light">Profile</router-link>
        </b-nav-item>
        <b-nav-item>
          <router-link to="/data" class="text-light">Data</router-link>
        </b-nav-item>
      </b-navbar-nav>

      <!-- Right aligned nav items -->
      <b-navbar-nav class="ml-auto">
        <div v-if="!this.$session.exists()">
          <b-button variant="success" class="mr-2">
            <router-link to="/signup" class="text-light">Sign Up</router-link>
          </b-button>
          <b-button variant="primary">
            <router-link to="/signin" class="text-light">Sign In</router-link>
          </b-button>
        </div>
        <div v-if="this.$session.exists()" >
          <!-- <b-button variant="success" class="mr-2 ">
            <router-link to="/profile" class="text-light">Profile</router-link>
          </b-button> -->
          <b-button variant="danger" @click="signout">Sign Out</b-button>
        </div>      
      </b-navbar-nav>
    </b-collapse>
  </b-navbar>
</div>
</template>

<script>
export default {
  methods: {
    signout() {
      this.$session.destroy()
      this.$emit("loginStatusChange")
      this.$router.push('/')
    }
  }
}
</script>