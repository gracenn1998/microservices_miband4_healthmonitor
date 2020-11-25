<template>
  <div>
    <b-card >
      <b-form inline>
        <label class="sr-only" for="inline-form-input-name">Name</label>
        <b-form-input
          id="inline-form-input-name"
          class="mb-2 mr-sm-2 mb-sm-0"
          placeholder="Mac address"
        ></b-form-input>

        <label class="sr-only" for="inline-form-input-username">Username</label>
        <b-input-group prepend="🔑" class="mb-2 mr-sm-2 mb-sm-0">
          <b-form-input id="inline-form-input-username" placeholder="Authentic key"></b-form-input>
        </b-input-group>
        <b-button variant="primary">Pair</b-button>
      </b-form>
    </b-card>
  </div>
</template>