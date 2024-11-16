import React, {useState, useEffect, useCallback} from 'react';
import {View, ScrollView, TouchableOpacity, Alert} from 'react-native';
import {useNavigation, useFocusEffect} from '@react-navigation/native';
import EncryptedStorage from 'react-native-encrypted-storage';
import CustomText from '../components/CustomText';

import defaultStyle from '../styles/DefaultStyle';
import MainStyle from '../styles/MainStyle';
import CustomTextInput from '../components/CustomTextInput';
import Icon from 'react-native-vector-icons/MaterialCommunityIcons';
import {
  MainToEnrollNavigationProp,
  MainToDetailNavigationProp,
} from '../../types/navigation.d';
import instance from '../api/axios';
import LogoutButton from '../components/LogoutButton';
import {Dimensions} from 'react-native';

type Elder = {
  index: number;
  seniorId: number;
  name: string;
  address: string;
  age: number;
  gender: string;
};

const MainScreen = (): JSX.Element => {
  const [type, setType] = useState<string>('');
  const [title, setTitle] = useState('');
  const [result, setResult] = useState('');
  const [elderList, setElderList] = useState<Elder[]>([]);
  const [filteredResult, setFilteredResult] = useState<Elder[]>([]);
  const [nameCount, setNameCount] = useState(1);
  const [ageCount, setAgeCount] = useState(0);
  const [deleteMode, setDeleteMode] = useState(false);
  const [markedForDeletion, setMarkedForDeletion] = useState<Set<number>>(
    new Set(),
  );
  const screenWidth = Dimensions.get('window').width;

  const enrollNavigation = useNavigation<MainToEnrollNavigationProp>();
  const detailNavigation = useNavigation<MainToDetailNavigationProp>();

  const onPressEnroll = () => enrollNavigation.navigate('Enroll');

  const toggleDeleteMode = () => {
    setDeleteMode(!deleteMode);
    setMarkedForDeletion(new Set());
  };

  const toggleSelection = (seniorId: number) => {
    setMarkedForDeletion(prev => {
      const updated = new Set(prev);
      if (updated.has(seniorId)) {
        updated.delete(seniorId);
      } else {
        updated.add(seniorId);
      }
      return updated;
    });
  };

  const saveDeletions = async () => {
    try {
      // 각 seniorId에 대해 delete 요청을 보냄
      await Promise.all(
        Array.from(markedForDeletion).map(seniorId =>
          instance.delete(`/seniors/delete?senior-id=${seniorId}`),
        ),
      );
      setDeleteMode(false);
      setMarkedForDeletion(new Set());
      Alert.alert('삭제 완료', '선택한 항목이 삭제되었습니다.');

      // 삭제 완료 후 최신 데이터를 다시 조회
      fetchElderList();
    } catch (error) {
      Alert.alert('삭제 실패', '항목을 삭제하는 데 실패했습니다.');
      console.error('삭제 오류:', error);
    }
  };

  const fetchElderList = async () => {
    try {
      const response = await instance.get(`/seniors/list`);
      setElderList(response.data);
      setFilteredResult(response.data);
    } catch (error) {
      Alert.alert('데이터를 불러오는 데 실패했습니다.');
    }
  };

  const onPressDetail = (seniorId: number) =>
    detailNavigation.navigate('Detail', {seniorId});

  useEffect(() => {
    const fetchType = async () => {
      try {
        const session = await EncryptedStorage.getItem('user_session');
        setType(session ? JSON.parse(session).type : '');
      } catch (error) {
        console.error('type 가져오기 오류:', error);
      }
    };
    fetchType();
  }, []);

  useFocusEffect(
    useCallback(() => {
      fetchElderList();
      setDeleteMode(false);
    }, []),
  );

  useEffect(() => {
    setTitle(
      type === 'SOCIAL_WORKER' ? '담당 독거 노인 목록' : '나의 가족 목록',
    );
  }, [type]);

  const handleSearch = (text: string) => {
    setResult(text);
    const filtered = text
      ? elderList.filter(elder => elder.name.includes(text))
      : elderList;
    setFilteredResult(filtered);
  };

  const sortByName = () => {
    if (ageCount > 0) setAgeCount(0);
    const updatedCount = (nameCount + 1) % 3 || 1;
    setNameCount(updatedCount);

    const sorted =
      updatedCount === 2
        ? [...filteredResult].sort((a, b) => b.name.localeCompare(a.name))
        : [...filteredResult].sort((a, b) => a.name.localeCompare(b.name));
    setFilteredResult(sorted);
  };

  const sortByAge = () => {
    if (nameCount > 0) setNameCount(0);
    const updatedCount = (ageCount + 1) % 3 || 1;
    setAgeCount(updatedCount);

    const sorted =
      updatedCount === 2
        ? [...filteredResult].sort((a, b) => a.age - b.age)
        : [...filteredResult].sort((a, b) => b.age - a.age);
    setFilteredResult(sorted);
  };

  return (
    <View
      style={[
        defaultStyle.container,
        {alignItems: 'flex-start', paddingTop: 50},
      ]}>
      <LogoutButton />
      <CustomText style={MainStyle.title}>{title}</CustomText>
      <CustomTextInput
        style={{...defaultStyle.input, marginBottom: 5}}
        placeholder="이름으로 검색하세요"
        autoCorrect={false}
        autoCapitalize="none"
        right={
          <TouchableOpacity onPress={() => handleSearch(result)}>
            <Icon name="account-search-outline" size={20} color={'black'} />
          </TouchableOpacity>
        }
        onChangeText={handleSearch}
        onSubmitEditing={() => handleSearch(result)}
      />
      <View style={MainStyle.menu}>
        <View style={MainStyle.arr}>
          <TouchableOpacity onPress={sortByName}>
            <CustomText
              style={{
                ...MainStyle.arrText,
                color: nameCount > 0 ? '#FF8A80' : '#000000',
              }}>
              이름 순 {nameCount === 2 ? '(ㅎ)' : '(ㄱ)'}
            </CustomText>
          </TouchableOpacity>
          <View style={{width: 10}} />
          <TouchableOpacity onPress={sortByAge} style={{flexDirection: 'row'}}>
            <CustomText
              style={{
                ...MainStyle.arrText,
                color: ageCount > 0 ? '#FF8A80' : '#000000',
              }}>
              나이 순
            </CustomText>
            <Icon
              name={ageCount === 2 ? 'arrow-down-thin' : 'arrow-up-thin'}
              color={ageCount > 0 ? '#FF8A80' : '#000000'}
              size={25}
              style={{marginTop: -1, marginLeft: -3}}
            />
          </TouchableOpacity>
        </View>
        {type === 'SOCIAL_WORKER' && (
          <View style={{flexDirection: 'row'}}>
            <TouchableOpacity style={{paddingRight: 3}} onPress={onPressEnroll}>
              <Icon name="account-plus" size={30} />
            </TouchableOpacity>
            <TouchableOpacity
              onPress={toggleDeleteMode}
              style={{paddingHorizontal: 3}}>
              <Icon
                name={deleteMode ? 'close' : 'delete'}
                size={30}
                color="black"
              />
            </TouchableOpacity>
          </View>
        )}
      </View>
      <ScrollView
        contentContainerStyle={{flexGrow: 1}}
        showsVerticalScrollIndicator={false}
        style={{marginBottom: 80}}>
        {filteredResult.map((elder, index) => (
          <View
            key={index}
            style={{flexDirection: 'row', alignItems: 'center', width: '100%'}}>
            {deleteMode && (
              <TouchableOpacity
                onPress={() => toggleSelection(elder.seniorId)}
                style={{marginRight: 10}}>
                <Icon
                  name={
                    markedForDeletion.has(elder.seniorId)
                      ? 'checkbox-marked'
                      : 'checkbox-blank-outline'
                  }
                  size={24}
                  color="black"
                />
              </TouchableOpacity>
            )}
            <TouchableOpacity
              style={[
                MainStyle.list,
                {
                  width: deleteMode ? screenWidth - 74 : '100%',
                },
              ]}
              onPress={() => onPressDetail(elder.seniorId)}>
              <View style={[MainStyle.subList, {alignItems: 'flex-start'}]}>
                <CustomText style={MainStyle.listText}>{elder.name}</CustomText>
                <CustomText style={MainStyle.addText}>
                  {elder.address}
                </CustomText>
              </View>
              <View style={[MainStyle.subList, {alignItems: 'flex-end'}]}>
                <CustomText style={MainStyle.listText}>
                  {elder.age} /{' '}
                  {elder.gender === 'MALE'
                    ? '남'
                    : elder.gender === 'FEMALE'
                    ? '여'
                    : elder.gender}
                </CustomText>
              </View>
            </TouchableOpacity>
          </View>
        ))}
        {deleteMode && (
          <View
            style={{
              flexDirection: 'row',
              justifyContent: 'flex-end',
              marginTop: 10,
            }}>
            <TouchableOpacity style={MainStyle.button} onPress={saveDeletions}>
              <CustomText style={MainStyle.buttonText}>삭제</CustomText>
            </TouchableOpacity>
          </View>
        )}
      </ScrollView>
    </View>
  );
};

export default MainScreen;
