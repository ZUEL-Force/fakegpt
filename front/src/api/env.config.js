import axios from 'axios'
import {ACCESS_TOKEN, ID} from "@/store/constant";
import {showFailToast} from "vant";
import storage from "@/store/store";
import router from "@/router";
import {stringify} from "qs";

const baseUrl = process.env.VUE_APP_API_HOST
const request = axios.create({
    baseURL: baseUrl,
    timeout: 30000
})


function post(data, url) {
    return request({
        url: url,
        method: 'post',
        data
    })

}
function formPost(data,url){
    return request({
        url: url,
        method: 'post',
        data,
        // transformRequest: [
        //     function (data) {
        //         // 将请求数据转换成功 formdata 接收格式
        //         return stringify(data)
        //     }
        // ],
        headers: {
            "Content-Type": 'multipart/form-data',
            'X-Requested-With': 'XMLHttpRequest'
        }

    })
}

// function post(data,url){
//     return request({
//         url:url,
//         method:'post',
//         data,
//         transformRequest: [
//             function (data) {
//                    let token= storage.get(ACCESS_TOKEN)
//                 if(data)
//                 {
//                     Object.assign(data,{zooToken:token})
//                 }
//                 else {
//                     data={
//                         zooToken: token
//                     }
//                 }
//                 // 在请求之前对data传参进行格式转换
//                 return JSON.stringify(data)
//             }
//         ]
//         // headers: {
//         //     // 内容类型
//         //     'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
//         //     // Ajax请求
//         //     'X-Requested-With': 'XMLHttpRequest'
//         // }
//
//         })
// }
function get(data, url) {
    return request({
        url: url,
        method: 'get',
        data
    })
}

// 异常拦截处理器
const errorHandler = (error) => {
    console.log(error) // for debug
    showFailToast('无法连接服务')
    return Promise.reject(error)
}

// request interceptor
request.interceptors.request.use(config => {
    const token = storage.get(ACCESS_TOKEN)
    const id=storage.get(ID)
    // console.log('请求拦截器',config)
    // 如果 token 存在
    // 让每个请求携带自定义 token 请根据实际情况自行修改
    if (token) {
        // config.headers[ACCESS_TOKEN] = token
        Object.assign(config.data,{token:token,id:id})
    }
    return config
}, errorHandler)

// response interceptor
request.interceptors.response.use((res) => {
// const res = response.data

if (res.data.state!==0) {
    showFailToast(res.msg)
    if(res.data.state===2)
    {
        storage.remove(ACCESS_TOKEN)
        router.go(0)
    }
    return Promise.reject(new Error(res.msg || 'Error'))
} else {
    return res
}
}, errorHandler)


export {post, get,formPost}
