import React, { useState, useEffect, useCallback } from 'react';
import { View, ScrollView, TouchableOpacity, Alert } from 'react-native';
import { useNavigation, useFocusEffect } from '@react-navigation/native';
import EncryptedStorage from 'react-native-encrypted-storage';
import axios from 'axios';
import CustomText from '../components/CustomText';

import defaultStyle from '../styles/DefaultStyle';
import MainStyle from '../styles/MainStyle';
import CustomTextInput from '../components/CustomTextInput';
import Icon from 'react-native-vector-icons/MaterialCommunityIcons';
import { MainToEnrollNavigationProp } from '../../types/navigation.d';
import instance, { localURL } from '../api/axios';
import LogoutButton from '../components/LogoutButton';

interface MainNavigatorProps {
  userType: string | null;
  setIsLoggedIn: React.Dispatch<React.SetStateAction<boolean>>;
}

type Elder = {
  index: number;
  name: string;
  address: string;
  age: number;
  gender: string;
};

const MainScreen = ({ userType, setIsLoggedIn }: MainNavigatorProps): JSX.Element => {
  const [type, setType] = useState<string>('');
  const [title, setTitle] = useState('');
  const [result, setResult] = useState('');
  const [filteredResult, setFilteredResult] = useState<Elder[]>([]);
  const [nameCount, setNameCount] = useState(1);
  const [ageCount, setAgeCount] = useState(0);
  const [deleteMode, setDeleteMode] = useState(false); // Delete mode toggle
  const [markedForDeletion, setMarkedForDeletion] = useState<Set<number>>(new Set()); // IDs marked for deletion

  const enrollNavigation = useNavigation<MainToEnrollNavigationProp>();

  const onPressEnroll = () => {
    enrollNavigation.navigate('Enroll');
  };

  // Toggle delete mode
  const toggleDeleteMode = () => {
    setDeleteMode(!deleteMode);
    setMarkedForDeletion(new Set()); // Reset marked items when toggling
  };

  const markForDeletion = (index: number) => {
    setMarkedForDeletion((prev) => {
      const updated = new Set(prev);
      if (updated.has(index)) {
        updated.delete(index); // 이미 선택된 경우 선택 해제
      } else {
        updated.add(index); // 삭제하려는 항목 선택
      }
      return updated;
    });
  
    // 삭제 모드일 때 화면에서 항목을 임시로 제거
    setFilteredResult((prev) => prev.filter((_, i) => i !== index));
  };
  

  const saveDeletions = () => {
    const updatedResult = filteredResult.filter((_, index) => !markedForDeletion.has(index));
    setFilteredResult(updatedResult);
    setDeleteMode(false); // Exit delete mode
    setMarkedForDeletion(new Set()); // Reset marked items
  };

  // EncryptedStorage에서 type 불러오기
  useEffect(() => {
    const fetchType = async () => {
      try {
        const session = await EncryptedStorage.getItem('user_session');
        const storedType = session ? JSON.parse(session).type : '';
        setType(storedType);
      } catch (error) {
        console.error('type 가져오기 오류:', error);
      }
    };

    fetchType();
  }, []);

  // elderList 데이터 가져오기
  useFocusEffect(
    useCallback(() => {
      const fetchElderList = async () => {
        try {
          const response = await instance.get(`${localURL}/seniors/list`); // 실제 API 엔드포인트로 변경하세요.
          setFilteredResult(response.data);
        } catch (error) {
          console.error('Failed to fetch elder list:', error);
          Alert.alert('데이터를 불러오는 데 실패했습니다.');
        }
      };
  
      fetchElderList();
    }, [])
  );

  // type에 따라 title 설정
  useEffect(() => {
    setTitle(type === 'SOCIAL_WORKER' ? '담당 독거 노인 목록' : '나의 가족 목록');
  }, [type]);


  const handleSearch = () => {
    const filtered = result
      ? filteredResult.filter(elder => elder.name.includes(result))
      : filteredResult;
    setFilteredResult(filtered);
  };

  const sortByName = () => {
    if (ageCount > 0) setAgeCount(0);
    const updatedCount = (nameCount + 1) % 3 || 1;
    setNameCount(updatedCount);

    const sorted = updatedCount === 2
      ? [...filteredResult].sort((a, b) => b.name.localeCompare(a.name))
      : [...filteredResult].sort((a, b) => a.name.localeCompare(b.name));
    setFilteredResult(sorted);
  };

  const sortByAge = () => {
    if (nameCount > 0) setNameCount(0);
    const updatedCount = (ageCount + 1) % 3 || 1;
    setAgeCount(updatedCount);

    const sorted = updatedCount === 2
      ? [...filteredResult].sort((a, b) => a.age - b.age)
      : [...filteredResult].sort((a, b) => b.age - a.age);
    setFilteredResult(sorted);
  };

  return (
    <View
      style={[
        defaultStyle.container,
        { alignItems: 'flex-start', paddingTop: 50 },
      ]}
    >
      <LogoutButton setIsLoggedIn={setIsLoggedIn} />
      <CustomText style={MainStyle.title}>{title}</CustomText>
      <CustomTextInput
        style={{ ...defaultStyle.input, marginBottom: 5 }}
        placeholder="이름으로 검색하세요"
        right={
          <TouchableOpacity onPress={handleSearch}>
            <Icon name="account-search-outline" size={20} color={'black'} />
          </TouchableOpacity>
        }
        onChangeText={text => setResult(text)}
        onSubmitEditing={handleSearch}
      />
      <View style={MainStyle.menu}>
        <View style={MainStyle.arr}>
          <TouchableOpacity onPress={sortByName}>
            <CustomText
              style={{
                ...MainStyle.arrText,
                color: nameCount > 0 ? '#FF8A80' : '#000000',
              }}
            >
              이름 순 {nameCount === 2 ? '(ㅎ)' : '(ㄱ)'}
            </CustomText>
          </TouchableOpacity>
          <View style={{ width: 10 }} />
          <TouchableOpacity onPress={sortByAge} style={{ flexDirection: 'row' }}>
            <CustomText
              style={{
                ...MainStyle.arrText,
                color: ageCount > 0 ? '#FF8A80' : '#000000',
              }}
            >
              나이 순
            </CustomText>
            <Icon
              name={ageCount === 2 ? 'arrow-down-thin' : 'arrow-up-thin'}
              color={ageCount > 0 ? '#FF8A80' : '#000000'}
              size={25}
              style={{ marginTop: -1, marginLeft: -3 }}
            />
          </TouchableOpacity>
        </View>
        <TouchableOpacity style={{ paddingRight: 3 }} onPress={onPressEnroll}>
          <Icon name="account-plus" size={30} />
        </TouchableOpacity>
        <TouchableOpacity style={{ paddingRight: 3 }} onPress={toggleDeleteMode}>
          <Icon name="account-minus" size={30} />
        </TouchableOpacity>
      </View>
      <ScrollView contentContainerStyle={{ flexGrow: 1 }}>
        {filteredResult.map((elder, index) => (
          <View key={index}>
            <TouchableOpacity style={MainStyle.list}>
              <View style={[MainStyle.subList, { alignItems: 'flex-start' }]}>
                <CustomText style={MainStyle.listText}>{elder.name}</CustomText>
                <CustomText style={MainStyle.addText}>
                  {elder.address}
                </CustomText>
              </View>
              <View style={[MainStyle.subList, { alignItems: 'flex-end' }]}>
                <CustomText style={MainStyle.listText}>
                  {elder.age} / {elder.gender === 'MALE' ? '남' : elder.gender === 'FEMALE' ? '여' : elder.gender}
                </CustomText>
                {deleteMode && (
                  <TouchableOpacity onPress={() => markForDeletion(index)}>
                    <Icon name="close" size={20} color={'red'} />
                  </TouchableOpacity>
                )}
              </View>
            </TouchableOpacity>
            <View style={{ height: 10 }} />
          </View>
        ))}
      </ScrollView>
      {deleteMode && (
        <TouchableOpacity style={MainStyle.button} onPress={saveDeletions}>
          <CustomText style={MainStyle.buttonText}>저장</CustomText>
        </TouchableOpacity>
      )}
    </View>
  );
};

export default MainScreen;
