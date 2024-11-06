// src/screens/Verify/FamilyVerifyRequestScreen.tsx
import React, { useState } from 'react';
import { View, Button } from 'react-native';
import CustomText from '../../../components/CustomText';
import CustomTextInput from '../../../components/CustomTextInput';
import FamilyStyle from '../../../styles/Float/FamilyStyle';
import BackButton from '../../../components/BackButton';

const FamilyVerifyRequestScreen: React.FC = () => {
  const [socialWorkerName, setSocialWorkerName] = useState('');
  const [elderlyName, setElderlyName] = useState('');
  const [age, setAge] = useState('');
  const [phoneNumber, setPhoneNumber] = useState('');

  const handleSubmitRequest = () => {
    console.log('Request submitted:', {
      socialWorkerName,
      elderlyName,
      age,
      phoneNumber,
    });
  };

  return (
    <View style={FamilyStyle.container}>
      <BackButton/>
      <CustomText style={FamilyStyle.title}>인증 요청</CustomText>
      <View style={FamilyStyle.inputContainer}>
        <CustomText style={FamilyStyle.label}>복지사 이름</CustomText>
        <CustomTextInput
          style={FamilyStyle.input}
          placeholder="복지사 이름을 입력하세요"
          value={socialWorkerName}
          onChangeText={setSocialWorkerName}
        />
      </View>
      <View style={FamilyStyle.inputContainer}>
        <CustomText style={FamilyStyle.label}>노인 이름</CustomText>
        <CustomTextInput
          style={FamilyStyle.input}
          placeholder="노인 이름을 입력하세요"
          value={elderlyName}
          onChangeText={setElderlyName}
        />
      </View>
      <View style={FamilyStyle.inputContainer}>
        <CustomText style={FamilyStyle.label}>나이</CustomText>
        <CustomTextInput
          style={FamilyStyle.input}
          placeholder="나이를 입력하세요"
          value={age}
          onChangeText={setAge}
          keyboardType="numeric"
        />
      </View>
      <View style={FamilyStyle.inputContainer}>
        <CustomText style={FamilyStyle.label}>전화번호</CustomText>
        <CustomTextInput
          style={FamilyStyle.input}
          placeholder="010-1234-5678"
          value={phoneNumber}
          onChangeText={setPhoneNumber}
          keyboardType="phone-pad"
        />
      </View>
      <Button title="승인 요청 보내기" onPress={handleSubmitRequest} color="#FF8A80" />
    </View>
  );
};

export default FamilyVerifyRequestScreen;
