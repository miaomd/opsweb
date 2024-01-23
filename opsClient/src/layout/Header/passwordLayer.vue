<template>
  <Layer :layer="layer" @confirm="submit" ref="layerDom">
    <el-form :model="form" :rules="rules" ref="ruleForm" label-width="120px" style="margin-right:30px;">
      <el-form-item label="登录名：" prop="name">
        {{ form.username }}
      </el-form-item>
      <el-form-item label="原密码：" prop="old_password">
        <el-input v-model="form.old_password" placeholder="请输入原密码" show-password></el-input>
      </el-form-item>
      <el-form-item label="新密码：" prop="password">
        <el-input v-model="form.password" placeholder="请输入新密码" show-password></el-input>
      </el-form-item>
      <el-form-item label="再一次：" prop="password2">
        <el-input v-model="form.password2" placeholder="再一次新密码" show-password></el-input>
      </el-form-item>

    </el-form>
  </Layer>
</template>

<script lang="ts">
import type { LayerType } from '@/components/layer/index.vue'
import type { Ref } from 'vue'
import type { ElFormItemContext } from 'element-plus/lib/el-form/src/token'
import { defineComponent, ref, computed } from 'vue'
import { ElMessage } from 'element-plus'
import { useStore } from 'vuex'
import { passwordChange } from '@/api/user'
import Layer from '@/components/layer/index.vue'
export default defineComponent({
  components: {
    Layer
  },
  props: {
    layer: {
      type: Object,
      default: () => {
        return {
          show: false,
          title: '',
          showButton: true
        }
      }
    }
  },
  setup(props, ctx) {
    const ruleForm: Ref<ElFormItemContext | null> = ref(null)
    const layerDom: Ref<LayerType | null> = ref(null)
    const store = useStore()
    const userInfo = computed(() => store.state.user.info).value

    let form = ref({
      Name: "",
      Level: "",
      username: userInfo.username,
      old_password: "",
      password: "",
      password2: "",
    })
    const rules = {
      old_password: [{ required: true, message: '请输入原密码', trigger: 'blur' }
      ],
      password: [{ required: true, message: '请输入新密码', trigger: 'blur' },
      { pattern: /^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[\W]).{8,16}$/, message: '密码为8~16位且同时包含,数字+大小写字母+特殊符号', trigger: 'blur' }],
      password2: [{ required: true, message: '再一次新密码', trigger: 'blur' },
      { pattern: /^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[\W]).{8,16}$/, message: '密码为8~16位且同时包含,数字+大小写字母+特殊符号', trigger: 'blur' }],

    }
    function submit() {
      if (ruleForm.value) {
        ruleForm.value.validate((valid) => {
          if (valid) {
            // let params = {
            //   id: form.value.userId,
            //   old: form.value.old,
            //   new: form.value.new
            // }
            console.log("form", form)
            passwordChange(form.value)
              .then(res => {
                let changeRe = res.data;
                if (changeRe.message == "ok") {
                  ElMessage({
                    type: 'success',
                    message: '密码修改成功，即将跳转到登录页面'
                  })
                  layerDom.value && layerDom.value.close()
                  setTimeout(() => {
                    store.dispatch('user/loginOut')
                  }, 2000)
                } else {
                  // alert(changeRe.message);

                  ElMessage({
                    message: changeRe.message,
                    type: "error",
                  });
                }
              })
          } else {
            return false;
          }
        });
      }
    }
    return {
      form,
      rules,
      layerDom,
      ruleForm,
      submit
    }
  }
})
</script>

<style lang="scss" scoped></style>