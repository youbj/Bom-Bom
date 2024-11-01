import React, { useState, useEffect } from 'react';
import { View, ScrollView, TouchableOpacity } from 'react-native';
import CustomText from '../components/CustomText';
import defaultStyle from '../styles/DefaultStyle';
import MainStyle from '../styles/MainStyle';
import CustomTextInput from '../components/CustomTextInput';
import Icon from 'react-native-vector-icons/MaterialCommunityIcons';

type Elder = {
  name: string;
  address: string;
  age: number;
  gender: string;
};

const MainScreen = () => {
  const [type, setType] = useState('S');
  const [title, setTitle] = useState('');
  const [result, setResult] = useState('');
  const [filteredResult, setFilteredResult] = useState<Elder[]>([]);
  const [nameCount, setNameCount] = useState(1);
  const [ageCount, setAgeCount] = useState(0);

  const elderList: Elder[] = [
    { name: '박정의', address: '서울시 강남구', age: 75, gender: '여' },
    { name: '유병주', address: '서울시 강서구', age: 77, gender: '남' },
    { name: '윤정섭', address: '서울시 강북구', age: 81, gender: '남' },
    { name: '이강현', address: '서울시 강동구', age: 73, gender: '여' },
    { name: '임동길', address: '서울시 종로구', age: 88, gender: '남' },
  ];

  useEffect(() => {
    setTitle(type === 'S' ? '담당 독거 노인 목록' : '나의 가족 목록');
    const sortedByName = [...elderList].sort((a, b) => a.name.localeCompare(b.name));
    setFilteredResult(sortedByName);
  }, [type]);

  const handleSearch = () => {
    const filtered = result
      ? elderList.filter(elder => elder.name.includes(result))
      : elderList;
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
          <TouchableOpacity onPress={sortByAge} style={{flexDirection: 'row'}}>
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
              style={{marginTop: -1, marginLeft: -3}}
            />
          </TouchableOpacity>
        </View>
        <TouchableOpacity style={{ paddingRight: 3 }}>
          <Icon name="account-plus" size={30} />
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
                  {elder.age} / {elder.gender}
                </CustomText>
              </View>
            </TouchableOpacity>
            <View style={{ height: 10 }} />
          </View>
        ))}
      </ScrollView>
    </View>
  );
};

export default MainScreen;
