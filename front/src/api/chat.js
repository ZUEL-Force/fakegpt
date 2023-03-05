import {formPost, post,longPost} from "@/api/env.config";

function sendMsg(data){
    return longPost(data,'/talk/')
}
function uploadImg(file){
    return formPost(file,'/updateface/')
}
function getFace(data){
    return post(data,'/getface/')
}
function create(data){
    return post(data,'/create/')
}
function getModel(){
    return post({},'/getmodel/')
}

export {sendMsg,uploadImg,create,getFace,getModel}
