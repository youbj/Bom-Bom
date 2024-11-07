import axios, { AxiosError, InternalAxiosRequestConfig } from 'axios';
import CookieManager from '@react-native-cookies/cookies'; 
import EncryptedStorage from 'react-native-encrypted-storage';

export const localURL = 'http://10.0.2.2:8080/api/v1'

const instance = axios.create({
  baseURL: localURL,
  timeout: 1000,
  headers: {
    "Content-Type": "application/json"
  }
});

// Request Interceptor - 요청마다 access token을 추가
instance.interceptors.request.use(
  async (config) => {
    const session = await EncryptedStorage.getItem('user_session');
    const sessionData = session ? JSON.parse(session) : null;
    const accessToken = sessionData?.accessToken;
    if (accessToken) {
      config.headers.Authorization = accessToken;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

instance.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;
    console.log(error);
    if (error.response?.status === 401 && !originalRequest._retry) {
      console.log('?')
      originalRequest._retry = true;

      try {
        // 쿠키에서 refresh token 가져오기
        const cookies = await CookieManager.get("http://10.0.2.2");
        const refreshToken = cookies?.refreshToken?.value;
        console.log(refreshToken)
        if (refreshToken) {
          // 새 access token 요청
          const { data } = await axios.post(`${localURL}/members/reissue`, {
            refreshToken,
          });

          const newAccessToken = data.accessToken;
          const type = data.type;
          console.log(newAccessToken)
          await EncryptedStorage.setItem(
            'user_session',
            JSON.stringify({
              newAccessToken,
              type
            }),
          );

          // 새 access token으로 원래 요청 재시도
          originalRequest.headers.Authorization = newAccessToken;
          return instance(originalRequest);
        }
      } catch (refreshError) {
        // refresh token 갱신 실패 시 로그인 페이지로 리다이렉트 등 처리
        return Promise.reject(refreshError);
      }
    }
    return Promise.reject(error);
  }
);

export default instance;

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
