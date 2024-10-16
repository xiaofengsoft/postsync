import request from "../utils/request";

export const choosePost = () => {
  return request.get("/post/choose");
};

export const chooseCover = () => {
  return request.get("/post/choose/cover");
};

export const savePostFile = (data: {
  title: string;
  type: string;
  content: string;
}) => {
  return request.post("/post/save/file", data);
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

export const extractPost = (file: string) => {
  return request.post("/post/extract", {
    file,
    tags_num: 3,
  });
};

export default {
  choosePost,
  chooseCover,
  uploadPost,
  savePostFile,
  extractPost,
};
