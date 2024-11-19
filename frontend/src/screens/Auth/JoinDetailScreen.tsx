import React, {useState} from 'react';
import axios from 'axios';
import {View, TouchableOpacity, ScrollView} from 'react-native';
import {useNavigation, useRoute} from '@react-navigation/native';
import {
  JoinDetailRouteProp,
  BackToLoginNavigationProp,
} from '../../../types/navigation.d';
import {formatPhoneNumber} from '../../utils/Format';

import CustomText from '../../components/CustomText';
import CustomTextInput from '../../components/CustomTextInput';
import defaultStyle from '../../styles/DefaultStyle';
import joinDetailStyle from '../../styles/Auth/JoinDetailStyle';
import {localURL} from '../../api/axios';
import BackButton from '../../components/BackButton';
import CustomAlert from '../../components/CustomAlert';

const JoinDetailScreen = (): JSX.Element => {
  const navigation = useNavigation<BackToLoginNavigationProp>();
  const route = useRoute<JoinDetailRouteProp>();
  const {isType} = route.params;

  const [loginId, setLoginId] = useState('');
  const [name, setName] = useState('');
  const [password, setPassword] = useState('');
  const [passwordConfirm, setPasswordConfirm] = useState('');
  const [phoneNumber, setPhoneNumber] = useState('');
  const [licenseNumber, setLicenseNumber] = useState('');
  const [isIdChecked, setIsIdChecked] = useState(false);
  const [isLicenseVerified, setIsLicenseVerified] = useState(false);

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

  const checkId = async () => {
    try {
      const response = await axios.post(`${localURL}/members/checkid`, {
        loginId,
      });
      const data = response.data;

      if (data === true) {
        showAlert('중복 확인', '이미 존재하는 아이디입니다.');
      } else {
        setIsIdChecked(true);
        showAlert('중복 확인', '사용 가능한 아이디입니다.');
      }
    } catch (error) {
      showAlert('오류', '아이디 중복 확인 중 오류가 발생했습니다.');
    }
  };

  const verifyLicenseNumber = async () => {
    try {
      const response = await axios.post(`${localURL}/qualify/verify`, {
        qualifyNumber: licenseNumber,
      });
      const data = response.data;

      if (data === true) {
        setIsLicenseVerified(true);
        showAlert('번호 확인', '자격번호가 유효합니다.');
      } else {
        showAlert('번호 확인', '유효하지 않은 자격번호입니다.');
      }
    } catch (error) {
      showAlert('오류', '자격번호 확인 중 오류가 발생했습니다.');
    }
  };

  const onJoinPress = async () => {
    if (
      !loginId ||
      !password ||
      !name ||
      !isPasswordMatching ||
      !phoneNumber ||
      !isIdChecked ||
      (isType === 'SOCIAL_WORKER' && !isLicenseVerified)
    ) {
      showAlert(
        '입력 오류',
        '필수 입력 항목을 모두 입력하거나 확인 절차를 완료해주세요.',
      );
      return;
    }

    try {
      const response = await axios.post(`${localURL}/members/regist`, {
        loginId,
        password,
        name,
        phoneNumber,
        type: isType,
        ...(isType === 'SOCIAL_WORKER' && {qualifyNum: licenseNumber}),
      });

      if (response.status === 200) {
        showAlert('회원가입 성공', '회원가입에 성공하셨습니다.', () =>
          navigation.navigate('Login'),
        );
      }
    } catch (error) {
      showAlert('회원가입 실패', '회원가입 중 문제가 발생했습니다.');
    }
  };

  const isPasswordLongEnough = password.length >= 8;
  const isPasswordMatching =
    password && passwordConfirm && password === passwordConfirm;

  const fields = [
    {
      label: '아이디',
      placeholder: '아이디',
      autoCapitalize: 'none' as const,
      value: loginId,
      onChangeText: setLoginId,
      hasButton: true,
      buttonText: '중복 확인',
      onPressButton: checkId,
      isButtonDisabled: loginId.length === 0,
    },
    {
      label: '비밀번호',
      placeholder: '비밀번호는 8자 이상 입력해주세요',
      secureTextEntry: true,
      value: password,
      onChangeText: setPassword,
    },
    {
      label: '비밀번호 확인',
      placeholder: '같은 비밀번호를 입력해주세요',
      secureTextEntry: true,
      value: passwordConfirm,
      onChangeText: setPasswordConfirm,
    },
    {
      label: '이름',
      placeholder: '이름',
      value: name,
      onChangeText: setName,
    },
    ...(isType === 'SOCIAL_WORKER'
      ? [
          {
            label: '자격번호',
            placeholder: '자격번호',
            value: licenseNumber,
            onChangeText: setLicenseNumber,
            hasButton: true,
            buttonText: '번호 확인',
            onPressButton: verifyLicenseNumber,
            isButtonDisabled: licenseNumber.length === 0 || isLicenseVerified,
            editable: !isLicenseVerified,
          },
        ]
      : []),
    {
      label: '핸드폰 번호',
      placeholder: '010-1234-5678',
      keyboardType: 'phone-pad' as const,
      value: phoneNumber,
      onChangeText: (text: string) => setPhoneNumber(formatPhoneNumber(text)),
    },
  ];

  return (
    <>
      <ScrollView
        style={{backgroundColor: 'white'}}
        showsVerticalScrollIndicator={false}>
        <View style={defaultStyle.container}>
          <BackButton />
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
                  value={field.value}
                  onChangeText={field.onChangeText}
                  editable={field.editable}
                />
                {field.hasButton && (
                  <TouchableOpacity
                    style={[
                      joinDetailStyle.button,
                      field.isButtonDisabled && {backgroundColor: '#ccc'},
                    ]}
                    onPress={field.onPressButton}
                    disabled={field.isButtonDisabled}>
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
            <TouchableOpacity
              style={joinDetailStyle.button}
              onPress={onJoinPress}>
              <CustomText style={joinDetailStyle.buttonText}>
                가입하기
              </CustomText>
            </TouchableOpacity>
          </View>
        </View>
      </ScrollView>
      <CustomAlert
        visible={alertVisible}
        title={alertTitle}
        message={alertMessage}
        onClose={alertOnClose}
      />
    </>
  );
};

export default JoinDetailScreen;
