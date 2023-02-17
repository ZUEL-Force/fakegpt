<template>
<div class="chat">
  <div class="select">
    <contact-popover :list="models" :selected-model="to.name" :show-popover="showModels" @onChange="modelChange"></contact-popover>
  </div>
  <div class="top-bar">
    {{to.name}}
  </div>
<!--  <div class="chat">-->
    <div class="body">
      <chat-body v-if="isReady" ref="chatBody" :msg-list="msgList" :to="to" :my-name="nickName" height="85vh">

      </chat-body>
    </div>
    <div class="input">
      <chat-input @handleMsg="send" @onFocus="handleFocus">

      </chat-input>
    </div>

<!--  </div>-->
</div>
</template>

<script>
import chatInput from "@/components/ChatRoom/chatInput";
import chatBody from "@/components/ChatRoom/chatBody";
import {onMounted, reactive, ref} from "vue";
// import {getInfo} from "@/api/api";
import store from "@/store/store";
import {LAST_DATE, NICK_NAME} from "@/store/constant";
import {getModel, sendMsg} from "@/api/chat";
import {setMsgData,getPrevDate} from "@/utils/msgUtil";
import ContactPopover from "@/components/ChatRoom/contactPopover";
// import {showToast} from "vant";
export default {
  name: "chat",
  components:{
    ContactPopover,
    chatInput,
    chatBody
  },
  setup(){
    // 刚开始的时候加载最近的一天的数据
    let date=store.get(LAST_DATE)
    let msgList=ref([])
    let models=ref([])
    let to=reactive({
      name:'',
      img:''
    })
    let isReady=ref(false)
    let showModels=ref(false)
    // 模型部分
    async function initModels(){
      //TODO:请求模型数据
       let r=await getModel() .catch(err=>{
         models.value=[]
         to.name='unKnown'
         console.log('modelList',err)
       })
           // .then(r=>{
        // console.log()
        console.log('models',r)
        r.data.msg.models.forEach(model=>{
          models.value.push({text:model.name,img:model.img})
        })
        to.name=models.value[0].text||'unKnown'
        to.img=models.value[0].img
        isReady.value=true

    }
    function modelChange(newModel){
      console.log('子组件给的action',newModel)
      to.name=newModel.text
      to.img=newModel.img
      // to.img=
    }
    if(date)
    msgList=ref(store.get(date).list)
    console.log('页面加载，初始化的数据',msgList.value)
    const chatBody=ref()
    const nickName=store.get(NICK_NAME)
    // const userInfo=store.get(USER_INFO)
    // store.set(NICK_NAME,'GuangGe')

    /**
     * 监听聚焦事件
     */

    function handleFocus(){
      console.log(chatBody)
      // setTimeout(()=>{
        chatBody.value.toBottom()
      // },1000)
    }

    function formatMsg(msg){

      return {
        time:Math.round(new Date().getTime()/1000),
        question: msg,
        from:nickName,
        to:to.name
      }
    }
    /**
     * 处理返回的信息
     * @param data
     */
    function handleRes(data){
      setMsgData(data.msg)
      msgList.value.push(data.msg)
    }

    initModels()

    // onMounted(()=>{
    // })
    return{
      title:'ChatGPT',
      msgList,
      chatBody,
      nickName,
      models,
      showModels,
      modelChange,
      handleFocus,
      isReady,
      to,
      send:(e)=>{
        //这里写发送消息给后端的接口
        let msg=formatMsg(e)
        setMsgData(msg)
        msgList.value.push(msg)
        //TODO:加载效果
        // 1-已发送;2-发送失败；3-发送中
        // Object.assign(msg,{status:SENDING})
        // setTimeout(()=>{
        //
        // })
        //   handleRes({
        //     status:true,
        //     msg:{
        //       answer:'回答',
        //       time:new Date().getTime()/1000
        //     }
        //   })

        sendMsg(msg).then(r=>{
          console.log('后端返回的的数据',r)
          handleRes(r.data)
          // console.log('r',r)
        })

      }
    }
  }
}
</script>

<style scoped>
.chat{
  height: 100vh;
}
.top-bar{
  height: 6vh;
  background-color: black;
  font-size: 18px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  color: bisque;
}
.body{
  height: 84vh;
  background-color: #2c3e50;
}
.input{
  /*position: fixed;*/
  /*bottom: 0;*/
  height: 10vh;
  /*background-color: #2c3e50;*/
}
.select{
  /*height: 3vh;*/
  /*background-color: #fff2e2;*/
  position: absolute;
  top: 10px;
  left: 10px;
}

</style>
