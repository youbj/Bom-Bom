import React, {useState} from 'react';
import {View, Image, TouchableOpacity, Alert} from 'react-native';
import {useNavigation} from '@react-navigation/native';
import {
  LoginScreenNavigationProp,
  LoginScreenProps,
} from '../../../types/navigation.d';
import EncryptedStorage from 'react-native-encrypted-storage';
import CookieManager from '@react-native-cookies/cookies'; // 쿠키 관리 라이브러리
import axios, {AxiosError} from 'axios';

import defaultStyle from '../../styles/DefaultStyle';
import loginStyle from '../../styles/Auth/LoginStyle';
import CustomText from '../../components/CustomText';
import CustomTextInput from '../../components/CustomTextInput';
import Icon from 'react-native-vector-icons/MaterialCommunityIcons';
import {localURL} from '../../api/axios';

const LoginScreen = ({setIsLoggedIn}: LoginScreenProps): JSX.Element => {
  const [passwordVisible, setPasswordVisible] = useState<boolean>(false);
  const [loginId, setLoginId] = useState<string>('');
  const [password, setPassword] = useState<string>('');
  const navigation = useNavigation<LoginScreenNavigationProp>();

  const onPressJoin = () => {
    navigation.navigate('Join');
  };

  // EncryptedStorage에 accessToken과 type 저장
  const storeDataInEncryptedStorage = async (accessToken: string, type: string) => {
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

        // 로그인 상태 업데이트
        setIsLoggedIn(true);
      }
    } catch (error) {
      if (axios.isAxiosError(error)) {
        if (error.response?.status === 500) {
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
        autoCapitalize="none"
        value={loginId}
        onChangeText={text => setLoginId(text)}
      />

      <CustomTextInput
        style={[defaultStyle.input, {flex: 1}]}
        placeholder="비밀번호"
        right={
          <Icon
            name={passwordVisible ? 'eye' : 'eye-off'}
            onPress={() => setPasswordVisible(!passwordVisible)}
            size={20}
            color={'#ccc'}
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
