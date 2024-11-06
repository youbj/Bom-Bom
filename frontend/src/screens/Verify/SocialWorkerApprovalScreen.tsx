// src/screens/Verify/SocialWorkerApprovalScreen.tsx
import React from 'react';
import { View, Button, FlatList, StyleSheet } from 'react-native';
import CustomText from '../../components/CustomText';
import CustomTextInput from '../../components/CustomTextInput';

interface Request {
  id: string;
  familyName: string;
  familyPhoneNumber: string;
  elderlyName: string;
  age: string;
  phoneNumber: string;
}

const requests: Request[] = [
  { id: '1', familyName: '김가족', familyPhoneNumber: '010-1111-2222', elderlyName: '이강현', age: '75', phoneNumber: '010-1234-5678' },
  { id: '2', familyName: '박가족', familyPhoneNumber: '010-3333-4444', elderlyName: '윤정섭', age: '77', phoneNumber: '010-1234-5678' },
  { id: '3', familyName: '최가족', familyPhoneNumber: '010-5555-6666', elderlyName: '박정의', age: '73', phoneNumber: '010-1234-5678' },
  { id: '4', familyName: '정가족', familyPhoneNumber: '010-7777-8888', elderlyName: '유병주', age: '75', phoneNumber: '010-1234-5678' },
];

const SocialWorkerApprovalScreen: React.FC = () => {
  const handleApprove = (id: string) => {
    console.log(`Approved request with id: ${id}`);
  };

  const handleReject = (id: string) => {
    console.log(`Rejected request with id: ${id}`);
  };

  const renderRequest = ({ item }: { item: Request }) => (
    <View style={styles.requestItem}>
      <View style={styles.textContainer}>
        <CustomText style={styles.name}>{item.elderlyName} / {item.age} / {item.phoneNumber}</CustomText>
        <CustomText style={styles.info}>{item.familyName} / {item.familyPhoneNumber}</CustomText>
      </View>
      <View style={styles.buttonContainer}>
        <Button title="승인" onPress={() => handleApprove(item.id)} color="#4CAF50" />
        <Button title="거절" onPress={() => handleReject(item.id)} color="#FF8A80" />
      </View>
    </View>
  );

  return (
    <View style={styles.container}>
      <CustomText style={styles.title}>인원 목록</CustomText>
      <FlatList
        data={requests}
        renderItem={renderRequest}
        keyExtractor={(item) => item.id}
        contentContainerStyle={styles.listContainer}
      />
    </View>
  );
};

export default SocialWorkerApprovalScreen;

const styles = StyleSheet.create({
  container: {
    flex: 1,
    padding: 20,
    paddingBottom: 100,
    backgroundColor: '#fff',
  },
  title: {
    fontSize: 24,
    fontWeight: 'bold',
    marginBottom: 20,
    textAlign: 'center',
  },
  listContainer: {
    paddingBottom: 20,
  },
  requestItem: {
    backgroundColor: '#FED7C3',
    padding: 15,
    borderRadius: 15,
    marginBottom: 15,
    elevation: 3,
  },
  textContainer: {
    marginBottom: 10,
  },
  name: {
    fontSize: 18,
    fontWeight: 'bold',
    marginBottom: 5,
  },
  info: {
    fontSize: 14,
    color: '#555',
    marginBottom: 3,
  },
  buttonContainer: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    marginTop: 10,
  },
});
