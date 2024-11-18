import React, {useState} from 'react';
import {View, TouchableOpacity} from 'react-native';
import CustomText from '../../../components/CustomText';
import CustomTextInput from '../../../components/CustomTextInput';
import FamilyStyle from '../../../styles/Float/FamilyStyle';
import BackButton from '../../../components/BackButton';
import instance from '../../../api/axios';
import EncryptedStorage from 'react-native-encrypted-storage';
import {formatPhoneNumber} from '../../../utils/Format';
import CustomAlert from '../../../components/CustomAlert';

const FamilyVerifyRequestScreen: React.FC = () => {
  const [socialWorkerName, setSocialWorkerName] = useState('');
  const [seniorName, setElderlyName] = useState('');
  const [age, setAge] = useState('');
  const [seniorPhoneNumber, setPhoneNumber] = useState('');

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

  const handleSubmitRequest = async () => {
    try {
      const response = await instance.post(`/members/approve/request`, {
        seniorName,
        seniorPhoneNumber,
      });

      if (response.status === 200) {
        showAlert('요청 성공', '사회복지사에게 인증 요청을 보냈습니다.');
      }
    } catch (error) {
      showAlert('요청 실패', '인증 요청에 실패했습니다.');
    }
  };

  const handlePhoneNumberChange = (text: string) => {
    setPhoneNumber(formatPhoneNumber(text));
  };

  return (
    <>
      <View style={FamilyStyle.container}>
        <BackButton />
        <CustomText style={FamilyStyle.title}>인증 요청</CustomText>
        <View style={FamilyStyle.inputContainer}>
          <CustomText style={FamilyStyle.label}>노인 이름</CustomText>
          <CustomTextInput
            style={FamilyStyle.input}
            placeholder="노인 이름을 입력하세요"
            value={seniorName}
            onChangeText={setElderlyName}
          />
        </View>
        <View style={FamilyStyle.inputContainer}>
          <CustomText style={FamilyStyle.label}>전화번호</CustomText>
          <CustomTextInput
            style={FamilyStyle.input}
            placeholder="- 없이 숫자만 입력해주세요"
            value={seniorPhoneNumber}
            onChangeText={handlePhoneNumberChange}
            keyboardType="phone-pad"
          />
        </View>

        <TouchableOpacity
          style={FamilyStyle.button}
          onPress={handleSubmitRequest}>
          <CustomText style={{fontWeight: '600', fontSize: 16, color: '#fff'}}>
            승인 요청 보내기
          </CustomText>
        </TouchableOpacity>
      </View>

      {/* CustomAlert 추가 */}
      <CustomAlert
        visible={alertVisible}
        title={alertTitle}
        message={alertMessage}
        onClose={alertOnClose}
      />
    </>
  );
};

export default FamilyVerifyRequestScreen;
