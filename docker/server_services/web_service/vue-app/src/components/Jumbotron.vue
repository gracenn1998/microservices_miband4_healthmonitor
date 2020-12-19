<template>
    <b-card class="w-75 mx-auto mt-3">
        <div>
            <b-jumbotron>
                <template #header>HEALTH MONITORING</template>

                <template #lead>
                    <p>Miband 4</p>
                    <p>Microservices architecture</p>
                </template>

                <hr class="my-4">

                <div v-if="!this.$session.exists()">
                    <b-button variant="success" class="mr-2">
                        <router-link to="/signup" class="text-light">Sign Up</router-link>
                    </b-button>
                    <b-button variant="primary">
                        <router-link to="/signin" class="text-light">Sign In</router-link>
                    </b-button>
                </div>

                <div v-if="this.$session.exists()" >
                    <b-button variant="success" class="mr-2">
                        <router-link to="/data" class="text-light">Data</router-link>
                    </b-button>
                    <b-button variant="primary">
                        <router-link to="/profile" class="text-light">Profile</router-link>
                    </b-button>
                </div>      

            </b-jumbotron>
        </div>
    </b-card>
</template>