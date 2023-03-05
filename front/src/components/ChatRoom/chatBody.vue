<template>
<div class="body" id="chatBody" :style="{maxHeight: $props.height}">
<!--  显示消息为当前模型的对话记录-->
<div class="msg" v-for="msg in msgList" :key="msg.time" >
  <div class="me" v-if="msg.from===$props.myName &&msg.contact===$props.session">
    <van-image
        width="30px"
        height="30px"
        round
        fit="cover"
        position="center"
        :src="myAvatar"
    />

    <div class="myPo">
      {{msg.question}}
    </div>

  </div>
  <div class="from" v-else-if="msg.contact===$props.session">
    <van-image
        width="30px"
        height="30px"
        round
        :src="youAvatar"
    >
      <template v-slot:loading>
        <van-loading type="spinner" size="20" />
      </template>
    </van-image>
    <div class="youPo">
      {{msg.answer}}
    </div>
    <van-loading v-show="msg.isloding" type="spinner" size="20px" color="#1989fa" />


  </div>

</div>
</div>
</template>

<script>
// import {imgs} from "@/view/pageConfig/config";
import {nextTick, onMounted, defineExpose, ref, watch} from "vue";
import store from "@/store/store";
import {MY_AVATAR} from "@/store/constant";
import {getImgPath} from "@/utils/img";

export default {
  name: "chatBody",
  props:{
    msgList:{
      type:Array,
      require:true
    },
    myName:{
      type:String,
      require: true
    },
    to:{
      type:Object,
      require: true
    },
    height:{
      type:String,
      require:true
    },
    session:{
      type:String,
      require:true
    }
  },

  setup(props){
    let youAvatar=ref(getImgPath(props.to.img))
    let myAvatar=ref(getImgPath(store.get(MY_AVATAR)))
    console.log('setup我的头像的对方头像',myAvatar.value,youAvatar.value)

    function toBottom(){
      let msg = document.getElementById('chatBody') // 获取对象
      msg.scrollTop = msg.scrollHeight // 滚动高度
      // console.log('height',msg)
    }
    const chatBody=ref({})
    watch(props.msgList,()=>{
      nextTick(() => {
        toBottom()
      })
    })
    // function setAvatar(){
    //   youAvatar.value=getImgPath(props.to.img)
    //   myAvatar.value=getImgPath(store.get(MY_AVATAR))
    // }
    // onMounted(()=>{
    //   // nextTick(()=>{
    //     setAvatar()
    //   // })
    // })

    defineExpose({
      toBottom
    })
    onMounted(()=>{
      toBottom()
    })

    // const imgError=(sign)=>{
    //   console.log('图片加载出错！')
    //   if(sign.code===1)
    //     youAvatar=imgs.chatGPT
    //   else if (sign.code===2)
    //   myAvatar=imgs.google
    //   console.log('我的头像的对方头像',myAvatar.value,youAvatar.value)
    // }
    return{
      youAvatar,
      myAvatar,
      chatBody,
      toBottom,
      // imgError
    }
  }
}
</script>

<style scoped>

.body{
  color: black;
  display: flex;
  flex-direction: column;
  overflow-x: hidden;
  overflow-y: scroll;
  font-size: 16px;
}
.body::-webkit-scrollbar {
  display: none;
}
/*.msg{*/
/*  padding: 1vw;*/
/*  !*max-width: 80vw;*!*/
/*}*/
.me{
  float: right;
  display: flex;
  flex-direction: row-reverse;
  align-items: flex-start;
  margin: 10px 0;
}
.myPo{
  text-align: left;
  background-color: #42b983;
  padding: 0.4em;
  margin-right: 6px;
  border-radius: 5px;
  max-width: 14em;
  /*text-wrap: ;*/
}
.youPo{
  text-align: left;
  text-wrap: normal;
  word-wrap: break-word;
  background-color: #eeeeee;
  padding: 10px;
  margin-left: 6px;
  border-radius: 5px;
  max-width: 14em;
  width: auto;
}
.from{
  float: left;
  display: flex;
  justify-content: left;
  align-items: flex-start;
  margin: 10px 0;

}
</style>
