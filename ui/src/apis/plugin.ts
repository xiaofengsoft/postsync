import request from "../utils/request";

export const getPlugins = () => {
  return request.get("plugins");
}

export default {
  getPlugins
};