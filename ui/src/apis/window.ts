import request from "../utils/request";

export const minimizeWindow = () => {
  return request.get("/window/minimize");
};

export const maximizeWindow = () => {
  return request.get("/window/maximize");
};

export const restoreWindow = () => {
  return request.get("/window/restore");
};

export const closeWindow = () => {
  return request.get("/window/close");
};

export default {
  minimizeWindow,
  maximizeWindow,
  restoreWindow,
  closeWindow,
};
