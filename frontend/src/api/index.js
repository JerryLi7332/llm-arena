import { authApi } from './auth'
import { usersApi } from './users'
import { rolesApi } from './roles'
import { filesApi } from './files'
import { apisApi } from './apis'

export {
  authApi,
  usersApi,
  rolesApi,
  filesApi,
  apisApi
}

// 默认导出所有API
export default {
  auth: authApi,
  users: usersApi,
  roles: rolesApi,
  files: filesApi,
  apis: apisApi
}
