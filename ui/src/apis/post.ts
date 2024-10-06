import request from "../utils/request";

export const choosePost = () => {
  return request.get("/post/choose");
};

export default {
  choosePost,
};
