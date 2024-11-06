// src/screens/Verify/SocialWorkerApprovalScreen.tsx
import React from 'react';
import { View, Button, FlatList } from 'react-native';
import CustomText from '../../../components/CustomText';
import SocialWorkerStyle from '../../../styles/Float/SocialWorkerStyle';
import BackButton from '../../../components/BackButton';


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
    <View style={SocialWorkerStyle.requestItem}>
      <View style={SocialWorkerStyle.textContainer}>
        <CustomText style={SocialWorkerStyle.name}>{item.elderlyName} / {item.age} / {item.phoneNumber}</CustomText>
        <CustomText style={SocialWorkerStyle.info}>{item.familyName} / {item.familyPhoneNumber}</CustomText>
      </View>
      <View style={SocialWorkerStyle.buttonContainer}>
        <Button title="승인" onPress={() => handleApprove(item.id)} color="#4CAF50" />
        <Button title="거절" onPress={() => handleReject(item.id)} color="#FF8A80" />
      </View>
    </View>
  );

  return (
    <View style={SocialWorkerStyle.container}>
      <BackButton/>
      <CustomText style={SocialWorkerStyle.title}>인원 목록</CustomText>
      <FlatList
        data={requests}
        renderItem={renderRequest}
        keyExtractor={(item) => item.id}
        contentContainerStyle={SocialWorkerStyle.listContainer}
      />
    </View>
  );
};

export default SocialWorkerApprovalScreen;


