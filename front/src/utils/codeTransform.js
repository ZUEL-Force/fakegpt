
import {clearArr} from "./simpleUtils.js";
import {standardList} from "../config/resloveConfig.js";

/**
 * rawList和组件列表转换
 * @param contentArr
 * @param cpList
 */
function changeCpList(contentArr, cpList){
    clearArr(cpList)
    console.log('清空之后的list',cpList,'传入的rawList',contentArr)
    contentArr.forEach(item=>{
        // console.log('',item)
        let temp1=item.match(/[A-Z]+-/)
        // 没有标识符的默认是MARKDOWN
        let type=!temp1?'MARKDOWN':temp1[0].replace('-','')
        let data=!temp1?item:item.match(/-\S*/)[0].replace('-','')
        standardList.forEach(cp=>{
            if(cp.sign==type){
                let cpInfo={
                    name:cp.name,
                    data:data,
                    sign:cp.sign
                }
                cpList.push(cpInfo)
            }
        })
        return
    })
}

export {
    changeCpList
}
