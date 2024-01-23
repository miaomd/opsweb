import request from '@/utils/system/request'

/** 注册api */
export function logonApi(data: object) {
  return request({
    url: '/api/logon/',
    method: 'post',
    // baseURL: '/mock',
    data
  })
}

/** 登录api */
export function loginApi(data: object) {
  return request({
    url: '/login',
    method: 'post',
    // baseURL: '/mock',
    data
  })
}
/** 校验密码api */
export function checkPwApi(data: object) {
  return request({
    url: '/api-token-auth',
    method: 'post',
    // baseURL: '/mock',
    data
  })
}

/** 用户信息Api */
export function userInfoApi(data: object) {
  return request({
    url: '/api/userinfo/',
    method: 'post',
    // baseURL: '/mock',
    data
  })
}

/** 退出登录Api */
export function loginOutApi() {
  return request({
    url: '/user/out',
    method: 'post',
    baseURL: '/mock'
  })
}

/** 重置用户密码Api */
export function resetPwdApi(data: object) {
  return request({
    url: '/resetpwd/',
    method: 'post',
    // baseURL: '/mock',
    data
  })
}
/** 修改用户密码Api */
export function passwordChange(data: object) {
  return request({
    url: '/updatepwd/',
    method: 'put',
    // baseURL: '/mock',
    data
  })
}


/** 获取登录后需要展示的菜单 */
export function getMenuApi(data: object) {
  return request({
    url: '/api/webmenu/',
    method: 'post',
    // baseURL: '/mock'
    data
  })
}

/**更新菜单 */
export function updateMenuApi(data: object) {
  return request({
    url: '/api/webmenu/',
    method: 'post',
    // baseURL: '/mock'
    data
  })
}
