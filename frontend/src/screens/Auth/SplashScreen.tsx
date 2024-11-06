import React, {useEffect, useRef} from 'react';
import {View, Image, Animated} from 'react-native';
import {useNavigation} from '@react-navigation/native';
import {SplashScreenNavigationProp, SplashScreenProps} from '../../../types/navigation.d';
import EncryptedStorage from 'react-native-encrypted-storage';
import CookieManager from '@react-native-cookies/cookies';

import defaultStyle from '../../styles/DefaultStyle';
import splashStyle from '../../styles/Auth/SplashStyle';
import CustomText from '../../components/CustomText';

const SplashScreen = ({setIsLoggedIn}: SplashScreenProps): JSX.Element => {
  const opacity = useRef(new Animated.Value(1)).current;
  const navigation = useNavigation<SplashScreenNavigationProp>();

  // 자동 로그인 검사 함수
  const checkSession = async () => {
    try {
      const session = await EncryptedStorage.getItem('user_session');
      const sessionData = session ? JSON.parse(session) : null;
      const accessToken = sessionData?.accessToken;
      const type = sessionData?.type;
  
      const cookies = await CookieManager.get('http://10.0.2.2');
      const refreshToken = cookies.refreshToken?.value;
      
      console.log(accessToken, type, refreshToken)
      
      if (accessToken && refreshToken && type) {
        setIsLoggedIn(true);
      } else {
        navigation.navigate('Login');
      }
    } catch (error) {
      console.error('자동 로그인 확인 중 오류:', error);
      navigation.navigate('Login');
    }
  };
  

  useEffect(() => {
    const timeoutId = setTimeout(() => {
      Animated.timing(opacity, {
        toValue: 0,
        duration: 1000,
        useNativeDriver: true,
      }).start(() => {
        checkSession();
      });
    }, 1500);

    return () => clearTimeout(timeoutId);
  }, [navigation, opacity]);

  return (
    <Animated.View style={[defaultStyle.container, {opacity}]}>
      <Image
        source={require('../../assets/images/logo.png')}
        style={splashStyle.logo}
      />
      <View style={splashStyle.spacing} />
      <CustomText style={splashStyle.text}>봄 : 봄</CustomText>
    </Animated.View>
  );
};

export default SplashScreen;
