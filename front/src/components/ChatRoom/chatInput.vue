<template>
<div class="input">
  <van-field v-model="myInput"
             rows="1"
             autosize
             type="textarea"
             maxlength="200"
             placeholder="请输入问题"
             @focus="onFocus"
  >
    <template #button>
      <van-button size="small" type="primary" @click="handleMsg()">发送</van-button>
    </template>
  </van-field>
</div>
</template>

<script>
import {ref} from "vue";
import {showToast} from "vant";
// import storage from "@/store/store";

export default {
  name: "chatInput",
  setup(props,ctx){
      console.log(props)
    let myInput=ref('')
    function validate(text){
      return text.replace(/(^\s+)|(\s+$)|\s+/g, "") !== '';
    }
    function onFocus(){
      ctx.emit('onFocus')
    }
    function handleMsg(){
        if(validate(myInput.value))
          // console.log('验证格式正确',myInput.value)
        ctx.emit('handleMsg',myInput.value)
      else {
        showToast('请输入文本内容')
        }
        myInput.value=''
    }
    return{
        myInput,
      handleMsg,
    onFocus
    }

  }
}
</script>

<style scoped>

</style>
