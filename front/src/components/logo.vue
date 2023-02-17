<template>
<div class="logo">
  <van-image class="shadow" round width="40vw" height="40vw" :src="logo"></van-image>
  <div class="text">ZUEL Force</div>
</div>
</template>

<script>
// import store from "@/store/store";
// import {MY_AVATAR} from "@/store/constant";
const logo=require('@/assets/avatar/logo.png')
export default {
  name: "logo",
  setup(){
    return{
      // logo:store.get(MY_AVATAR)?store.get(MY_AVATAR):logo
      logo
    }
  }
}
</script>

<style scoped>
.text{
  font-size: 42px;
  color: darkgoldenrod;
  font-weight: 700;
}
.shadow{
  box-shadow: black 10px 3px 20px;
}
</style>
