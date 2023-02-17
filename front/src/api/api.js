import {post} from "@/api/env.config";

function login (data){
    return post(data,'/login/')
}

function getInfo(data){
    return post(data,'/getInfo')
}
function logout(data){
    return post(data,'/logout')
}
function getMailText(data){
    return post(data,'/sendMailText')

}
function getMailList(data){
    return post(data,'/mailList')
}
function getMyMail(data){
    return post(data,'/myMail')
}
function getAMail(data){
    return post(data,'/aMail')
}
function delAMail(data){
    return post(data,'/delAMail')
}
function sendBlogText(data){
    return post(data,'/receiveBlogText')
}
function getWechatMsg(data){
    return post(data,'/sendWechatMsg')
}
function getBlogText(data){
    return post(data,'/sendBlogText')
}
function getVideo(data){
    console.log(data)
}


export {login,logout,getInfo,getWechatMsg,getMailText,getBlogText,getMailList,getAMail,sendBlogText,getVideo,getMyMail,delAMail}
