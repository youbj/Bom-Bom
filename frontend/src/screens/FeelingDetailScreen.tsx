import React, {useState, useEffect} from 'react';
import {View, TouchableOpacity, FlatList} from 'react-native';
import CustomText from '../components/CustomText';
import CustomTextInput from '../components/CustomTextInput';
import BackButton from '../components/BackButton';
import LogoutButton from '../components/LogoutButton';
import defaultStyle from '../styles/DefaultStyle';
import FeelingDetailStyle from '../styles/FeelingDetailStyle';
import Icon from 'react-native-vector-icons/MaterialCommunityIcons';
import instance from '../api/axios';
import {useRoute, RouteProp} from '@react-navigation/native';
import {MainStackParamList} from '../../types/navigation.d';
import WeeklyChart from '../components/WeeklyChart';

type FeelingScreenRouteProp = RouteProp<MainStackParamList, 'Detail'>;

interface Conv {
  avgScore: number;
  startDate: string;
  endTime: string;
}

const FeelingDetailScreen = () => {
  const route = useRoute<FeelingScreenRouteProp>();
  const {seniorId} = route.params;

  const [weeklyData, setWeeklyData] = useState<(number | null)[]>([]);
  const [convList, setConvList] = useState<Conv[]>([]);
  const [filteredList, setFilteredList] = useState<Conv[]>([]);
  const [searchQuery, setSearchQuery] = useState('');

  const fetchWeeklyData = async () => {
    try {
      const response = await instance.get('/conv/weekavg', {
        params: {
          'senior-id': seniorId,
        },
      });
      if (response.status === 200) {
        setWeeklyData(response.data);
      }
    } catch (error) {
      console.error('Failed to fetch weekly data:', error);
    }
  };

  const fetchConversations = async () => {
    try {
      const response = await instance.get('/conv/list', {
        params: {
          'senior-id': seniorId,
        },
      });
      if (response.status === 200) {
        setConvList(response.data);
        setFilteredList(response.data);
      }
    } catch (error) {
      console.error('Failed to fetch conversation list:', error);
    }
  };

  useEffect(() => {
    fetchWeeklyData();
    fetchConversations();
  }, []);

  const handleSearch = (text: string) => {
    setSearchQuery(text);
    if (text) {
      const filtered = convList.filter(conv => conv.startDate.includes(text));
      setFilteredList(filtered);
    } else {
      setFilteredList(convList);
    }
  };

  const getEmojiByScore = (score: number): string => {
    if (score <= 20) return '😢';
    if (score <= 40) return '😟';
    if (score <= 60) return '😐';
    if (score <= 80) return '🙂';
    return '😄';
  };

  return (
    <View
      style={[
        defaultStyle.container,
        {justifyContent: 'flex-start', paddingTop: 70, paddingBottom: 120},
      ]}>
      <BackButton />
      <LogoutButton />
      <CustomText style={FeelingDetailStyle.headerText}>
        주간 감정 상태
      </CustomText>
      {weeklyData.length > 0 ? (
        <WeeklyChart rawData={weeklyData} />
      ) : (
        <CustomText>Loading...</CustomText>
      )}
      <CustomTextInput
        placeholder="날짜를 입력하여 감정 상태를 살펴보세요"
        value={searchQuery}
        onChangeText={handleSearch}
        style={[defaultStyle.input, FeelingDetailStyle.searchInput]}
        right={
          <TouchableOpacity
            onPress={() => handleSearch('')}
            style={{marginRight: 8, marginTop: 19}}>
            <Icon name="calendar-search" size={20} color="black" />
          </TouchableOpacity>
        }
      />
      <FlatList
        data={filteredList}
        keyExtractor={(item, index) => index.toString()}
        showsVerticalScrollIndicator={false}
        renderItem={({item, index}) => (
          <View style={FeelingDetailStyle.listRow}>
            <View style={FeelingDetailStyle.leftContainer}>
              <View style={FeelingDetailStyle.timeline}>
                {index === 0 ||
                item.startDate !== filteredList[index - 1]?.startDate ? (
                  <>
                    <CustomText style={FeelingDetailStyle.dateText}>
                      {item.startDate}
                    </CustomText>
                  </>
                ) : (
                  <View style={FeelingDetailStyle.timelineSpacer} />
                )}
              </View>
            </View>

            <View style={FeelingDetailStyle.rightContainer}>
              <CustomText style={FeelingDetailStyle.timeText}>
                {item.endTime}
              </CustomText>
              <CustomText style={FeelingDetailStyle.emoji}>
                {getEmojiByScore(item.avgScore)}
              </CustomText>
            </View>
          </View>
        )}
        ListEmptyComponent={
          <CustomText style={FeelingDetailStyle.emptyText}>
            검색 결과가 없습니다
          </CustomText>
        }
      />
    </View>
  );
};

export default FeelingDetailScreen;
