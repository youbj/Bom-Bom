import React, {useState, useCallback, useEffect} from 'react';
import {View, TouchableOpacity, Text, ScrollView, Alert} from 'react-native';
import {Calendar, LocaleConfig} from 'react-native-calendars';
import {
  useNavigation,
  useRoute,
  RouteProp,
  useFocusEffect,
} from '@react-navigation/native';
import CustomText from '../components/CustomText';
import LogoutButton from '../components/LogoutButton';
import BackButton from '../components/BackButton';
import instance from '../api/axios';
import PlanStyle from '../styles/PlanStyle';
import defaultStyle from '../styles/DefaultStyle';
import {getFontFamily} from '../utils/FontUtils';
import {
  PlanToEnrollNavigationProp,
  MainStackParamList,
} from '../../types/navigation.d';
import ScheduleModal from '../components/ScheduleModal';

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

interface Schedule {
  scheduleId: number;
  memo: string;
  startAt: string;
  endAt: string;
}

interface MarkedDate {
  [key: string]: {
    marked?: boolean;
    dots?: {color: string}[];
    selected?: boolean;
    selectedColor?: string;
  };
}

const COLORS = ['#7CFC00', '#9C27B0', '#FF4500'];

const PlanScreen = (): JSX.Element => {
  const [selectedDate, setSelectedDate] = useState('');
  const [currentYear, setCurrentYear] = useState(new Date().getFullYear());
  const [currentMonth, setCurrentMonth] = useState(
    (new Date().getMonth() + 1).toString().padStart(2, '0'),
  );
  const [markedDates, setMarkedDates] = useState<MarkedDate>({});
  const [scheduleDetails, setScheduleDetails] = useState<Schedule[]>([]);
  const [filteredSchedules, setFilteredSchedules] = useState<Schedule[]>([]);
  const [modalVisible, setModalVisible] = useState(false);
  const [selectedSchedule, setSelectedSchedule] = useState<Schedule | null>(
    null,
  );
  const [editedSchedule, setEditedSchedule] = useState({
    startAt: '',
    endAt: '',
    memo: '',
  });

  const navigation = useNavigation<PlanToEnrollNavigationProp>();
  const route = useRoute<RouteProp<MainStackParamList, 'Plan'>>();
  const {seniorId} = route.params;

  const onEnroll = () => {
    navigation.navigate('PlanEnroll', {seniorId});
  };

  const openModal = (schedule: Schedule) => {
    setSelectedSchedule(schedule);
    setEditedSchedule({
      startAt: schedule.startAt,
      endAt: schedule.endAt,
      memo: schedule.memo,
    });
    setModalVisible(true);
  };

  const closeModal = () => {
    setModalVisible(false);
    setSelectedSchedule(null);
  };

  const handleEdit = async () => {
    if (!selectedSchedule) return;

    try {
      await instance.patch(`/schedule/update`, editedSchedule, {
        params: {'schedule-id': selectedSchedule.scheduleId},
      });
      await getInfo(currentYear, currentMonth);
      closeModal();
    } catch (error) {
      console.error(error);
      Alert.alert('수정 실패', '수정 중 문제가 발생했습니다.');
    }
  };

  const handleDelete = async () => {
    if (!selectedSchedule) return;

    Alert.alert(
      '일정 삭제',
      '이 일정을 삭제하시겠습니까?',
      [
        {text: '취소', style: 'cancel'},
        {
          text: '삭제',
          style: 'destructive',
          onPress: async () => {
            try {
              await instance.delete('/schedule/delete', {
                params: {'schedule-id': selectedSchedule.scheduleId},
              });
              await getInfo(currentYear, currentMonth);
              closeModal();
            } catch (error) {
              console.error(error);
              Alert.alert('삭제 실패', '삭제 중 문제가 발생했습니다.');
            }
          },
        },
      ],
      {cancelable: true},
    );
  };

  const getInfo = async (year: number, month: string) => {
    try {
      const response = await instance.get('/schedule', {
        params: {'senior-id': seniorId, year, month},
      });
      const scheduleData: Schedule[] = response.data;

      const newMarkedDates: MarkedDate = {};
      scheduleData.forEach(schedule => {
        const startDate = schedule.startAt.split('T')[0];
        const endDate = schedule.endAt.split('T')[0];
        const color = COLORS[schedule.scheduleId % COLORS.length];

        let currentDate = new Date(startDate);
        const lastDate = new Date(endDate);

        while (currentDate <= lastDate) {
          const formattedDate = currentDate.toISOString().split('T')[0];

          if (!newMarkedDates[formattedDate]) {
            newMarkedDates[formattedDate] = {
              dots: [{color}],
              marked: true,
              selectedColor: color,
            };
          } else {
            newMarkedDates[formattedDate].dots = [
              ...(newMarkedDates[formattedDate].dots || []),
              {color},
            ];
          }

          currentDate.setDate(currentDate.getDate() + 1);
        }
      });

      setMarkedDates(newMarkedDates);
      setScheduleDetails(scheduleData);

      const updatedFilteredSchedules = scheduleData.filter(schedule => {
        const startDate = schedule.startAt.split('T')[0];
        const endDate = schedule.endAt.split('T')[0];
        return selectedDate >= startDate && selectedDate <= endDate;
      });
      setFilteredSchedules(updatedFilteredSchedules);
    } catch (error) {
      console.error(error);
    }
  };

  const handleDayPress = (date: string) => {
    setSelectedDate(date);
    const filtered = scheduleDetails.filter(schedule => {
      const startDate = schedule.startAt.split('T')[0];
      const endDate = schedule.endAt.split('T')[0];
      return date >= startDate && date <= endDate;
    });
    setFilteredSchedules(filtered);
  };

  const handleMonthChange = (date: {year: number; month: number}) => {
    const newYear = date.year;
    const newMonth = date.month.toString().padStart(2, '0');

    setCurrentYear(newYear);
    setCurrentMonth(newMonth);

    setSelectedDate('');

    getInfo(newYear, newMonth);
  };

  useFocusEffect(
    useCallback(() => {
      getInfo(currentYear, currentMonth);
    }, [currentYear, currentMonth]),
  );

  return (
    <View style={[defaultStyle.container, {justifyContent: 'flex-start'}]}>
      <BackButton />
      <LogoutButton />
      <CustomText style={PlanStyle.title}>한눈에 일정 보기</CustomText>
      <Calendar
        style={PlanStyle.calendar}
        markingType={'multi-dot'}
        onDayPress={day => handleDayPress(day.dateString)}
        onMonthChange={handleMonthChange}
        renderHeader={date => {
          const year = date.getFullYear();
          const month = (date.getMonth() + 1).toString().padStart(2, '0');
          return (
            <Text style={{fontSize: 18, fontFamily: getFontFamily('500')}}>
              {year}년 {month}월
            </Text>
          );
        }}
        markedDates={{
          ...markedDates,
          [selectedDate]: {
            ...markedDates[selectedDate],
            selected: true,
            selectedColor: 'transparent',
          },
        }}
        theme={{
          backgroundColor: 'white',
          calendarBackground: 'white',
          todayTextColor: '#FF8C69',
          selectedDayTextColor: '#1E90FF',
          textDayFontFamily: getFontFamily('600'),
          textDayHeaderFontFamily: getFontFamily('600'),
          arrowColor: '#FF8C69',
          textSectionTitleColor: '#FF8C69',
          textDayHeaderFontSize: 18,
        }}
      />
      {filteredSchedules.length > 0 && (
        <View style={PlanStyle.plan}>
          <ScrollView showsVerticalScrollIndicator={false}>
            <CustomText
              style={{fontWeight: '600', fontSize: 16, marginBottom: 10}}>
              오늘의 일정
            </CustomText>
            {filteredSchedules.map(item => (
              <TouchableOpacity
                key={item.scheduleId}
                onPress={() => openModal(item)}
                style={{paddingBottom: 3}}>
                <CustomText style={{fontWeight: '500', fontSize: 14}}>
                  {item.memo}: {item.startAt.split('T')[1].slice(0, 5)} ~{' '}
                  {item.endAt.split('T')[1].slice(0, 5)}
                </CustomText>
              </TouchableOpacity>
            ))}
          </ScrollView>
        </View>
      )}
      <ScheduleModal
        modalVisible={modalVisible}
        editedSchedule={editedSchedule}
        setEditedSchedule={setEditedSchedule}
        closeModal={closeModal}
        handleEdit={handleEdit}
        handleDelete={handleDelete}
      />
      <View style={{flex: 1, alignItems: 'flex-end'}}>
        <TouchableOpacity style={PlanStyle.button} onPress={onEnroll}>
          <CustomText style={PlanStyle.buttonText}>일정 등록</CustomText>
        </TouchableOpacity>
      </View>
    </View>
  );
};

export default PlanScreen;
