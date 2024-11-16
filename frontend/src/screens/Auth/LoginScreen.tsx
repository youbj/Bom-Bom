// LoginScreen.tsx
import React, {useState} from 'react';
import {
  View,
  Image,
  TouchableOpacity,
  Alert,
  Platform,
  PermissionsAndroid,
} from 'react-native';
import {useNavigation} from '@react-navigation/native';
import EncryptedStorage from 'react-native-encrypted-storage';
import CookieManager from '@react-native-cookies/cookies';
import {LoginScreenNavigationProp} from '../../../types/navigation.d';
import axios from 'axios';
import defaultStyle from '../../styles/DefaultStyle';
import loginStyle from '../../styles/Auth/LoginStyle';
import CustomText from '../../components/CustomText';
import CustomTextInput from '../../components/CustomTextInput';
import Icon from 'react-native-vector-icons/MaterialCommunityIcons';
import instance, {localURL} from '../../api/axios';
import messaging from '@react-native-firebase/messaging';
import useAuthStore from '../../stores/useAuthStore';

const LoginScreen = (): JSX.Element => {
  const setIsLoggedIn = useAuthStore(state => state.setIsLoggedIn);
  const [passwordVisible, setPasswordVisible] = useState<boolean>(false);
  const [loginId, setLoginId] = useState<string>('');
  const [password, setPassword] = useState<string>('');
  const navigation = useNavigation<LoginScreenNavigationProp>();

  const onPressJoin = () => {
    navigation.navigate('Join');
  };

  // EncryptedStorage에 accessToken과 type 저장
  const storeDataInEncryptedStorage = async (
    accessToken: string,
    type: string,
  ) => {
    try {
      await EncryptedStorage.setItem(
        'user_session',
        JSON.stringify({
          accessToken,
          type,
        }),
      );
      console.log('EncryptedStorage에 저장 성공');
    } catch (error) {
      console.error('EncryptedStorage에 저장 실패:', error);
    }
  };

  // 쿠키에 refreshToken 저장
  const storeRefreshTokenInCookie = async (refreshToken: string) => {
    try {
      await CookieManager.set('http://10.0.2.2', {
        name: 'refreshToken',
        value: refreshToken,
        path: '/',
        secure: false,
        httpOnly: true,
      });

      console.log('쿠키에 refreshToken 저장 성공');
    } catch (error) {
      console.error('쿠키에 refreshToken 저장 실패:', error);
    }
  };

  // Android 13 이상 알림 권한 요청
  const requestNotificationPermission = async () => {
    if (Platform.OS === 'android' && Platform.Version >= 33) {
      const granted = await PermissionsAndroid.request(
        PermissionsAndroid.PERMISSIONS.POST_NOTIFICATIONS,
      );
      return granted === PermissionsAndroid.RESULTS.GRANTED;
    }
    return true;
  };

  // 로그인 이후 FCM 토큰을 백엔드로 전송
  const sendFcmToken = async () => {
    try {
      const permissionGranted = await requestNotificationPermission();
      if (!permissionGranted) {
        console.log('알림 권한이 거부되었습니다.');
        return;
      }

      await messaging().registerDeviceForRemoteMessages();
      const fcmToken = await messaging().getToken();

      // FCM 토큰을 포함한 요청을 보낼 때 accessToken을 header에 포함
      const fcmResponse = await instance.post(`/members/fcmtoken`, {
        fcmToken,
      });
      if (fcmResponse.status === 200) {
        console.log('FCM 토큰 전송 성공');
      }
    } catch (error) {
      console.error('FCM 등록 중 오류 발생:', error);
    }
  };

  // 로그인 요청 및 FCM 토큰 전송
  const onLogin = async () => {
    try {
      const response = await axios.post(`${localURL}/members/login`, {
        loginId,
        password,
      });
      const data = response.data;
      const accessToken = data.accessToken;
      const refreshToken = data.refreshToken;
      const type = data.type;

      if (response.status === 200) {
        // accessToken과 type을 EncryptedStorage에 저장
        await storeDataInEncryptedStorage(accessToken, type);

        // refreshToken을 쿠키에 저장
        await storeRefreshTokenInCookie(refreshToken);

        // accessToken을 포함해 FCM 토큰을 백엔드로 전송
        await sendFcmToken();

        setIsLoggedIn(true); // 상태 관리 스토어에서 로그인 상태를 true로 설정
      }
    } catch (error) {
      if (axios.isAxiosError(error)) {
        if (error.response?.status === 401) {
          Alert.alert('아이디 혹은 비밀번호를 확인해주세요.');
        } else {
          Alert.alert('로그인 중 오류가 발생했습니다.');
        }
      } else {
        Alert.alert('예상치 못한 오류가 발생했습니다.');
      }
    }
  };

  return (
    <View style={defaultStyle.container}>
      <Image
        source={require('../../assets/images/logo.png')}
        style={loginStyle.logo}
      />
      <CustomText style={loginStyle.title}>봄 : 봄</CustomText>
      <View style={loginStyle.longSpace} />

      <CustomTextInput
        style={defaultStyle.input}
        placeholder="아이디"
        placeholderTextColor="#999999"
        autoCapitalize="none"
        value={loginId}
        onChangeText={text => setLoginId(text)}
      />

      <CustomTextInput
        style={[defaultStyle.input, {flex: 1}]}
        placeholder="비밀번호"
        placeholderTextColor="#999999"
        right={
          <Icon
            name={passwordVisible ? 'eye' : 'eye-off'}
            onPress={() => setPasswordVisible(!passwordVisible)}
            size={20}
            color={'#bbb'}
          />
        }
        secureTextEntry={!passwordVisible}
        value={password}
        onChangeText={text => setPassword(text)}
      />

      <TouchableOpacity style={loginStyle.button} onPress={onLogin}>
        <CustomText style={loginStyle.buttonText}>로그인</CustomText>
      </TouchableOpacity>
      <View style={loginStyle.space} />
      <TouchableOpacity
        style={[loginStyle.button, loginStyle.transparentButton]}
        onPress={onPressJoin}>
        <CustomText style={loginStyle.text}>아직 회원이 아니시라면?</CustomText>
      </TouchableOpacity>
    </View>
  );
};

export default LoginScreen;
