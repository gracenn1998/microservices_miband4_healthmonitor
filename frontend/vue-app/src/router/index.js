import Vue from 'vue'
import VueRouter from 'vue-router'
Vue.use(VueRouter)


export default new VueRouter({
    mode: 'history',
    routes: [
        {
            path: '/',
            name: 'homepage',
            component: () => import('@/components/Jumbotron.vue')
        },
        {
            path: '/signup',
            name: 'signup',
            component: () => import('@/components/account/SignUpForm.vue')
        },
        {
            path: '/signin',
            name: 'signin',
            component: () => import('@/components/account/SignInForm.vue')
        },
        {
            path: '/profile',
            name: 'profile',
            component: () => import('@/components/account/Profile.vue')
        },
        {
            path: '/profile/edit',
            name: 'profile-edit',
            component: () => import('@/components/account/EditForm.vue')
        },
        {
            path: '/data',
            name: 'data',
            component: () => import('@/components/Data.vue')
        },
    ]
})