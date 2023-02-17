<template>
  <div class="picker">
    <van-popover offset="[1.10]" theme="dark" v-model:show="$props.showPopover" :actions="$props.list" @select="onSelect">
      <template #reference>
        <van-tag  color="#ffe1e1" text-color="#ad0000" plain round medium> <div class="tag">{{ $props.selectedModel === '模型' ? '' : $props.selectedModel}}</div> </van-tag>
      </template>
    </van-popover>
  </div>
</template>

<script>
// import {ref} from "vue";

export default {
  name: "contactPopover",
  props:['showPopover','list','selectedModel'],

  setup(props,ctx){
    const onSelect = (action) => {
      ctx.emit('onChange',action)
    }
    return{
      onSelect,

    }
  }
}
</script>

<style scoped>
.picker{
  text-align: center;
  line-height: 3vh;
}
.tag{
  font-size: 2vh;
  height: 3vh;

}
</style>
