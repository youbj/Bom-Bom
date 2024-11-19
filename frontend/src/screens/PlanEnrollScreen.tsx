import React, {useState} from 'react';
import {View, TouchableOpacity} from 'react-native';
import CustomText from '../components/CustomText';
import CustomTextInput from '../components/CustomTextInput';
import defaultStyle from '../styles/DefaultStyle';
import PlanEnrollStyle from '../styles/PlanEnrollStyle';
import BackButton from '../components/BackButton';
import LogoutButton from '../components/LogoutButton';
import {useRoute, RouteProp, useNavigation} from '@react-navigation/native';
import {MainStackParamList} from '../../types/navigation.d';
import instance from '../api/axios';
import {renderDateTimeInput} from '../utils/RenderDateTimeInput';
import CustomAlert from '../components/CustomAlert';

type PlanEnrollScreenRouteProp = RouteProp<MainStackParamList, 'PlanEnroll'>;

const PlanEnrollScreen = () => {
  const route = useRoute<PlanEnrollScreenRouteProp>();
  const {seniorId} = route.params;
  const navigation = useNavigation();

  const [startDate, setStartDate] = useState('');
  const [startTime, setStartTime] = useState('');
  const [endDate, setEndDate] = useState('');
  const [endTime, setEndTime] = useState('');
  const [memo, setMemo] = useState('');

  // CustomAlert 상태 관리
  const [alertState, setAlertState] = useState({
    visible: false,
    title: '',
    message: '',
    onConfirm: () => setAlertState(prev => ({...prev, visible: false})),
  });

  const showAlert = (
    title: string,
    message: string,
    onConfirm?: () => void,
  ) => {
    setAlertState({
      visible: true,
      title,
      message,
      onConfirm:
        onConfirm || (() => setAlertState(prev => ({...prev, visible: false}))),
    });
  };

  const combineTime = (date: string, time: string): string =>
    `${date}T${time}:00`;

  const handleSave = async () => {
    if (!startDate || !startTime || !memo) {
      showAlert('입력 오류', '시작 일정, 시간, 메모는 필수 입력 사항입니다.');
      return;
    }

    const requestData: {
      seniorId: number;
      startAt: string;
      endAt?: string; // 선택적 필드
      memo: string;
    } = {
      seniorId,
      startAt: combineTime(startDate, startTime),
      memo,
    };

    // endDate와 endTime이 모두 입력된 경우에만 endAt 추가
    if (endDate && endTime) {
      requestData.endAt = combineTime(endDate, endTime);
    }

    try {
      const response = await instance.post('/schedule/regist', requestData);
      if (response.status === 200) {
        showAlert('성공', '일정이 성공적으로 등록되었습니다.', () =>
          navigation.goBack(),
        );
      }
    } catch (error) {
      console.error('Error saving schedule:', error);
      showAlert('오류', '일정을 저장하는 중 오류가 발생했습니다.');
    }
  };

  return (
    <View
      style={[
        defaultStyle.container,
        {alignItems: 'flex-start', justifyContent: 'flex-start'},
      ]}>
      <BackButton />
      <LogoutButton />
      <CustomText style={PlanEnrollStyle.title}>일정 등록하기</CustomText>

      {renderDateTimeInput(
        '시작 일정',
        startDate,
        setStartDate,
        startTime,
        setStartTime,
      )}

      {renderDateTimeInput(
        '종료 일정',
        endDate,
        setEndDate,
        endTime,
        setEndTime,
      )}

      <CustomText style={PlanEnrollStyle.subTitle}>메모</CustomText>
      <CustomTextInput
        placeholder="메모를 입력하세요"
        value={memo}
        onChangeText={setMemo}
        style={defaultStyle.input}
      />

      <View style={{alignItems: 'flex-end', width: '100%'}}>
        <TouchableOpacity onPress={handleSave} style={PlanEnrollStyle.button}>
          <CustomText style={PlanEnrollStyle.buttonText}>저장</CustomText>
        </TouchableOpacity>
      </View>

      {/* CustomAlert 추가 */}
      <CustomAlert
        visible={alertState.visible}
        title={alertState.title}
        message={alertState.message}
        onClose={alertState.onConfirm}
      />
    </View>
  );
};

export default PlanEnrollScreen;
