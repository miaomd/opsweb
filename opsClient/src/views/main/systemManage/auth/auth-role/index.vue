<template>
  <div class="layout-container">
    <div class="layout-container-table">

      <el-select v-model="selectValue" filterable placeholder="选择角色" @change="changeLevel">
        <el-option v-for="item in selectOptions" :key="item.value" :label="item.label" :value="item.value" />
      </el-select>
      <el-button type="primary" @click="changeAuth" style="margin-left: 20px">提交变更</el-button>
      <!-- :filter-method="filterMethod" :left-default-checked="leftValue" :right-default-checked="rightValue"-->
      <el-transfer v-model="transferValue" filterable style="margin-top: 1rem;" filter-placeholder="State Abbreviations"
        :data="data" :titles="['未授权', '已授权']" />


    </div>
  </div>
</template>

<script lang="ts">
import {
  ElTransfer,
  ElSelect,
  ElOption,
  ElRadioGroup,
  ElRadio,
  ElButton,
  ElNotification,
  ElForm,
  ElFormItem,
} from "element-plus";
import { defineComponent, ref, onMounted, watch, reactive } from 'vue'
import { getMenuApi, userInfoApi } from '@/api/user'

export default defineComponent({
  setup() {
    const typeVal = ref(1);
    const formLabelWidth = "100px";
    const typeSwitch = ref("add");
    const transferValue = ref([]);
    const activeNames = ref(["3"]);
    const data = ref([]);
    const Myresult = ref();
    const changeLevel = () => {
      let params = { type: "getAuth", role: selectValue.value };
      getMenuApi(params).then((res: { data: any; }) => {
        let myRes = res.data;
        if (myRes.myState == "success") {
          data.value = [];
          console.log(myRes)
          if (myRes["no_list"].length > 0) {
            for (var index in myRes["no_list"]) {
              data.value.push({
                label: myRes["no_list"][index]["meta_title"],
                key: myRes["no_list"][index]['id'],
                initial: myRes["no_list"][index]['id']
              });
            }
          }
          transferValue.value = [];
          if (myRes["yes_list"].length > 0) {
            for (var index2 in myRes["yes_list"]) {
              data.value.push({
                label: myRes["yes_list"][index2]["meta_title"],
                key: myRes["yes_list"][index2]['id'],
                initial: myRes["yes_list"][index2]['id']
              });
              transferValue.value.push(
                myRes["yes_list"][index2]['id']
              );
            }
          }

        } else {
          ElNotification({
            title: "error",
            message: myRes.myDesc,
            type: "error",
            position: "bottom-right",
          });
          console.log(myRes);
        }
      })
    };


    const changeAuth = () => {
      let params = { type: "changeAuth", role: selectValue.value, authList: transferValue.value };
      getMenuApi(params).then((res: { data: any; }) => {
        let myRes = res.data;
        if (myRes.myState == "success") {
          
          ElNotification({
            title: "success",
            message: selectValue.value + "权限更新完成！",
            type: "success",
            position: "bottom-right",
          });
          selectValue.value =""
        } else {
          ElNotification({
            title: "error",
            message: myRes.myDesc,
            type: "error",
            position: "bottom-right",
          });
          console.log(myRes);
        }
      });
    };

    function getRoleList() {
      let params = { type: "roleList" };
      userInfoApi(params).then((res2: { data: { myState: string; myDesc: any; }; }) => {
        if (res2.data.myState == "success") {
          Myresult.value = res2.data.myDesc;
          selectOptions.value = [];
          cities.value = [];
          Myresult.value.forEach(function (v: any) {
            selectOptions.value.push({ value: v, label: v });
            cities.value.push(v);
          })


        } else {
          console.log("获取权限失败：", res2.data);
        }
      });
    };
    // const filterMethod = (query: string, item: { initial: string; }) => {
    //   return item.initial.toLowerCase().includes(query.toLowerCase());
    // };
    // const handleChange2 = (cascaderValue) => {
    //   console.log(cascaderValue);
    // };

    const selectValue = ref();
    const selectOptions = ref([]);
    const checkedCities = ref([]);
    const cities = ref([]);

    onMounted(() => {
      getRoleList()
    })
    // watch the codeData change but not from editor change
    // watch(selectValue, (selectValue) => {
    //   if (!editorChange) {
    //     setEditorData()
    //   }
    // })    
    return {
      selectValue,
      changeLevel,
      selectOptions,
      changeAuth,
      transferValue,
      // filterMethod,
      data
    }
  }
})
</script>

<style lang="scss" scoped>
* {
  text-align: left;
}

#codeEditor {
  text-align: left;
}

pre {
  text-align: left;
}
</style>