import request from "../utils/request";

export const selectImage = () => {
  return request.get("write/image/select");
};

export default {
  selectImage,
};
