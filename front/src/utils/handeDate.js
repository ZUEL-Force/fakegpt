import storage from "@/store/store";
import {DAY_GAP, LAST_UPDATE} from "@/store/constant";
import store from "@/store";
// import {getInfo} from "@/api/api";



function handleQuote(){
    const now=new Date().getTime()
    console.log('time',now)
    if(!storage.get(LAST_UPDATE)){
        storage.set(LAST_UPDATE,now)
        store.dispatch('GetInfo').then((res)=> {
            console.log('用户信息', res)
            return
        })
    }

    let lastUpdate=storage.get(LAST_UPDATE)
    if(now-lastUpdate>DAY_GAP){
        storage.set(LAST_UPDATE,now)
        store.dispatch('GetInfo').then((res)=>{
            console.log('用户信息',res)
        })
    }
}
 function handleDate(){
    // store.dispatch('GetInfo').then(r=>{
    //     console.log('GETinfo',r)
    // })

}

export {handleDate,handleQuote}
