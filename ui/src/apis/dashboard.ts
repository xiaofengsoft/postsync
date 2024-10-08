import request from "../utils/request";

export const readme = () => {
  return request.get("/dashboard/readme");
};

export default {
  readme,
};
