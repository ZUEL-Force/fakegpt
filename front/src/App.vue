<template>
  <router-view/>
</template>
<script>
// import {handleDate} from "@/utils/handeDate";
// import store from "@/store/store";
// import {ACCESS_TOKEN} from "@/store/constant";
// import {onMounted} from "vue";

export default {
  setup(){
    // if(store.get(ACCESS_TOKEN))
    //   handleDate()
  }

}
</script>
<style lang="scss">
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}

#nav {
  padding: 30px;

  a {
    font-weight: bold;
    color: #2c3e50;

    &.router-link-exact-active {
      color: #42b983;
    }
  }
}
</style>
