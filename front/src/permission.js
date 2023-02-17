import {ACCESS_TOKEN} from "@/store/constant";
import router from './router'
// import {createApp} from "vue";
// import {Toast} from "vant";
import storage from 'store'
// import store from './store'

const loginRoutePath = '/login'
// const casLoginRoutePath = '/cas/login'
// /cas/login
const whiteList = ['Login', 'login', 'Register','/'] // no redirect whitelist
const defaultRoutePath = '/'

router.beforeEach((to, from, next) => {
    // to.meta
    // console.log('beforeEach')
    if (storage.get(ACCESS_TOKEN)) {
        console.log('to.path', to.path,storage.get(ACCESS_TOKEN))
        if (to.path === loginRoutePath) {
            next({path: defaultRoutePath})
        } else {

            next()
        }
    } else {
        if (whiteList.includes(to.name)) {
            console.log('在白名单')
            // 在免登录白名单，直接进入
            next()
        } else {
            next({path: loginRoutePath, query: {redirect: to.fullPath}})
            // NProgress.done() // if current page is login will not trigger afterEach hook, so manually handle it
        }
    }
})

router.afterEach(() => {
})
