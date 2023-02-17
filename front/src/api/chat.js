import {formPost, post} from "@/api/env.config";

function sendMsg(data){
    return post(data,'/talk/')
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
