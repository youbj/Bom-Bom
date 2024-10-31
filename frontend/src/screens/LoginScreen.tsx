import React, {useState} from 'react';
import {View, Image, TouchableOpacity} from 'react-native';
import {useNavigation} from '@react-navigation/native';
import {LoginScreenNavigationProp} from '../../types/navigation.d';

import defaultStyle from '../styles/DefaultStyles';
import loginStyle from '../styles/LoginStyles';
import CustomText from '../components/CustomText';
import CustomTextInput from '../components/CustomTextInput';
import Icon from 'react-native-vector-icons/MaterialCommunityIcons';

const LoginScreen = (): JSX.Element => {
  const [passwordVisible, setPasswordVisible] = useState<boolean>(false);
  const navigation = useNavigation<LoginScreenNavigationProp>();
  const onPress = () => {
    navigation.navigate('Join');
  };

  return (
    <View style={defaultStyle.container}>
      <Image
        source={require('../assets/images/logo.png')}
        style={loginStyle.logo}
      />
      <CustomText style={loginStyle.title}>봄 : 봄</CustomText>
      <View style={loginStyle.longSpace} />

      <CustomTextInput
        style={defaultStyle.input}
        placeholder="아이디"
        autoCapitalize="none"
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
        secureTextEntry={passwordVisible}
      />

      <TouchableOpacity style={loginStyle.button}>
        <CustomText style={loginStyle.buttonText}>로그인</CustomText>
      </TouchableOpacity>
      <View style={loginStyle.space} />
      <TouchableOpacity
        style={[loginStyle.button, loginStyle.transparentButton]}
        onPress={onPress}>
        <CustomText style={loginStyle.text}>아직 회원이 아니시라면?</CustomText>
      </TouchableOpacity>
    </View>
  );
};

export default LoginScreen;
