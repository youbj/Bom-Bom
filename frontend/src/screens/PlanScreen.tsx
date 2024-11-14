import React, {useState} from 'react';
import {View, Text, TouchableOpacity} from 'react-native';
import CustomText from '../components/CustomText';
import {Calendar, LocaleConfig} from 'react-native-calendars';
import PlanStyle from '../styles/PlanStyle';
import defaultStyle from '../styles/DefaultStyle';
import {getFontFamily} from '../utils/FontUtils';
import LogoutButton from '../components/LogoutButton';
import BackButton from '../components/BackButton';
import {useNavigation, useRoute, RouteProp} from '@react-navigation/native';
import {
  PlanToEnrollNavigationProp,
  MainStackParamList,
} from '../../types/navigation.d';

// LocaleConfig 설정
LocaleConfig.locales['ko'] = {
  monthNames: [
    '1월',
    '2월',
    '3월',
    '4월',
    '5월',
    '6월',
    '7월',
    '8월',
    '9월',
    '10월',
    '11월',
    '12월',
  ],
  dayNames: [
    '일요일',
    '월요일',
    '화요일',
    '수요일',
    '목요일',
    '금요일',
    '토요일',
  ],
  dayNamesShort: ['일', '월', '화', '수', '목', '금', '토'],
  today: '오늘',
};

LocaleConfig.defaultLocale = 'ko';

type PlanScreenRouteProp = RouteProp<MainStackParamList, 'Plan'>;

const PlanScreen = () => {
  const [selectedDate, setSelectedDate] = useState('');
  const today = new Date().toISOString().split('T')[0]; // 오늘 날짜 가져오기
  const navigation = useNavigation<PlanToEnrollNavigationProp>();
  const route = useRoute<PlanScreenRouteProp>();
  const {seniorId} = route.params;
  const onEnroll = () => {
    navigation.navigate('PlanEnroll', {seniorId});
  };
  return (
    <View style={[defaultStyle.container, {justifyContent: 'flex-start'}]}>
      <BackButton />
      <LogoutButton />
      <CustomText style={PlanStyle.title}>한눈에 일정 보기</CustomText>
      <Calendar
        style={PlanStyle.calendar}
        renderHeader={date => {
          const year = date.getFullYear();
          const month = (date.getMonth() + 1).toString().padStart(2, '0');
          return (
            <CustomText style={PlanStyle.subTitle}>
              {`${year}년 ${month}월`}
            </CustomText>
          );
        }}
        onDayPress={day => {
          setSelectedDate(day.dateString);
        }}
        markedDates={{
          [selectedDate]: {selected: true, selectedColor: '#FF8C69'},
          [today]: {selected: true, selectedColor: '#FFA500'}, // 오늘 날짜 스타일 추가
        }}
        theme={{
          backgroundColor: 'white',
          calendarBackground: 'white',
          todayTextColor: 'red',
          textDayFontFamily: getFontFamily('600'),
          textDayHeaderFontFamily: getFontFamily('600'),
          selectedDayBackgroundColor: '#FF8C69',
          arrowColor: '#FF8C69',
          textSectionTitleColor: '#FF8C69',
          textDayHeaderFontSize: 18,
        }}
        dayComponent={({date, state}) => {
          if (!date) return null;
          const isSelected = selectedDate === date.dateString;
          const isToday = date.dateString === today;
          return (
            <TouchableOpacity
              onPress={() => setSelectedDate(date.dateString)}
              style={{
                backgroundColor: isSelected ? '#FF8C69' : 'white', // 오늘 날짜 배경색 지정
                borderRadius: 5,
                alignItems: 'center',
                width: 35,
                height: 35,
                justifyContent: 'center',
              }}>
              <Text
                style={{
                  color: isSelected
                    ? 'white'
                    : isToday
                    ? '#FF8C69'
                    : state === 'disabled'
                    ? 'gray'
                    : 'black',
                  fontFamily: getFontFamily('600'),
                  fontSize: 16,
                }}>
                {date.day}
              </Text>
            </TouchableOpacity>
          );
        }}
        firstDay={0}
      />
      <TouchableOpacity style={PlanStyle.button} onPress={onEnroll}>
        <CustomText style={PlanStyle.buttonText}>일정 등록</CustomText>
      </TouchableOpacity>
    </View>
  );
};

export default PlanScreen;
