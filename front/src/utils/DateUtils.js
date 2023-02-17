// 时间转换
function timestampToTime(timestamp) {
    let date = new Date(timestamp);//时间戳为10位需*1000，时间戳为13位的话不需乘1000
    let Y = date.getFullYear() + '-';
    let M = (date.getMonth()+1 < 10 ? '0'+(date.getMonth()+1) : date.getMonth()+1) + '-';
    let D = date.getDate() + ' ';
    let h = date.getHours() + ':';
    let m = date.getMinutes() + ':';
    let s = date.getSeconds();
    return Y+M+D+h+m+s;
}

/**
 * 读取时间戳转换为年月日（时间戳单位为s）
 * @param timestamp
 */
function getMsgDate(timestamp){
    let date = new Date(timestamp*1000);
    let Y = date.getFullYear() + '-';
    let M = (date.getMonth()+1 < 10 ? '0'+(date.getMonth()+1) : date.getMonth()+1);
    // let D = date.getDate() + ' ';
    return Y+M
}

function setMsgDate(timestamp){
    return timestamp/1000
}

export {timestampToTime,getMsgDate,setMsgDate}
