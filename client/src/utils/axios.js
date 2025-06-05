
import axios from "axios";

const instance = axios.create({
  baseURL: "http://127.0.0.1:9000/",
  withCredentials: true,
  headers: {
    Accept: "application/json",
  },
});

// Thêm bộ chặn request
instance.interceptors.request.use(
  (config) => {
    const localStorageData = window.localStorage.getItem("persist:qltv/user");

    if (localStorageData) {
      try {
        const parsedData = JSON.parse(localStorageData);
        const accessToken = JSON.parse(parsedData?.token);

        if (accessToken) {
          config.headers.Authorization = `Bearer ${accessToken}`;
        }
      } catch (error) {
        console.error("Error parsing token:", error);
      }
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Thêm bộ chặn response
instance.interceptors.response.use(
  (response) => response.data,
  (error) => {
    if (error.response) {
      if (error.response.status === 401) {
        window.localStorage.removeItem("persist:qltv/user");
        window.location.reload();
      } else {
        console.error("API Error:", error.response.data);
      }
      return Promise.reject(error.response.data);
    }
    return Promise.reject(error);
  }
);

export default instance;
