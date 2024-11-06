import axios, { AxiosError, InternalAxiosRequestConfig } from 'axios';
import CookieManager from '@react-native-cookies/cookies'; 

export const localURL = 'http://10.0.2.2:8080/api/v1'


const instance = axios.create({
  baseURL: localURL,
  timeout: 1000,
  headers: {
    "Content-Type": "application/json"
  }
});

// instance.interceptors.request.use(
//   async (config: InternalAxiosRequestConfig) => {

//     const cookies = await CookieManager.get('https://localhost:8080');
//     let accessToken = cookies.accessToken; 

//     if (!accessToken) {
//       try {
//         const response = await axios.post
//       }
//     }

//     if (accessToken && config.headers) {
//       config.headers.Authorization = `${accessToken}`;
//     }

//     return config; 
//   },
//   (error: AxiosError) => {
//     return Promise.reject(error); 
//   }
// );

// export default instance;
