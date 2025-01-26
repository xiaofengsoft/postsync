import request from "../utils/request";

export const getPlugins = () => {
  return request.get("plugins");
}

export const uninstallPlugins = (name: string) => {
  return request.post(`plugins/uninstall`, {
    name: name
  });
}

export default {
  getPlugins,
  uninstallPlugins
};