import request from "../utils/request";

export const choosePost = () => {
  return request.get("/post/choose");
};

export const chooseCover = () => {
  return request.get("/post/choose/cover");
};

export const uploadPost = (data: {
  title: string;
  digest: string;
  tags: string[];
  cover: string;
  category: string[];
  topic: string;
  columns: string[];
  file: string;
  sites: string[];
}) => {
  return request.post("/post/upload", data);
};

export default {
  choosePost,
  chooseCover,
  uploadPost,
};
