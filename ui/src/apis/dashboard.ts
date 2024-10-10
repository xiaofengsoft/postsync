import request from "../utils/request";

export const checkLogin = () => {
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

export default {
  checkLogin,
  loginOnce,
  getPostList,
  deletePostFile,
};
