import {createRouter, createWebHashHistory} from 'vue-router'
// import Home from '../views/Home.vue'
/*
import {DEFAULT_INDEX_TOOL} from "@/store/constant";
import Index from '@/views/Index.vue'
import Mail from "@/views/Mail.vue"
import Microphone from "@/views/Microphone.vue";
import User from "@/views/User.vue";
import More from "@/views/more.vue"
import Read from '@/views/read.vue'
import Write from '@/views/write.vue'
import Login from '@/views/login.vue'
import MailList from "@/views/mailList";
import ReadPage from "@/views/readPage";
import My from '@/views/my'
 */

import Chat from '@/view/chat/chat.vue'
import Index from '@/view/index.vue'
import Login from '@/view/login/login'
import Register from '@/view/login/register'
const routes=[
    {
        path: '/',
        name: 'Index',
        component: Index,
        redirect:'/chat',
        children:[
            {
                path:'/chat',
                name:"Chat",
                component:Chat
            }
        ]
    },
    {
        path: '/login',
        name: "Login",
        component: Login
    },
    {
        path: '/register',
        name:'Register',
        component: Register
    }
]

const router = createRouter({
    mode: 'hash',
    history:createWebHashHistory(),
    routes
})

export default router
