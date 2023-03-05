//会话模块
import store from "@/store/store";
import {CURRENT_SESSION, LAST_DATE, MSG_CACHE, SESSIONS} from '@/store/constant'
import {getMsgData} from "@/utils/msgUtil";
import {defaultContact} from "@/view/pageConfig/config";
export function getSessions(){
    return store.get(SESSIONS)
}

/**
 * 添加成功返回true
 * 添加失败返回false
 * @param session
 */
export function addSession(session){
    let list=getSessions(SESSIONS)
    if(!list){
        list=[session]
        store.set(SESSIONS,list)
        return list
    }
    list.unshift(session)
    store.set(SESSIONS,list)
        return list
}
export function delSessions(session){
    let list=getSessions()
    let newList=list.filter(item=>{
        return item.name!==session.name
    })
    store.set(SESSIONS,newList)
    return newList
}
export function getCurrentSession(){
    return store.get(CURRENT_SESSION)
}
export function setCurrentSession(sessionName){
    store.set(CURRENT_SESSION,sessionName)
}


// 消息模块

// 获取CacheMessage
export function getMsgCache(){
   return  store.get(MSG_CACHE)
}
//注入CacheMessage
export function setMsgCache(msg){
    let list=getMsgCache()
    if(!list)
        list=[msg]
    else{
        list.push(msg)
    }
    store.set(MSG_CACHE,list)
}

//清除CacheMessage
export function removeMsgCache(){
    store.remove(MSG_CACHE)
}

export function getSessionMsg(option){
    let msgCache =getMsgCache()
    const sysMsg={
        role:defaultContact.system,
        content:option.character
    }
    let messages=[]
    messages.push(sysMsg)
    msgCache.filter(item=>{
        return item.contact===option.name
    }).forEach(msg=>{
        let Msg={
            //是否是助手消息
            role:msg.to===option.me?defaultContact.assistance:defaultContact.user,
            content:msg.to===option.me?msg.answer:msg.question
        }
        messages.push(Msg)
        console.log('sessionMsg',Msg)
    })
    return {
        to:option.to,
        from:option.me,
        messages:messages,
        time:Math.round(new Date().getTime()/1000),
        contact:option.name
    }

}

export function getSessionMessages(session){
    let msgList=getMsgData(LAST_DATE).filter(msg=>{
        return msg===session
    })
    return getSessionMsg(msgList)
}
