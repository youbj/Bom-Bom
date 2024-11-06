// src/screens/Verify/FamilyVerifyRequestScreen.tsx
import React, { useState } from 'react';
import { View, Button, StyleSheet } from 'react-native';
import CustomText from '../../components/CustomText';
import CustomTextInput from '../../components/CustomTextInput';

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
    <View style={styles.container}>
      <CustomText style={styles.title}>인증 요청</CustomText>
      <View style={styles.inputContainer}>
        <CustomText style={styles.label}>복지사 이름</CustomText>
        <CustomTextInput
          style={styles.input}
          placeholder="복지사 이름을 입력하세요"
          value={socialWorkerName}
          onChangeText={setSocialWorkerName}
        />
      </View>
      <View style={styles.inputContainer}>
        <CustomText style={styles.label}>노인 이름</CustomText>
        <CustomTextInput
          style={styles.input}
          placeholder="노인 이름을 입력하세요"
          value={elderlyName}
          onChangeText={setElderlyName}
        />
      </View>
      <View style={styles.inputContainer}>
        <CustomText style={styles.label}>나이</CustomText>
        <CustomTextInput
          style={styles.input}
          placeholder="나이를 입력하세요"
          value={age}
          onChangeText={setAge}
          keyboardType="numeric"
        />
      </View>
      <View style={styles.inputContainer}>
        <CustomText style={styles.label}>전화번호</CustomText>
        <CustomTextInput
          style={styles.input}
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

const styles = StyleSheet.create({
  container: {
    flex: 1,
    padding: 20,
    backgroundColor: '#fff',
  },
  title: {
    fontSize: 24,
    fontWeight: 'bold',
    textAlign: 'center',
    marginBottom: 30,
  },
  inputContainer: {
    marginBottom: 15,
  },
  label: {
    fontSize: 16,
    fontWeight: '500',
    marginBottom: 5,
    color: '#333',
  },
  input: {
    height: 50,
    backgroundColor: '#FED7C3',
    borderRadius: 25,
    paddingHorizontal: 20,
    fontSize: 16,
    color: '#333',
    // shadowColor: '#000',
    // shadowOffset: { width: 0, height: 2 },
    // shadowOpacity: 0.1,
    // shadowRadius: 5,
    // elevation: 5,
  },
});
