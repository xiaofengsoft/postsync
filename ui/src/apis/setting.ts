import request from "../utils/request";

export const getSettings = () => {
  return request.get("/setting/read");
};

export const saveSettings = (data: any) => {
  return request.post("/setting/save", data);
};

export default {
  getSettings,
  saveSettings,
};
