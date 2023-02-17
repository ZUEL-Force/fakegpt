<template>
  <van-image class="back" :src="back" width="40px" @click="goBack"></van-image>
</template>
<script>
import pageConfig from "@/views/config/page.config";
import router from "@/router";
export default {
  name: "index",
  setup(){
    return{
      goBack:()=>{
        router.go(-1)
      },
      back:pageConfig.image.back
  }
  }
}
</script>

<style scoped>

</style>
