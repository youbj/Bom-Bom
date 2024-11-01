import React, {useState} from 'react';
import {View, TouchableOpacity, ScrollView} from 'react-native';
import {useNavigation, useRoute} from '@react-navigation/native';
import {
  JoinDetailRouteProp,
  BackToLoginNavigationProp,
} from '../../../types/navigation.d';

import CustomText from '../../components/CustomText';
import CustomTextInput from '../../components/CustomTextInput';
import defaultStyle from '../../styles/DefaultStyle';
import joinDetailStyle from '../../styles/Auth/JoinDetailStyle';

const JoinDetailScreen = (): JSX.Element => {
  const navigation = useNavigation<BackToLoginNavigationProp>();
  const route = useRoute<JoinDetailRouteProp>();
  const {isType} = route.params;
  const [password, setPassword] = useState('');
  const [passwordConfirm, setPasswordConfirm] = useState('');
  const [phoneNumber, setPhoneNumber] = useState('');

  const onPress = () => {
    navigation.navigate('Login');
  };

  const isPasswordLongEnough = password.length >= 8;
  const isPasswordMatching =
    password && passwordConfirm && password === passwordConfirm;
  const formatPhoneNumber = (input: string) => {
    const numbers = input.replace(/[^\d]/g, '');

    if (numbers.length < 4) return numbers;
    if (numbers.length < 8)
      return `${numbers.slice(0, 3)} - ${numbers.slice(3)}`;
    return `${numbers.slice(0, 3)}-${numbers.slice(3, 7)}-${numbers.slice(7)}`;
  };

  const fields = [
    {
      label: '아이디',
      placeholder: '아이디',
      autoCapitalize: 'none' as const,
      hasButton: true,
      buttonText: '중복 확인',
    },
    {
      label: '비밀번호',
      placeholder: '비밀번호는 8자 이상 입력해주세요',
      secureTextEntry: true,
      onChangeText: setPassword,
    },
    {
      label: '비밀번호 확인',
      placeholder: '같은 비밀번호를 입력해주세요',
      secureTextEntry: true,
      onChangeText: setPasswordConfirm,
    },
    {label: '이름', placeholder: '이름'},
    ...(isType === 'SOCIAL_WORKER'
      ? [
          {
            label: '자격번호',
            placeholder: '자격번호',
            hasButton: true,
            buttonText: '번호 확인',
          },
        ]
      : []),
    {
      label: '핸드폰 번호',
      placeholder: '010-1234-5678',
      keyboardType: 'phone-pad' as const,
      onChangeText: (text: string) => setPhoneNumber(formatPhoneNumber(text)),
    },
  ];

  return (
    <ScrollView style={{backgroundColor: 'white'}}>
      <View style={defaultStyle.container}>
        <CustomText style={joinDetailStyle.title}>회원 가입</CustomText>
        <View style={joinDetailStyle.space}></View>
        {fields.map((field, index) => (
          <View key={index} style={joinDetailStyle.subContainer}>
            <CustomText style={joinDetailStyle.subtitle}>
              {field.label}
            </CustomText>
            <View
              style={[
                joinDetailStyle.subSpace,
                (field.label === '아이디' || field.label === '자격번호') && {
                  width: '75%',
                },
              ]}>
              <CustomTextInput
                style={joinDetailStyle.input}
                placeholder={field.placeholder}
                autoCapitalize={field.autoCapitalize}
                secureTextEntry={field.secureTextEntry}
                keyboardType={field.keyboardType}
                value={field.label === '핸드폰 번호' ? phoneNumber : undefined}
                onChangeText={field.onChangeText}
              />
              {field.hasButton && (
                <TouchableOpacity style={joinDetailStyle.button}>
                  <CustomText style={joinDetailStyle.buttonText}>
                    {field.buttonText}
                  </CustomText>
                </TouchableOpacity>
              )}
            </View>
            {field.label === '비밀번호' &&
              password.length > 0 &&
              !isPasswordLongEnough && (
                <CustomText
                  style={{
                    color: 'red',
                    marginLeft: 5,
                    marginTop: -5,
                    marginBottom: 10,
                  }}>
                  비밀번호는 8자 이상 입력하셔야 합니다.
                </CustomText>
              )}

            {field.label == '비밀번호 확인' && passwordConfirm.length > 0 && (
              <CustomText
                style={{
                  color: isPasswordMatching ? 'green' : 'red',
                  marginLeft: 5,
                  marginTop: -5,
                  marginBottom: 10,
                }}>
                {isPasswordMatching
                  ? '비밀번호가 일치합니다.'
                  : '비밀번호가 일치하지 않습니다.'}
              </CustomText>
            )}
          </View>
        ))}
        <View style={{marginTop: 30}}>
          <TouchableOpacity style={joinDetailStyle.button} onPress={onPress}>
            <CustomText style={joinDetailStyle.buttonText}>가입하기</CustomText>
          </TouchableOpacity>
        </View>
      </View>
    </ScrollView>
  );
};

export default JoinDetailScreen;
