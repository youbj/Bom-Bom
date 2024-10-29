import React, {useState} from 'react';
import {View, Text, Image, TouchableOpacity} from 'react-native';

import defaultStyle from '../styles/DefaultStyles';
import loginStyles from '../styles/LoginStyles';
import CustomText from '../components/CustomText';
import CustomTextInput from '../components/CustomTextInput';
import Icon from 'react-native-vector-icons/MaterialCommunityIcons';

const LoginScreen = (): JSX.Element => {
  const [passwordVisible, setPasswordVisible] = useState<boolean>(false);

  return (
    <View style={defaultStyle.container}>
      <Image
        source={require('../assets/images/logo.png')}
        style={loginStyles.logo}
      />
      <CustomText style={loginStyles.title}>봄 : 봄</CustomText>
      <View style={loginStyles.longSpace} />

      <CustomTextInput
        style={loginStyles.input}
        placeholder="아이디"
        autoCapitalize="none"
      />

      <CustomTextInput
        style={[loginStyles.input, { flex: 1 }]}
        placeholder="비밀번호"
        right={
          <Icon
            name={passwordVisible ? "eye" : "eye-off"}
            onPress={() => setPasswordVisible(!passwordVisible)}
            size = {20}
            color = {'#ccc'}
          />
        }
        secureTextEntry={passwordVisible}
      />

      <TouchableOpacity style={loginStyles.button}>
        <CustomText style={loginStyles.buttonText}>로그인</CustomText>
      </TouchableOpacity>
      <View style={loginStyles.space} />
      <TouchableOpacity
        style={[loginStyles.button, loginStyles.transparentButton]}>
        <CustomText style={loginStyles.text}>
          아직 회원이 아니시라면?
        </CustomText>
      </TouchableOpacity>
    </View>
  );
};

export default LoginScreen;
