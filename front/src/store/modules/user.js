import storage from '@/store/store'
import {ACCESS_TOKEN, ID, NICK_NAME, USER_INFO} from "@/store/constant";
import {getInfo, login, logout} from '@/api/api'
import {create} from "@/api/chat";
// 定义user module
const user = {
    //要管理的状态
    state: {
        token: '',
        nickname: '',
        avatarId: '',
        hasGetInfo: false,
        account: '',
        password: '',
        cloudMusicInfo: {},
        info:{},
    },
    //状态的同步更新方法（由commit方法触发）
    mutations: {
        SET_TOKEN: (state, token) => {
            state.token = token
        },
        SET_AVATAR: (state, avatar) => {
            state.avatar = avatar
        },
        SET_NAME: (state, name) => {
            state.name = name
        },
        SET_PASSWORD: (state, password) => {
            state.password = password
        },
        SET_ACCOUNT: (state, account) => {
            state.account = account
        },
        SET_HAS_GET_INFO: (state, hasGetInfo) => {
            state.hasGetInfo = hasGetInfo
        },
        SET_INFO: (state, info) => {
            state.info = info
        },
        RESET_INFO: (state) => {
            state.token = ''
            state.name = ''
            state.info = {}
            state.hasGetInfo = false
            state.welcome = ''
            state.avatar = ''
            storage.remove(ACCESS_TOKEN)
        }
    },
    // 状态的异步更新方法：封装mutations方法，返回Promise对象（由dispatch函数触发）
    actions: {
        // 获取vuex的commit方法更新状态
        Login({commit}, loginInfo) {
            let {account, password} = loginInfo
            return new Promise((resolve,reject) => {
                // let dataJson=JSON.stringify({account: account, password: password})
                login({name: account, password: password}).then(r=> {
                        // 登录成功之后更新vuex和缓存中的token
                        let token = r.data.msg.token
                        let id=r.data.msg.id
                        console.log('拿到的token',token)
                        storage.set(ACCESS_TOKEN, token)
                        storage.set(NICK_NAME,account)
                        storage.set(ID,id)
                        storage.set(USER_INFO,r.data.msg)
                        commit('SET_TOKEN', token)
                        commit('SET_INFO',r.data)
                        resolve()
                })
            }).catch(err => {
                console.log('登录状态更新出错', err)
            })

        },
        // // 获取vuex的commit方法更新状态
        // Create({commit}, createInfo) {
        //     return new Promise((resolve,reject) => {
        //         // let dataJson=JSON.stringify({account: account, password: password})
        //         create(createInfo).then(r=>{
        //
        //         })
        //         console.log('注册成功')
        //     }).catch(err => {
        //         console.log('登录状态更新出错', err)
        //     })
        //
        // },
        // 获取用户信息
        GetInfo({commit}) {
            return new Promise((resolve, reject) => {
                getInfo().then(response => {
                  const { data } = response
                  commit('SET_HAS_GET_INFO', true)
                  commit('SET_NAME', { name: data.username})
                  commit('SET_INFO', data)
                  commit('SET_AVATAR', data.avatar)
                    storage.set(USER_INFO,data)
                  resolve(response)
                }).catch(error => {
                  reject(error)
                })
            })
        },

        // 储存用户信息
        SetInfo({commit}, data) {
            return new Promise((resolve) => {
                commit('SET_PASSWORD', data.password)
                commit('SET_ACCOUNT', data.account)
                resolve(data)
            })
        },
        // 登出
        Logout ({ commit }) {
          return new Promise((resolve) => {
            logout().then(() => {
              commit('RESET_INFO')
              resolve()
            }).catch(() => {
              commit('RESET_INFO')
              resolve()
            })
          })
        },

        // 信息失效
        ResetToken({commit}) {
            return new Promise(resolve => {
                commit('RESET_INFO')
                resolve()
            })
        }

    }
}

export default user
