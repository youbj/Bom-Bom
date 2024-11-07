// src/screens/Verify/FamilyVerifyRequestScreen.tsx
import React, { useState } from 'react';
import { View, Button, Alert } from 'react-native';
import CustomText from '../../../components/CustomText';
import CustomTextInput from '../../../components/CustomTextInput';
import FamilyStyle from '../../../styles/Float/FamilyStyle';
import BackButton from '../../../components/BackButton';
import axios from 'axios';
import instance, { localURL } from '../../../api/axios';
import EncryptedStorage from 'react-native-encrypted-storage';

const FamilyVerifyRequestScreen: React.FC = () => {
  const [socialWorkerName, setSocialWorkerName] = useState('');
  const [seniorName, setElderlyName] = useState('');
  const [age, setAge] = useState('');
  const [seniorPhoneNumber, setPhoneNumber] = useState('');

  const handleSubmitRequest = async () => {
    const session = await EncryptedStorage.getItem('user_session');
    const sessionData = session ? JSON.parse(session) : null;
    const accessToken = sessionData?.accessToken;
    console.log(accessToken);
    try{
      const response = await instance.post(
        `${localURL}/members/approve/request`,
        { seniorName, seniorPhoneNumber }
      );
      console.log(response);

      if(response.status === 200){
        Alert.alert('사회복지사에게 인증 요청을 보냈습니다.');
      }
    }
    catch(error){
      Alert.alert('인증 요청에 실패했습니다.');
    }
  };

  return (
    <View style={FamilyStyle.container}>
      <BackButton/>
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
          placeholder="010-1234-5678"
          value={seniorPhoneNumber}
          onChangeText={setPhoneNumber}
          keyboardType="phone-pad"
        />
      </View>
      <Button title="승인 요청 보내기" onPress={handleSubmitRequest} color="#FF8A80" />
    </View>
  );
};

export default FamilyVerifyRequestScreen;
