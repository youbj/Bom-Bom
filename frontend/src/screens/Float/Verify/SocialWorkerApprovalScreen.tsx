// src/screens/Verify/SocialWorkerApprovalScreen.tsx
import React, {useEffect, useState} from 'react';
import {View, Button, FlatList, Alert} from 'react-native';
import CustomText from '../../../components/CustomText';
import SocialWorkerStyle from '../../../styles/Float/SocialWorkerStyle';
import BackButton from '../../../components/BackButton';
import instance, {localURL} from '../../../api/axios';

interface Request {
  id: number;
  familyName: string;
  familyPhoneNumber: string;
  seniorName: string;
  seniorPhoneNumber: string;
  seniorAge: string;
}

const SocialWorkerApprovalScreen: React.FC = () => {
  const [requests, setRequests] = useState<Request[]>([]);

  // 데이터 가져오기 함수
  const fetchRequests = async () => {
    try {
      const response = await instance.get(`/members/approve/list`);
      setRequests(response.data);
    } catch (error) {
      console.error('Failed to fetch requests:', error);
      Alert.alert('데이터를 불러오는 데 실패했습니다.');
    }
  };

  useEffect(() => {
    fetchRequests();
  }, []);

  const handleApprove = async (id: number) => {
    try {
      const response = await instance.post(`/members/approve`, {id});
      if (response.status === 200) {
        Alert.alert('승인 완료', '요청이 승인되었습니다.');
        fetchRequests(); // 승인 후 리스트를 새로 고침
      }
    } catch (error) {
      console.error('Failed to approve request:', error);
      Alert.alert('승인 실패', '요청을 승인하는 중 오류가 발생했습니다.');
    }
  };

  const handleReject = async (id: number) => {
    try {
      const response = await instance.post(`/members/reject`, {id});
      if (response.status === 200) {
        Alert.alert('거절 완료', '요청이 거절되었습니다.');
        fetchRequests(); // 거절 후 리스트를 새로 고침
      }
    } catch (error) {
      console.error('Failed to reject request:', error);
      Alert.alert('거절 실패', '요청을 거절하는 중 오류가 발생했습니다.');
    }
  };

  const renderRequest = ({item}: {item: Request}) => (
    <View style={SocialWorkerStyle.requestItem}>
      <View style={SocialWorkerStyle.textContainer}>
        <CustomText style={SocialWorkerStyle.name}>
          {item.seniorName} / {item.seniorAge} / {item.seniorPhoneNumber}
        </CustomText>
        <CustomText style={SocialWorkerStyle.info}>
          {item.familyName} / {item.familyPhoneNumber}
        </CustomText>
      </View>
      <View style={SocialWorkerStyle.buttonContainer}>
        <Button
          title="승인"
          onPress={() => handleApprove(item.id)}
          color="#4CAF50"
        />
        <Button
          title="거절"
          onPress={() => handleReject(item.id)}
          color="#FF8A80"
        />
      </View>
    </View>
  );

  return (
    <View style={SocialWorkerStyle.container}>
      <BackButton />
      <CustomText style={SocialWorkerStyle.title}>인원 목록</CustomText>
      <FlatList
        data={requests}
        renderItem={renderRequest}
        keyExtractor={item => item.id.toString()}
        contentContainerStyle={SocialWorkerStyle.listContainer}
      />
    </View>
  );
};

export default SocialWorkerApprovalScreen;
