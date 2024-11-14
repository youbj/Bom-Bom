import React, {useState} from 'react';
import {
  View,
  TextInput,
  TouchableOpacity,
  Alert,
  StyleSheet,
} from 'react-native';
import CustomText from '../components/CustomText';
import CustomTextInput from '../components/CustomTextInput';
import defaultStyle from '../styles/DefaultStyle';
import PlanEnrollStyle from '../styles/PlanEnrollStyle';
import BackButton from '../components/BackButton';
import LogoutButton from '../components/LogoutButton';
import {useRoute, RouteProp} from '@react-navigation/native';
import {MainStackParamList} from '../../types/navigation.d';
import instance from '../api/axios';

type PlanEnrollScreenRouteProp = RouteProp<MainStackParamList, 'PlanEnroll'>;

const PlanEnrollScreen = () => {
  const route = useRoute<PlanEnrollScreenRouteProp>();
  const {seniorId} = route.params;

  const [scheduleAt, setScheduleAt] = useState('');
  const [memo, setMemo] = useState('');

  const handleSave = async () => {
    if (!scheduleAt || !memo) {
      Alert.alert('입력 오류', '모든 필드를 입력해주세요.');
      return;
    }

    const requestData = {
      seniorId,
      scheduleAt,
      memo,
    };

    try {
      const response = await instance.post('/schedules/create', requestData);
      if (response.status === 200) {
        Alert.alert('성공', '일정이 성공적으로 등록되었습니다.');
      }
    } catch (error) {
      console.error('Error saving schedule:', error);
      Alert.alert('오류', '일정을 저장하는 중 오류가 발생했습니다.');
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

      <CustomText style={PlanEnrollStyle.subTitle}>시작 일정</CustomText>
      <View
        style={{
          flexDirection: 'row',
          justifyContent: 'space-between',
          width: '100%',ㅊ
        }}>
        <View style={{width: '50%'}}>
          <CustomTextInput
            placeholder="YYYY-MM-DD"
            value={scheduleAt}
            onChangeText={setScheduleAt}
            style={[defaultStyle.input, {marginHorizontal: 5}]}
          />
        </View>

        <View style={{width: '50%'}}>
          <CustomTextInput
            placeholder="YYYY-MM-DD"
            value={scheduleAt}
            onChangeText={setScheduleAt}
            style={[defaultStyle.input, {marginHorizontal: 5}]}
          />
        </View>
      </View>

      <CustomText style={PlanEnrollStyle.subTitle}>메모</CustomText>
      <CustomTextInput
        placeholder="메모를 입력하세요"
        value={memo}
        onChangeText={setMemo}
        style={defaultStyle.input}
      />

      <TouchableOpacity onPress={handleSave} style={PlanEnrollStyle.button}>
        <CustomText style={PlanEnrollStyle.buttonText}>저장</CustomText>
      </TouchableOpacity>
    </View>
  );
};

export default PlanEnrollScreen;
