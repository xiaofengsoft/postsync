import request from "../utils/request";

export const selectImage = () => {
  return request.get("write/image/select");
};

export const loadPostFile = (path: string) => {
  return request.post("write/load", { path });
};

export default {
  selectImage,
  loadPostFile,
};
