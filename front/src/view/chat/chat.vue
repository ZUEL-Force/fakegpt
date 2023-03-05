<template>
<div class="chat">
  <div class="select">
    <van-tag size="large" @click="showContact">角色</van-tag>
<!--    <contact-popover :list="models" :selected-model="to.name" :show-popover="showModels" @onChange="modelChange"></contact-popover>-->
  </div>
  <div class="top-bar">
    {{currentContact}}
  </div>
<!--  <div class="chat">-->
    <div class="body">
      <chat-body ref="chatBody"
                 :msg-list="msgList" :to="to" :session="currentContact" :my-name="nickName"
                 height="85vh">

      </chat-body>
     <van-popup v-model:show="showContacts"
                :style="{ width:'50vw', padding: '12px',height:'100%'}"  position="left" class="container-contact">
       <contacts ref="contact" :contacts="contacts"
                 @handelDelContact="delContact"
                 @addContact="addContact"
                 @handleSelect="handleSelect"></contacts>
     </van-popup>
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
import {sendMsg} from "@/api/chat";
import {setMsgData} from "@/utils/msgUtil";
// import ContactPopover from "@/components/ChatRoom/contactPopover";
import {defaultContact} from "@/view/pageConfig/config";
import Contacts from "@/components/contacts/contacts";
import {
  addSession,
  delSessions,
  getCurrentSession,
  getSessionMsg,
  getSessions, removeMsgCache,
  setCurrentSession, setMsgCache
} from "@/view/chat/utils";
export default {
  name: "chat",
  components:{
    Contacts,
    chatInput,
    chatBody
  },
  setup(){
    // 刚开始的时候加载最近的一天的数据
    let date=store.get(LAST_DATE)
    let msgList=ref([])
    let currentContact=ref('')
    // let models=ref([])
    let to=reactive({
      name:defaultContact.model,
      img:defaultContact.modelAvatar
    })
    let contacts=ref([])
    let showModels=ref(false)
    // let me=ref()
    // 模型部分
    /**
     *
     * @returns {Promise<void>}
     * async function initModels(){
     *       //TODO:请求模型数据
     *        let r=await getModel() .catch(err=>{
     *          models.value=[]
     *          to.name='unKnown'
     *          console.log('modelList',err)
     *        })
     *            // .then(r=>{
     *         // console.log()
     *         console.log('models',r)
     *         r.data.msg.models.forEach(model=>{
     *           models.value.push({text:model.name,img:model.img})
     *         })
     *         to.name=models.value[0].text||'unKnown'
     *         to.img=models.value[0].img
     *         isReady.value=true
     *
     *     }
     *  function modelChange(newModel){
     *       console.log('子组件给的action',newModel)
     *       to.name=newModel.text
     *       to.img=newModel.img
     *       // to.img=
     *     }
     */
    //会话部分
    const initSession = () => {
      let selectedId = getCurrentSession()
      //有contacts
      if(getSessions()){
        contacts.value=getSessions()
        console.log('contacts',contacts.value)
      }
      if (!selectedId)
      {
        selectedId = defaultContact.name
        setCurrentSession(defaultContact.name)
      }
      currentContact.value=selectedId
      console.log('init-contact',selectedId)
    }
    let showContacts=ref(false)
    const showContact = () => {
      showContacts.value = !showContacts.value;
    };
    const delContact =(contact) =>{
      // this.contacts=delSessions(contact)
      console.log('删除contact',contact)
      contacts.value=delSessions(contact)
      currentContact.value=getCurrentSession()
    }
    const addContact=(contact)=>{
      contacts.value=addSession(contact)
      console.log('add-contact',contacts.value)
    }
    const handleSelect=(name)=>{
      currentContact.value=name
      console.log('chat-current-change',currentContact.value)
    }
    const getCharacter=()=>{
      if(currentContact.value===defaultContact.name)
        return defaultContact.character
      return contacts.value.find(item=>{
        return item.name===currentContact.value
      }).character
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
        question:msg,
        from:nickName,
        to:to.name,
        contact:currentContact.value
      }
    }
    /**
     * 处理返回的信息
     * @param data
     */
    function handleRes(data){
      let msg=Object.assign(data.msg,{contact:currentContact.value})
      setMsgData(msg)
      setMsgCache(msg)
      msgList.value.push(msg)
    }

    onMounted(()=>{
      removeMsgCache()
    })
    initSession()
    return{
      title:'ChatGPT',
      msgList,
      chatBody,
      nickName,
      showModels,
      handleFocus,
      to,
      contacts,
      showContacts,
      showContact,
      delContact,
      addContact,
      handleSelect,
      currentContact,
      send:(e)=>{
        //这里写发送消息给后端的接口
        let msg=formatMsg(e)
        setMsgData(msg)
        setMsgCache(msg)
        msgList.value.push(msg)
        //获取当前会话的聊天话题
        let messages=getSessionMsg({character:getCharacter(currentContact.value),
          name:currentContact.value,
          me:nickName,
          to:to.name
        })
        sendMsg(messages).then(r=>{
          console.log('后端返回的数据',r)
          handleRes(r.data)
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
  position: absolute;
  top: 10px;
}
/*.container-contact{*/
/*  height: 100%;*/
/*}*/

</style>
