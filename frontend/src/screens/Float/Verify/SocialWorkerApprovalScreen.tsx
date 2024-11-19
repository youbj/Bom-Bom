import React, {useEffect, useState} from 'react';
import {View, FlatList, TouchableOpacity, StyleSheet} from 'react-native';
import CustomText from '../../../components/CustomText';
import BackButton from '../../../components/BackButton';
import CustomAlert from '../../../components/CustomAlert';
import instance from '../../../api/axios';
import defaultStyle from '../../../styles/DefaultStyle';

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
  const [alertVisible, setAlertVisible] = useState(false);
  const [alertTitle, setAlertTitle] = useState('');
  const [alertMessage, setAlertMessage] = useState('');
  const [alertOnClose, setAlertOnClose] = useState<() => void>(() => {});

  // Alert 보여주기 함수
  const showAlert = (title: string, message: string, onClose?: () => void) => {
    setAlertTitle(title);
    setAlertMessage(message);
    setAlertVisible(true);
    setAlertOnClose(() => {
      const closeModal = () => setAlertVisible(false);
      return onClose
        ? () => {
            onClose();
            closeModal();
          }
        : closeModal;
    });
  };

  // 데이터 가져오기 함수
  const fetchRequests = async () => {
    try {
      const response = await instance.get(`/members/approve/list`);
      setRequests(response.data);
    } catch (error) {
      console.error('Failed to fetch requests:', error);
      showAlert('오류', '데이터를 불러오는 데 실패했습니다.');
    }
  };

  useEffect(() => {
    fetchRequests();
  }, []);

  const handleApprove = async (id: number) => {
    try {
      const response = await instance.post(`/members/approve`, {id});
      if (response.status === 200) {
        showAlert('승인 완료', '요청이 승인되었습니다.', fetchRequests);
      }
    } catch (error) {
      console.error('Failed to approve request:', error);
      showAlert('승인 실패', '요청을 승인하는 중 오류가 발생했습니다.');
    }
  };

  const handleReject = async (id: number) => {
    try {
      const response = await instance.post(`/members/reject`, {id});
      if (response.status === 200) {
        showAlert('거절 완료', '요청이 거절되었습니다.', fetchRequests);
      }
    } catch (error) {
      console.error('Failed to reject request:', error);
      showAlert('거절 실패', '요청을 거절하는 중 오류가 발생했습니다.');
    }
  };

  const renderRequest = ({item}: {item: Request}) => (
    <View style={styles.card}>
      <View style={styles.textContainer}>
        <CustomText style={styles.seniorInfo}>
          {item.seniorName} ({item.seniorAge}세) {item.seniorPhoneNumber}
        </CustomText>
        <CustomText style={styles.familyInfo}>
          보호자 : {item.familyName} {item.familyPhoneNumber}
        </CustomText>
      </View>
      <View style={styles.buttonContainer}>
        <TouchableOpacity
          style={[styles.button, styles.approveButton]}
          onPress={() => handleApprove(item.id)}>
          <CustomText style={styles.buttonText}>승인</CustomText>
        </TouchableOpacity>
        <TouchableOpacity
          style={[styles.button, styles.rejectButton]}
          onPress={() => handleReject(item.id)}>
          <CustomText style={styles.buttonText}>거절</CustomText>
        </TouchableOpacity>
      </View>
    </View>
  );

  return (
    <>
      <View style={defaultStyle.container}>
        <BackButton />
        <CustomText style={styles.title}>승인 요청 목록</CustomText>
        <FlatList
          data={requests}
          renderItem={renderRequest}
          keyExtractor={item => item.id.toString()}
          contentContainerStyle={styles.listContainer}
        />
      </View>

      {/* CustomAlert 추가 */}
      <CustomAlert
        visible={alertVisible}
        title={alertTitle}
        message={alertMessage}
        onClose={() => {
          alertOnClose(); // 사용자 정의 콜백 실행
          setAlertVisible(false); // 모달 닫기
        }}
      />
    </>
  );
};

const styles = StyleSheet.create({
  title: {
    fontSize: 25,
    fontWeight: '600',
    marginBottom: 16,
    marginTop: 50,
  },
  listContainer: {
    paddingBottom: 20,
    paddingHorizontal: 10,
  },
  card: {
    backgroundColor: '#FED7C3',
    borderRadius: 10,
    padding: 16,
    marginVertical: 8,
    width: '100%',
    shadowColor: '#000',
    shadowOpacity: 0.1,
    shadowRadius: 6,
    elevation: 2,
  },
  textContainer: {
    marginBottom: 16,
  },
  seniorInfo: {
    fontSize: 18,
    fontWeight: '600',
    marginBottom: 5,
    paddingLeft: 5,
  },
  familyInfo: {
    fontSize: 14,
    color: '#555',
    marginBottom: 10,
    paddingLeft: 5,
  },
  buttonContainer: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    paddingHorizontal: 10,
    gap: 50,
  },
  button: {
    flex: 1,
    paddingVertical: 10,
    borderRadius: 8,
    alignItems: 'center',
    justifyContent: 'center',
    marginHorizontal: 5,
  },
  approveButton: {
    backgroundColor: '#A8D98A',
  },
  rejectButton: {
    backgroundColor: '#FF8A80',
  },
  buttonText: {
    color: '#fff',
    fontWeight: '600',
    fontSize: 14,
  },
});

export default SocialWorkerApprovalScreen;
