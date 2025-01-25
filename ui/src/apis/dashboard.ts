import request from "../utils/request";

export const checkLogin = (is_force: boolean = false) => {
  if (is_force) {
    return request.get("dashboard/login/check?force=true");
  }
  return request.get("dashboard/login/check");
};
export const loginOnce = (name: string) => {
  return request.post("dashboard/login/once", { name });
};
export const getPostList = () => {
  return request.get("dashboard/post/list");
};
export const deletePostFile = (path: string) => {
  return request.post("dashboard/post/delete", { path });
};

export const resetLogin = (name: string) => {
  return request.post("dashboard/login/reset", { name });
};

export const confirmLogin = (name: string) => {
  return request.post("dashboard/login/confirm", { name });
}


export default {
  checkLogin,
  loginOnce,
  getPostList,
  deletePostFile,
  resetLogin,
  confirmLogin
};
