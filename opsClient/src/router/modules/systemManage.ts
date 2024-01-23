import type { Route } from '../index.type'
import Layout from '@/layout/index.vue'
import { createNameComponent } from '../createNode'
const route: Route[] = [
  {
    path: '/systemManage',
    component: Layout,
    redirect: '/systemManage/menu',
    meta: { title: '系统管理', icon: 'sfont system-shezhi' },
    alwayShow: true,
    children: [
      {
        path: 'menu',
        component: createNameComponent(() => import('@/views/main/systemManage/menu/index.vue')),
        // redirect: '/systemManage/menu/menu-add',
        meta: { title: '菜单管理' },
        // children: [
        //   {
        //     path: 'menu-add',
        //     component: createNameComponent(() => import('@/views/main/systemManage/menu/menu-add/index.vue')),
        //     meta: { title: '菜单注册' },
        //   },
        //   {
        //     path: 'menu-edit',
        //     component: createNameComponent(() => import('@/views/main/systemManage/menu/index.vue')),
        //     meta: { title: '菜单编辑' },
        //   }
        // ]
      },
      {
        path: 'anth',
        component: createNameComponent(() => import('@/components/menu/index.vue')),
        meta: { title: '权限管理' },
        children: [
          {
            path: 'auth-role',
            component: createNameComponent(() => import('@/views/main/systemManage/auth/auth-role/index.vue')),
            meta: { title: '按角色管理' },
          },
          {
            path: 'auth-user',
            component: createNameComponent(() => import('@/views/main/systemManage/menu/index.vue')),
            meta: { title: '按用户管理' },
          }
        ]
      },
      {
        path: 'user',
        component: createNameComponent(() => import('@/views/main/systemManage/users/index.vue')),
        meta: { title: '用户管理' }
      }
    ]
  }
]

export default route