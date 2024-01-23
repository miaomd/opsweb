<template>
  <Layer :layer="layer" @confirm="submit">
    <el-form :model="ruleForm" :rules="rules" ref="form" label-width="120px" style="margin-right:30px;">
      <el-form-item label="姓名：" prop="name">
        <el-input v-model="ruleForm.name" placeholder="请输入名称"></el-input>
      </el-form-item>
      <el-form-item label="登录名：" prop="username">
        <el-input v-model="ruleForm.username" placeholder="请输入用户名"></el-input>
      </el-form-item>
      <el-form-item label="角色：" prop="role">
        <el-select v-model="ruleForm.role" placeholder="选择角色" clearable filterable allow-create default-first-option
          :reserve-keyword="false">
          <el-option v-for="item in roleOptions" :key="item.value" :label="item.label" :value="item.value">
          </el-option>
        </el-select>
      </el-form-item>

      <!-- <el-form-item label="所属团队：" prop="team">
        <el-select v-model="ruleForm.team" placeholder="选择团队" clearable filterable allow-create default-first-option
          :reserve-keyword="false">
          <el-option v-for="item in teamOptions" :key="item" :label="item" :value="item">
          </el-option>
        </el-select>
      </el-form-item> -->
      <el-form-item label="密码：">
        <el-input v-model="ruleForm.password" autocomplete="off" :disabled="true"></el-input>
      </el-form-item>
    </el-form>
  </Layer>
</template>

<script lang="ts">
import { defineComponent, ref, reactive } from 'vue'
import Layer from '@/components/layer/index.vue'
import { userInfoApi, logonApi } from '@/api/user'
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
    let ruleForm = reactive({
      name: '',
      username: '',
     
      role: '',
      password: ''
    })
    const rules = {
      name: [{ required: true, message: '请输入姓名', trigger: 'blur' }],
      username: [{ required: true, message: '请输入登录名', trigger: 'blur' }],
      
      role: [{ required: true, message: '请选择', trigger: 'blur' }]
    }
    const roleOptions = [
      {
        value: "user",
        label: "用户",
      },
      {
        value: "admin",
        label: "管理员",
      },
      {
        value: "SuperAdmin",
        label: "超级管理员",
      },
    ];



    return {
      ruleForm,
      rules,
      roleOptions
    }
  },
  methods: {
    submit() {
      this.$refs['form'].validate((valid: boolean) => {
        if (valid) {
          let params = this.ruleForm
          if (this.layer.row) {
            this.updateForm(params)
          } else {
            params['password'] = params.username + "@1234"
            this.addForm(params)
          }
        } else {
          return false;
        }
      });
    },
    // 新增提交事件
    addForm(params: object) {
      logonApi(params)
        .then(res => {
          this.$message({
            type: 'success',
            message: '新增成功'
          })
          this.layer.show = false
          this.$emit('getData')
        })
    },
    // 编辑提交事件
    updateForm(params: object) {
      // update(params)
      // .then(res => {
      //   this.$message({
      //     type: 'success',
      //     message: '编辑成功'
      //   })
      //   this.$emit('getTableData', false)
      // })
    }
  }
})
</script>

<style lang="scss" scoped></style>