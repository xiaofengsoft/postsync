import axios from "axios";

const instance = axios.create({
  baseURL: "/api",
  headers: {
    "Content-Type": "application/json",
  },
  timeout: 1000000,
});

export default instance;
