/** 动态路由实现基础组件 */
/** 引入全局Layout组件 */
import Layout from '@/layout/index.vue'
/** 引入多级菜单控制器组件 */
import MenuBox from '@/components/menu/index.vue'
/** 引入带有系统自定义name的组件，方便keep-alive实现 */
import { createNameComponent } from '../createNode'
/** 引入所有的配置清单 */
import backConfig from './backConfig'
import { getMenuApi } from '@/api/user'
import store from '@/store'

/** 获取后台模板配置清单 */
const getMenu = async () => {
  let params = { type: "getMenu", role: store.state.user.info.role, username: store.state.user.info.username };
  const result = await getMenuApi(params)
  const backRoutes = getComponents(result.data.list)
  return backRoutes
}

/** 循环取出component */
const getComponents = (data: any[], level = 1) => {
  const newData: any[] = data.map((item) => {
    if (item.children) {
      if (level == 1) {
        return {
          ...item,
          component: Layout,
          children: getComponents(item.children, level + 1)
        }
      } else {
        return {
          ...item,
          component: MenuBox,
          children: getComponents(item.children, level + 1)
        }
      }
    } else {
      const [first, end] =  item.component.split('_')
      const component = backConfig[first][end]
      return {
        ...item,
        component,
      }
    }
  })
  return newData
}

export default getMenu