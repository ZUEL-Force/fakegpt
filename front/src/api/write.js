import {post} from "@/api/env.config";
// import * as url from "url";
import store from "@/store/store";
import {USER_INFO} from "@/store/constant";
function getContact() {
    // return  post({},'/myContact')
return new Promise(resolve => {
    resolve({
        code:0,
        data:store.get(USER_INFO).contact
    })

})
    // return post(data,'/getContact')
}

function sendMailText(data) {
    return post(data, '/receiveMailText')
}

export {sendMailText,getContact}
