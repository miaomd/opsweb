import{d as T,bF as G,j as B,bM as L,_ as U,r as m,o as y,q as E,w as s,b as t,c as q,F as O,x as P,k as w,aT as I,a as _,e as C,t as $,bd as A,bx as S,ai as j,bL as k,E as g,bN as M}from"./index.17213d34.js";import{T as R}from"./index.a9f44871.js";import{P as H}from"./Plus.c665c221.js";import{D as J}from"./Delete.d2b3d8a8.js";import{S as K}from"./Search.91283474.js";const Q=T({components:{Layer:G},props:{layer:{type:Object,default:()=>({show:!1,title:"",showButton:!0})}},setup(e,a){return{ruleForm:B({name:"",username:"",role:"",password:""}),rules:{name:[{required:!0,message:"\u8BF7\u8F93\u5165\u59D3\u540D",trigger:"blur"}],username:[{required:!0,message:"\u8BF7\u8F93\u5165\u767B\u5F55\u540D",trigger:"blur"}],role:[{required:!0,message:"\u8BF7\u9009\u62E9",trigger:"blur"}]},roleOptions:[{value:"user",label:"\u7528\u6237"},{value:"admin",label:"\u7BA1\u7406\u5458"},{value:"SuperAdmin",label:"\u8D85\u7EA7\u7BA1\u7406\u5458"}]}},methods:{submit(){this.$refs.form.validate(e=>{if(e){let a=this.ruleForm;this.layer.row?this.updateForm(a):(a.password=a.username+"@1234",this.addForm(a))}else return!1})},addForm(e){L(e).then(a=>{this.$message({type:"success",message:"\u65B0\u589E\u6210\u529F"}),this.layer.show=!1,this.$emit("getData")})},updateForm(e){}}});function W(e,a,i,h,c,D){const r=m("el-input"),f=m("el-form-item"),p=m("el-option"),F=m("el-select"),v=m("el-form"),b=m("Layer",!0);return y(),E(b,{layer:e.layer,onConfirm:e.submit},{default:s(()=>[t(v,{model:e.ruleForm,rules:e.rules,ref:"form","label-width":"120px",style:{"margin-right":"30px"}},{default:s(()=>[t(f,{label:"\u59D3\u540D\uFF1A",prop:"name"},{default:s(()=>[t(r,{modelValue:e.ruleForm.name,"onUpdate:modelValue":a[0]||(a[0]=n=>e.ruleForm.name=n),placeholder:"\u8BF7\u8F93\u5165\u540D\u79F0"},null,8,["modelValue"])]),_:1}),t(f,{label:"\u767B\u5F55\u540D\uFF1A",prop:"username"},{default:s(()=>[t(r,{modelValue:e.ruleForm.username,"onUpdate:modelValue":a[1]||(a[1]=n=>e.ruleForm.username=n),placeholder:"\u8BF7\u8F93\u5165\u7528\u6237\u540D"},null,8,["modelValue"])]),_:1}),t(f,{label:"\u89D2\u8272\uFF1A",prop:"role"},{default:s(()=>[t(F,{modelValue:e.ruleForm.role,"onUpdate:modelValue":a[2]||(a[2]=n=>e.ruleForm.role=n),placeholder:"\u9009\u62E9\u89D2\u8272",clearable:"",filterable:"","allow-create":"","default-first-option":"","reserve-keyword":!1},{default:s(()=>[(y(!0),q(O,null,P(e.roleOptions,n=>(y(),E(p,{key:n.value,label:n.label,value:n.value},null,8,["label","value"]))),128))]),_:1},8,["modelValue"])]),_:1}),t(f,{label:"\u5BC6\u7801\uFF1A"},{default:s(()=>[t(r,{modelValue:e.ruleForm.password,"onUpdate:modelValue":a[3]||(a[3]=n=>e.ruleForm.password=n),autocomplete:"off",disabled:!0},null,8,["modelValue"])]),_:1})]),_:1},8,["model","rules"])]),_:1},8,["layer","onConfirm"])}var X=U(Q,[["render",W]]);const Y=T({components:{Table:R,Layer:X},setup(){const e=B({input:""}),a=B({show:!1,title:"\u65B0\u589E",showButton:!0}),i=B({index:1,size:20,total:0}),h=w(!0),c=w([]),D=w([]),r=w([]),f=l=>{D.value=l},p=l=>{l&&(i.index=1),c.value=[],e.input?r.value.forEach(d=>{for(let o in d)d[o]==e.input&&c.value.push(d)}):r.value.forEach((d,o)=>{let N=(i.index-1)*i.size,z=(i.index-1)*i.size+i.size-1;o>=N&&o<=z&&c.value.push(d)})},F=()=>{h.value=!0,r.value=[],k({type:"info"}).then(d=>{let o=d.data;o.myState=="success"?(r.value=o.myDesc,i.total=Number(r.value.length),p(!0),r.value.length==0&&g({message:"\u6CA1\u6709\u7B26\u5408\u6761\u4EF6\u7684\u6570\u636E\uFF01\uFF01\uFF01",type:"error"})):(g({message:"\u67E5\u8BE2\u5931\u8D25\uFF0C\u539F\u56E0\uFF1A"+o.myDesc,type:"error"}),console.log("res:",o))}).catch(d=>{c.value=[],r.value=[],i.index=1,i.total=0}).finally(()=>{h.value=!1})},v=l=>{M({username:l}).then(o=>{g({type:"success",message:"\u91CD\u7F6E\u6210\u529F\uFF0C\u65B0\u5BC6\u7801\uFF1A"+o.data.message})})},b=l=>{let d={name:l.name,username:l.username,password:l.username+"@1234",level:"tester",team:"\u6D4B\u8BD5\u5916\u5305"};L(d).then(o=>{g({type:"success",message:"\u6CE8\u518C\u6210\u529F"}),F()}).catch(o=>{g({type:"error",message:"\u6CE8\u518C\u5931\u8D25\uFF1A"+o})})},n=()=>{a.title="\u65B0\u589E\u6570\u636E",a.show=!0,delete a.row},V=l=>{a.title="\u7F16\u8F91\u6570\u636E",a.row=l,a.show=!0},u=l=>{if(!l.username)return;l.loading=!0,k({type:"is_active",row:l}).then(o=>{o.data.myState=="success"?(g({type:"success",message:"\u72B6\u6001\u53D8\u66F4\u6210\u529F"}),F()):g({type:"error",message:"\u72B6\u6001\u53D8\u66F4\u5931\u8D25\uFF1A"+o.data.myDesc})}).catch(o=>{g({type:"error",message:"\u72B6\u6001\u53D8\u66F4\u5931\u8D25"})}).finally(()=>{l.loading=!1})};return F(),{Plus:H,Delete:J,Search:K,query:e,tableData:c,chooseData:D,loading:h,page:i,layer:a,handleSelectionChange:f,getTableData:p,handleReset:v,handleAdd:n,handleEdit:V,handleUpdateStatus:u,handleLogon:b,getData:F}}}),Z={class:"layout-container"},x={class:"layout-container-form flex space-between"},ee={class:"layout-container-form-handle"},ae={class:"layout-container-form-search"},le={class:"layout-container-table"},te={class:"statusName"};function ue(e,a,i,h,c,D){const r=m("el-button"),f=m("el-input"),p=m("el-table-column"),F=m("el-switch"),v=m("el-popconfirm"),b=m("Table"),n=m("Layer"),V=I("loading");return y(),q("div",Z,[_("div",x,[_("div",ee,[t(r,{type:"primary",icon:e.Plus,onClick:e.handleAdd},{default:s(()=>[C($(e.$t("message.common.add")),1)]),_:1},8,["icon","onClick"])]),_("div",ae,[t(f,{modelValue:e.query.input,"onUpdate:modelValue":a[0]||(a[0]=u=>e.query.input=u),placeholder:e.$t("message.common.searchTip")},null,8,["modelValue","placeholder"]),t(r,{type:"primary",icon:e.Search,class:"search-btn",onClick:a[1]||(a[1]=u=>e.getTableData(!0))},{default:s(()=>[C($(e.$t("message.common.search")),1)]),_:1},8,["icon"])])]),_("div",le,[A((y(),E(b,{ref:"table",page:e.page,"onUpdate:page":a[2]||(a[2]=u=>e.page=u),showSelection:!1,data:e.tableData,showIndex:!0,onGetTableData:e.getTableData,onSelectionChange:e.handleSelectionChange},{default:s(()=>[t(p,{prop:"username",label:"\u7528\u6237\u540D",align:"center"}),t(p,{prop:"name",label:"\u6635\u79F0",align:"center"}),t(p,{prop:"role",label:"\u89D2\u8272",align:"center"}),t(p,{prop:"is_active",label:"\u72B6\u6001",align:"center"},{default:s(u=>[_("span",te,$(u.row.is_active===1?"\u542F\u7528":"\u7981\u7528"),1),t(F,{modelValue:u.row.is_active,"onUpdate:modelValue":l=>u.row.is_active=l,"active-color":"#13ce66","inactive-color":"#ff4949","active-value":1,"inactive-value":0,loading:u.row.loading,onChange:l=>e.handleUpdateStatus(u.row)},null,8,["modelValue","onUpdate:modelValue","loading","onChange"])]),_:1}),t(p,{label:e.$t("message.common.handle"),align:"center",fixed:"right",width:"200"},{default:s(u=>[A(t(r,{onClick:l=>e.handleLogon(u.row)},{default:s(()=>[C("\u6CE8\u518C")]),_:2},1032,["onClick"]),[[S,!u.row.role]]),t(v,{title:u.row.name,onConfirm:l=>e.handleReset(u.row.username)},{reference:s(()=>[A(t(r,{type:"danger"},{default:s(()=>[C("\u91CD\u7F6E")]),_:2},1536),[[S,u.row.role]])]),_:2},1032,["title","onConfirm"])]),_:1},8,["label"])]),_:1},8,["page","data","onGetTableData","onSelectionChange"])),[[V,e.loading]]),e.layer.show?(y(),E(n,{key:0,layer:e.layer,onGetData:e.getData},null,8,["layer","onGetData"])):j("",!0)])])}var me=U(Y,[["render",ue],["__scopeId","data-v-1187f136"]]);export{me as default};