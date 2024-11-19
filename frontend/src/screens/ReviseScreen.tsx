import React, {useState} from 'react';
import CustomText from '../components/CustomText';
import CustomTextInput from '../components/CustomTextInput';
import {View, TouchableOpacity} from 'react-native';
import instance from '../api/axios';
import BackButton from '../components/BackButton';
import LogoutButton from '../components/LogoutButton';
import defaultStyle from '../styles/DefaultStyle';
import ReviseStyle from '../styles/ReviseStyle';
import {RouteProp, useNavigation, useRoute} from '@react-navigation/native';
import {MainStackParamList} from '../../types/navigation.d';
import {formatPhoneNumber, formatBirth} from '../utils/Format';
import CustomAlert from '../components/CustomAlert';

type ReviseScreenRouteProp = RouteProp<MainStackParamList, 'Revise'>;

const ReviseScreen = () => {
  const route = useRoute<ReviseScreenRouteProp>();
  const {detail} = route.params;
  const navigation = useNavigation();

  const [name, setName] = useState(detail.name);
  const [address, setAddress] = useState(detail.address);
  const [phoneNumber, setPhoneNumber] = useState(
    formatPhoneNumber(detail.phoneNumber),
  );
  const [birth, setBirth] = useState(formatBirth(detail.birth));
  const [gender, setGender] = useState(detail.gender);

  const [alertVisible, setAlertVisible] = useState(false);
  const [alertTitle, setAlertTitle] = useState('');
  const [alertMessage, setAlertMessage] = useState('');
  const [alertOnClose, setAlertOnClose] = useState<() => void>(() => {});

  const showAlert = (title: string, message: string, onClose?: () => void) => {
    setAlertTitle(title);
    setAlertMessage(message);
    setAlertOnClose(() => onClose || (() => setAlertVisible(false)));
    setAlertVisible(true);
  };

  const onSave = async () => {
    try {
      const response = await instance.patch(
        '/seniors/update',
        {
          name,
          phoneNumber,
          address,
          birth,
          gender,
        },
        {
          params: {'senior-id': detail.seniorId},
        },
      );
      if (response.status === 200) {
        showAlert('저장 완료', '어르신 정보가 성공적으로 수정되었습니다.', () =>
          navigation.goBack(),
        );
      }
    } catch {
      showAlert(
        '저장 실패',
        '어르신 정보를 저장하는 중 문제가 발생하였습니다.',
      );
    }
  };

  return (
    <View
      style={[
        defaultStyle.container,
        {justifyContent: 'flex-start', padding: 20},
      ]}>
      <BackButton />
      <LogoutButton />
      <CustomText style={ReviseStyle.title}>어르신 정보 수정</CustomText>

      <View style={{flexDirection: 'row', justifyContent: 'flex-start'}}>
        <View style={{flex: 1}}>
          <CustomText style={ReviseStyle.subtitle}>이름</CustomText>
          <CustomTextInput
            value={name}
            onChangeText={setName}
            style={defaultStyle.input}
            placeholder="이름을 입력하세요"
          />
        </View>
        <View>
          <CustomText style={ReviseStyle.subtitle}>성별</CustomText>
          <View style={ReviseStyle.genderContainer}>
            <TouchableOpacity
              style={[
                ReviseStyle.genderButton,
                gender === 'MALE' && ReviseStyle.selectedGender,
              ]}
              onPress={() => setGender('MALE')}>
              <CustomText style={{fontWeight: '600'}}>남</CustomText>
            </TouchableOpacity>

            <TouchableOpacity
              style={[
                ReviseStyle.genderButton,
                gender === 'FEMALE' && ReviseStyle.selectedGender,
              ]}
              onPress={() => setGender('FEMALE')}>
              <CustomText style={{fontWeight: '600'}}>여</CustomText>
            </TouchableOpacity>
          </View>
        </View>
      </View>

      <CustomText style={ReviseStyle.subtitle}>주소</CustomText>
      <CustomTextInput
        value={address}
        onChangeText={setAddress}
        style={defaultStyle.input}
        placeholder="주소를 입력하세요"
      />

      <CustomText style={ReviseStyle.subtitle}>전화번호</CustomText>
      <CustomTextInput
        value={phoneNumber}
        onChangeText={text => setPhoneNumber(formatPhoneNumber(text))}
        style={defaultStyle.input}
        keyboardType="phone-pad"
        placeholder="전화번호를 입력하세요"
      />

      <CustomText style={ReviseStyle.subtitle}>생년월일</CustomText>
      <CustomTextInput
        value={birth}
        onChangeText={text => setBirth(formatBirth(text))}
        style={defaultStyle.input}
        placeholder="생년월일을 입력하세요 (YYYY-MM-DD)"
      />

      <TouchableOpacity style={ReviseStyle.button} onPress={onSave}>
        <CustomText style={ReviseStyle.buttonText}>저 장</CustomText>
      </TouchableOpacity>

      {/* CustomAlert 추가 */}
      <CustomAlert
        visible={alertVisible}
        title={alertTitle}
        message={alertMessage}
        onClose={alertOnClose}
      />
    </View>
  );
};

export default ReviseScreen;
