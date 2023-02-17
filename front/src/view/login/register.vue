<template>
  <div class="container">
    <div class="logo">
      <a-upload
          v-model:file-list="img"
          name="avatar"
          :customRequest="aRead"
          list-type="picture-card"
          :beforeUpload="bRead"
          @preview="handlePreview"
          :max-count="1"
      >
        <div  v-if="img.length < 1">
          <bug-outlined spin />
          <div style="margin-top: 8px;color: #556574">上传</div>
        </div>
      </a-upload>
<!--      <ZUELForce></ZUELForce>-->
    </div>
    <a-modal :visible="previewVisible" :footer="null" @cancel="handleCancel">
      <img style="width: 100%" :src="previewImg" />
    </a-modal>
    <div class="form">
      <!--      <van-form>-->
      <van-cell-group inset>
        <div class="field">
          <van-field
              v-model="form.name"
              name="昵称"
              label="昵称"
              placeholder="输入昵称"
              :rules="[{ required: true, message: '请输入昵称' }]"
          />
        </div>

        <div class="field">
          <van-field
              v-model="form.password"
              name="密码"
              label="密码"
              type="password"
              placeholder="输入密码"
              :rules="[{ required: true, message: '请填写密码' }]"
          />

        </div>
      </van-cell-group>
      <div class="submit" @click="onSubmit">
        <!--          <span class="btn">提交</span>-->
        <!--          <van-button color="#7232dd" class="btn" plain >打开</van-button>-->
        <div class="btn">
          <!--            <van-image width="20vw" :src="loginIcon" @click="onSubmit"></van-image>-->
          <van-button>注册</van-button>
        </div>

      </div>
      <!--      </van-form>-->

    </div>
  </div>
</template>

<script>

import {Upload, Modal} from 'ant-design-vue'
import {BugOutlined} from '@ant-design/icons-vue'

// import store from "@/store";
// import {getBase64} from "@/utils/img";
import router from "@/router";
import 'ant-design-vue/es/upload/style/css';
import 'ant-design-vue/es/modal/style/css';
// import ZUELForce from '@/components/logo'
import {reactive, ref} from "vue";
import {showToast} from "vant";
import {create} from "@/api/chat";
// import pageConfig from "@/views/config/page.config";
export default {
  name: "register",
  components: {
    // ZUELForce
    AModal: Modal,
    AUpload: Upload,
    BugOutlined
  },
  setup() {
    const loginState = {
      loading: false,
    }
    let previewVisible = ref(false)
  let previewImg=ref('')
    let form = reactive({
      name: '',
      password: '',
      img:{}
    })
    let img = ref([
      // {
      //   uid:1,
      //   name:'logo.png',
      //   status: 'done',
      //   url:'E:/code/chatGTP/src/assets/avatar/logo.png'
      //
      // },
      // {
      //   uid: '-1',
      //   name: 'image.png',
      //   status: 'done',
      //   url: 'https://zos.alipayobjects.com/rmsportal/jkjgkEfvpUPVyRjUImniVslZfWPnJuuZ.png',
      // }
    ])

    function bRead(file) {
      // console.log('file', typeof file.file,file.file)
      if (file.type !== 'image/jpeg' && file.type !== 'image/png') {
        showToast('请上传 jpg或者png 格式图片');
        return false;
      }
      return true;
    }

    function aRead(data) {
      return new Promise(resolve => {
        console.log('myfile', data.file)
        // img.value[0]
       form.img=data.file
        let tempUrl = URL.createObjectURL(data.file)
        img.value[0] = {
          id: -1,
          url: tempUrl,
          name: 'ZOO.png'
        }
        console.log('formData', URL.createObjectURL(data.file),img.value)
        resolve(data.file)
      })

    }
    const handlePreview =  async () => {
      previewImg.value=img.value[0].url
      previewVisible.value = true;
      // previewTitle.value = file.name || file.url.substring(file.url.lastIndexOf('/') + 1);
    };
    function handleCancel() {
      previewVisible.value = false
    }

    const onSubmit = () => {
      // console.log('提交的数据', e)
      loginState.loading = true
      if (!img.value[0]) {
        showToast('请上传头像')
        return false
      }
      let formData=new FormData()
      formData.append('img',form.img)
      formData.append('name',form.name)
      formData.append('password',form.password)

      create(formData).then(() => {
        form.img={}
        form.name=''
        form.password=''

        router.push({path:'/login'})
      })
    }


    return {
      onSubmit,
      form,
      img,
      aRead,
      bRead,
      previewVisible,
      previewImg,
      handleCancel,
      handlePreview
      // loginIcon:pageConfig.image.earphone
    }
  }
}
</script>

<style scoped>


.container {
  height: 100vh;
  /*background: url("../assets/background/5.jpg") no-repeat;*/
  background:linear-gradient(60deg, #334185,#70807f,black,#556574,#7d7687);
  background-size: 100% 100%;

  display: flex;
  flex-direction: column;
  /*justify-content: center;*/
  align-items: center;
  justify-content: space-around;
}

.logo{
  width: 40vw;
  height: 40vw;
  /*border-radius: 20px;*/
  margin-top: 20px;
  /*background-color:;*/
  /*box-shadow: #0e0e0e 5px 1px;*/
}
.form{
  padding-bottom: 40vh;

}
.field{
  height:auto;
  /*background-color: #42b983;*/
}
.submit{
  width: 100vw;
  height: 10vh;
  margin-top: 40px;
  display: flex;
  justify-content: center;
  align-items: center;

  /*background-color: aliceblue;*/
}

.btn{
  font-size: 16px;
  /*width: 20vw;*/
  /*height: 20vw;*/
  border-radius: 25%;
  padding: 0 0 5px 5px;
  color: #2c3e50;
  /*border-radius: 5px;*/
  /*background-color: aliceblue;*/
}
</style>
