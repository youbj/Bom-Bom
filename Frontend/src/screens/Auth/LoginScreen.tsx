import React, {useState} from 'react';
import {
  View,
  Image,
  TouchableOpacity,
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
import CustomAlert from '../../components/CustomAlert';

const LoginScreen = (): JSX.Element => {
  const setIsLoggedIn = useAuthStore(state => state.setIsLoggedIn);
  const [passwordVisible, setPasswordVisible] = useState<boolean>(false);
  const [loginId, setLoginId] = useState<string>('');
  const [password, setPassword] = useState<string>('');
  const navigation = useNavigation<LoginScreenNavigationProp>();

  // CustomAlert 상태 관리
  const [alertVisible, setAlertVisible] = useState(false);
  const [alertTitle, setAlertTitle] = useState('');
  const [alertMessage, setAlertMessage] = useState('');
  const [alertOnClose, setAlertOnClose] = useState<() => void>(() => {});

  const showAlert = (title: string, message: string, onClose?: () => void) => {
    setAlertTitle(title);
    setAlertMessage(message);
    setAlertVisible(true);
    setAlertOnClose(() => onClose || (() => setAlertVisible(false)));
  };

  const onPressJoin = () => {
    navigation.navigate('Join');
  };

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

  const requestNotificationPermission = async () => {
    if (Platform.OS === 'android' && Platform.Version >= 33) {
      const granted = await PermissionsAndroid.request(
        PermissionsAndroid.PERMISSIONS.POST_NOTIFICATIONS,
      );
      return granted === PermissionsAndroid.RESULTS.GRANTED;
    }
    return true;
  };

  const sendFcmToken = async () => {
    try {
      const permissionGranted = await requestNotificationPermission();
      if (!permissionGranted) {
        console.log('알림 권한이 거부되었습니다.');
        return;
      }

      await messaging().registerDeviceForRemoteMessages();
      const fcmToken = await messaging().getToken();

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
        await storeDataInEncryptedStorage(accessToken, type);
        await storeRefreshTokenInCookie(refreshToken);
        await sendFcmToken();

        setIsLoggedIn(true);
        showAlert('로그인 성공', '환영합니다!', () => {
          setAlertVisible(false);
        });
      }
    } catch (error) {
      if (axios.isAxiosError(error)) {
        if (error.response?.status === 401) {
          showAlert('로그인 실패', '아이디 혹은 비밀번호를 확인해주세요.');
        } else {
          showAlert('로그인 실패', '로그인 중 오류가 발생했습니다.');
        }
      } else {
        showAlert('오류', '예상치 못한 오류가 발생했습니다.');
      }
    }
  };

  return (
    <>
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
          <CustomText style={loginStyle.text}>
            아직 회원이 아니시라면?
          </CustomText>
        </TouchableOpacity>
      </View>

      <CustomAlert
        visible={alertVisible}
        title={alertTitle}
        message={alertMessage}
        onClose={alertOnClose}
      />
    </>
  );
};

export default LoginScreen;
