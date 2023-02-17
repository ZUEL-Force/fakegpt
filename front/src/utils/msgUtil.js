import store from "@/store/store";
import {getMsgDate} from "@/utils/DateUtils";
import {LAST_DATE} from "@/store/constant";

/**
 * 把消息放入缓存中
 * @param msg
 * msgList:{
 *   list,
 *   prev:lastDate
 * }
 */

function setMsgData(msg){
    //如果本条消息存在归属日期，就放入该日期中
    if(store.get(getMsgDate(msg.time))){
        let msgList=store.get(getMsgDate(msg.time))
        msgList.list.push(msg)
        //将消息记录重新回填缓存
        store.set(getMsgDate(msg.time),msgList)
    }
    //如果没找到归属日期，就建立归属日期，不过要先确认是否存在上一次的日期（即是否存在初始日期）
    else {
        //如果存在上一日期，就新建本日期并将指针指向上一日期
        if(store.get(LAST_DATE)){
            let msgList={
                prev:store.get(LAST_DATE),
                list:[]
            }

            msgList.list.push(msg)
            //将消息记录重新回填缓存
            store.set(getMsgDate(msg.time),msgList)
            // 更新最新日期：
            store.set(LAST_DATE,getMsgDate(msg.time))
        }
        //如果没有最新日期说明还没消息,此消息为第一条消息，创建 last_date；并指向指针为-1
        else {
            let msgList={
                list:[],
                prev:-1
            }
            msgList.list.push(msg)
            store.set(getMsgDate(msg.time),msgList)
            store.set(LAST_DATE,getMsgDate(msg.time))

        }

    }

}

/**
 * 通过时间返回缓存中的消息列表
 * @param date
 * @returns {*}
 */
function getMsgData(date){
    return store.get(date).list
}

/**
 * 获取date前一天的消息记录
 * @param date
 * @returns {boolean|*}
 */
function getPrevDate(date){
    let prevDate=store.get(date).prev
    // 如果拿到的prevDate为空或者为-1
    if(!prevDate||prevDate===-1){
        return []
    }
    return store.get(prevDate).list
}



export {getMsgData,getPrevDate,setMsgData}
