<template>
  <div class="layout-container">
    <div class="layout-container-form flex space-between">
      <div class="layout-container-form-handle">
        <el-button type="primary" :icon="Plus" @click="handleAdd">{{
          $t("message.common.add")
        }}</el-button>
        <!-- <el-popconfirm :title="$t('message.common.delTip')" @confirm="handleReset(chooseData)">
          <template #reference>
            <el-button type="danger" :icon="Delete" :disabled="chooseData.length === 0">{{ $t("message.common.delBat")
            }}</el-button>
          </template>
        </el-popconfirm> -->
      </div>
      <div class="layout-container-form-search">
        <el-input v-model="query.input" :placeholder="$t('message.common.searchTip')"></el-input>
        <el-button type="primary" :icon="Search" class="search-btn" @click="getTableData(true)">{{
          $t("message.common.search") }}</el-button>
      </div>
    </div>
    <div class="layout-container-table">
      <Table ref="table" v-model:page="page" v-loading="loading" :showSelection="false" :data="tableData"
        :showIndex="true" @getTableData="getTableData" @selection-change="handleSelectionChange">
        <!-- <el-table-column prop="id" label="Id" align="center" width="80" /> -->
        <el-table-column prop="username" label="用户名" align="center" />
        <el-table-column prop="name" label="昵称" align="center" />
        <!-- <el-table-column prop="team" label="团队" align="center" /> -->
        <el-table-column prop="role" label="角色" align="center" />
        <el-table-column prop="is_active" label="状态" align="center">
          <template #default="scope">
            <span class="statusName">{{ scope.row.is_active === 1 ? "启用" : "禁用" }}</span>
            <el-switch v-model="scope.row.is_active" active-color="#13ce66" inactive-color="#ff4949" :active-value="1"
              :inactive-value="0" :loading="scope.row.loading" @change="handleUpdateStatus(scope.row)"></el-switch>
          </template>
        </el-table-column>
        <el-table-column :label="$t('message.common.handle')" align="center" fixed="right" width="200">
          <template #default="scope">
            <!-- <el-button @click="handleEdit(scope.row)">{{
              $t("message.common.update")
            }}</el-button> -->
            <el-button @click="handleLogon(scope.row)" v-show="!scope.row.role">注册</el-button>

            <el-popconfirm :title=scope.row.name @confirm="handleReset(scope.row.username)">
              <template #reference>
                <el-button type="danger" v-show="scope.row.role">重置</el-button>
              </template>
            </el-popconfirm>
          </template>
        </el-table-column>
      </Table>
      <Layer :layer="layer" @getData="getData" v-if="layer.show" />
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, reactive } from "vue";
import { Page } from "@/components/table/type";
import { userInfoApi, resetPwdApi, logonApi } from "@/api/user";
import { LayerInterface } from "@/components/layer/index.vue";
import { ElMessage } from "element-plus";
import Table from "@/components/table/index.vue";
import Layer from "./layer.vue";
import { Plus, Delete, Search } from '@element-plus/icons'
export default defineComponent({
  components: {
    Table,
    Layer,
  },
  setup() {
    // 存储搜索用的数据
    const query = reactive({
      input: "",
    });
    // 弹窗控制器
    const layer: LayerInterface = reactive({
      show: false,
      title: "新增",
      showButton: true,
    });
    // 分页参数, 供table使用
    const page: Page = reactive({
      index: 1,
      size: 20,
      total: 0,
    });
    const loading = ref(true);
    const tableData = ref([]);
    const chooseData = ref([]);
    const myTableData = ref([])

    const handleSelectionChange = (val: []) => {
      chooseData.value = val;
    };
    // 获取表格数据
    // params <init> Boolean ，默认为false，用于判断是否需要初始化分页
    const getTableData = (init: Boolean) => {
      if (init) {
        page.index = 1
      }
      tableData.value = []
      if (query.input) {
        myTableData.value.forEach((value) => {
          for (let key in value) {
            if (value[key] == query.input) {
              tableData.value.push(value)
            }
          }
        })
      } else {
        myTableData.value.forEach((value, index) => {
          // 0 20
          let min = (page.index - 1) * page.size
          // 19 39
          let max = (page.index - 1) * page.size + page.size - 1
          if (index >= min && index <= max) {
            tableData.value.push(value)
          }
        })
      }
    }
    const getData = () => {
      loading.value = true
      myTableData.value = []

      let params = { type: "info" }
      userInfoApi(params).then((Response) => {
        let res = Response.data;
        if (res["myState"] == "success") {
          myTableData.value = res["myDesc"];
          // console.log(myTableData.value)
          page.total = Number(myTableData.value.length)
          getTableData(true)
          if (myTableData.value.length == 0) {
            ElMessage({
              message: "没有符合条件的数据！！！",
              type: "error",
            });
          }
        } else {
          ElMessage({
            message: "查询失败，原因：" + res.myDesc,
            type: "error",
          });
          console.log("res:", res);
        }
      })
        .catch(error => {
          tableData.value = []
          myTableData.value = []
          page.index = 1
          page.total = 0
        })
        .finally(() => {
          loading.value = false
        })
    };
    // 重置功能
    const handleReset = (data: any) => {
      let params = {
        username: data
      };
      resetPwdApi(params).then((res) => {
        ElMessage({
          type: "success",
          message: "重置成功，新密码：" + res.data.message,
        });
        // getTableData(tableData.value.length === 1 ? true : false);
      });
    }
    // 注册功能
    const handleLogon = (row: any) => {
      let params = {
        name: row.name,
        username: row.username,
        password: row.username + "@1234",
        level: "tester",
        team: "测试外包"
      };
      logonApi(params).then((res) => {
        ElMessage({
          type: "success",
          message: "注册成功",
        });
        getData()
        // getTableData(tableData.value.length === 1 ? true : false);
      }).catch(err => {
        ElMessage({
          type: 'error',
          message: '注册失败：' + err
        })
      })
    }

    // 新增弹窗功能
    const handleAdd = () => {
      layer.title = "新增数据";
      layer.show = true;
      delete layer.row;
    }
    // 编辑弹窗功能
    const handleEdit = (row: any) => {
      layer.title = "编辑数据";
      layer.row = row;
      layer.show = true;
    }
    // 状态编辑功能
    const handleUpdateStatus = (row: any) => {
      if (!row.username) {
        return
      }
      row.loading = true
      let params = {
        type: "is_active",
        row: row
      }
      userInfoApi(params)
        .then(res => {
          if (res.data["myState"] == "success") {
            ElMessage({
              type: 'success',
              message: '状态变更成功'
            })
            getData()
          } else {
            ElMessage({
              type: 'error',
              message: '状态变更失败：' + res.data["myDesc"]
            })

          }
        })
        .catch(err => {
          ElMessage({
            type: 'error',
            message: '状态变更失败'
          })
        })
        .finally(() => {
          row.loading = false
        })
    }
    getData()
    return {
      Plus,
      Delete,
      Search,
      query,
      tableData,
      chooseData,
      loading,
      page,
      layer,
      handleSelectionChange,
      getTableData,
      handleReset,
      handleAdd,
      handleEdit,
      handleUpdateStatus,
      handleLogon,
      getData
    };
  }
});
</script>

<style lang="scss" scoped>
.statusName {
  margin-right: 10px;
}
</style>
