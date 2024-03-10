import axios, { AxiosInstance } from "axios";

const apiClient: AxiosInstance = axios.create({
  headers: {
    "Content-type": "application/json",
  },
  timeout: 5000,
});

export default apiClient;
