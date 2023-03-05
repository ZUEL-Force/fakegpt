<template>
  <div class="container">
    <div class="cell" :id="sys.name" @click="handleSelect(sys.name)">
      <div class="title">{{ sys.name }}</div>
      <div class="character">{{ sys.character }}</div>
    </div>
    <div class="contact" v-for="item in $props.contacts" :key="item.name">
      <van-swipe-cell>
        <div class="cell" :id="item.name" @click="handleSelect(item.name)">
          <div class="title">{{ item.name }}</div>
          <div class="character">{{ item.character }}</div>
        </div>
        <template #right>
          <van-button class="del" square type="danger" text="删除会话" @click="del(item)"/>
        </template>
      </van-swipe-cell>
    </div>
    <div class="addInfo" v-show="showAdd">
      <div class="label">名称
        <van-field class="input"
                   v-model="newContact.name"
                   maxlength="6"
                   show-word-limit
        ></van-field>
      </div>
      <div class="label">设定
        <van-field class="input" type="textarea"
                   v-model="newContact.character"
                   maxlength="100"
                   show-word-limit
        />
      </div>
      <div class="btn">
        <van-tag color="blue" @click="add">确认</van-tag>
        <van-tag color="red" @click="cancelAdd">取消</van-tag>
      </div>
    </div>
    <div class="add-icon" v-show="!showAdd">
      <van-icon name="add" size="50px" @click="handleShowAdd"></van-icon>
    </div>
  </div>
</template>

<script>
import { nextTick, reactive, ref} from "vue";
import {showToast} from "vant";
import {defaultContact} from "@/view/pageConfig/config";
import {getCurrentSession, setCurrentSession} from "@/view/chat/utils";

export default {
  name: "contacts",
  props: ['contacts'],
  setup(props, ctx) {
    let newContact = reactive({
      name: '',
      character: ''
    })
    let sys = {
      name: defaultContact.name,
      character: defaultContact.character
    }

    const reset = () => {
      newContact.name = ''
      newContact.character = ''
    }
    let showAdd = ref(false)
    // 触发删除事件
    const del = (contact) => {
      console.log('del', contact)
      if(contact.name===getCurrentSession())
        setCurrentSession(sys.name)
      ctx.emit('handelDelContact', contact)
    }
    //增加
    const add = () => {
      console.log('contact', newContact)
      if (newContact.name === '' || newContact.character === '') {
        showToast('请填写信息！')
        return false
      }
      let flag=0
        props.contacts.forEach(contact=>{
          if(contact.name===newContact.name)
          {
            showToast('命名重复')
            flag=1
          }

        })
      if(flag===1)
        return false
      let temp={name: newContact.name, character: newContact.character}
      ctx.emit('addContact',temp )
      // console.log('传递的contact', {name: newContact.name, character: newContact.character})
      nextTick(()=>{
        handleSelect(temp.name)
        console.log('执行了nextTick')
      })
      reset()
      showAdd.value = false
    }
    const cancelAdd = () => {
      reset()
      showAdd.value = false
    }
    const handleShowAdd = () => {
      showAdd.value = true
    }
    //切换选项(视图切换)

    const handleSelect = (id) => {
      let currentId = getCurrentSession()
      if (currentId === id)
        return
      let currentVal = document.getElementById(currentId)
      let newVal = document.getElementById(id)
      currentVal.style.backgroundColor = defaultContact.background
      newVal.style.backgroundColor = defaultContact.selectedBackground
      setCurrentSession(id)
      ctx.emit('handleSelect', id)
    }
    // 初始化
    handleSelect(getCurrentSession())
    return {
      del,
      add,
      sys,
      cancelAdd,
      newContact,
      showAdd,
      handleShowAdd,
      handleSelect
    }
  },

}
</script>

<style scoped>
.character {
  font-size: 6px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.title {
  margin-top: 10px;
  font-size: 18px;
  font-weight: bold;
  color: #2c3e50;
}

.input {
  /*margin: 10px 0;*/
  text-align: center;
}

.addInfo {
  margin: 10px 0;
  /*display: flex;*/
  /*flex-direction: column;*/
  /*justify-content: space-around;*/
  /*height: 200px;*/
}

.label {
  color: rgba(134, 102, 41, 0.7);
  font-weight: 700;
  vertical-align: top;
}

.addInfo input {
  width: 80%;

}

.cell-selected {
  background-color: darkgoldenrod;
}
.del{
  height: 100%;
}

.cell {
  background-color: #a1acbd;
}

.btn {
  margin: 10px 5px;
  display: flex;
  /*flex-direction: ;*/
  justify-content: space-around;
}
.add-icon{
  padding: 10px;
}
</style>
