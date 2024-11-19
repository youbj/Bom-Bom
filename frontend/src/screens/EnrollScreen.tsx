import React, {useState} from 'react';
import {useNavigation} from '@react-navigation/native';
import {EnrollToMainNavigationProp} from '../../types/navigation.d';
import {View, TouchableOpacity, ScrollView, StyleSheet} from 'react-native';
import {formatBirth, formatPhoneNumber} from '../utils/Format';

import enrollStyle from '../styles/EnrollStyle';
import defaultStyle from '../styles/DefaultStyle';

import CustomText from '../components/CustomText';
import CustomTextInput from '../components/CustomTextInput';
import Icon from 'react-native-vector-icons/MaterialCommunityIcons';
import BackButton from '../components/BackButton';
import LogoutButton from '../components/LogoutButton';
import instance from '../api/axios';
import CustomAlert from '../components/CustomAlert';

type Person = {
  name: string;
  gender: string;
  birth: string;
  address: string;
  phoneNumber: string;
};

const EnrollScreen = (): JSX.Element => {
  const navigation = useNavigation<EnrollToMainNavigationProp>();

  const [people, setPeople] = useState<Person[]>([]);
  const [currentPerson, setCurrentPerson] = useState<Person>({
    name: '',
    gender: '',
    birth: '',
    address: '',
    phoneNumber: '',
  });

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

  const handleAddPersonToList = () => {
    setPeople([...people, currentPerson]);
    setCurrentPerson({
      name: '',
      gender: '',
      birth: '',
      address: '',
      phoneNumber: '',
    });
  };

  const handleRemovePerson = (index: number) => {
    const updatedPeople = [...people];
    updatedPeople.splice(index, 1);
    setPeople(updatedPeople);
  };

  const fields: {label: string; placeholder: string; key: keyof Person}[] = [
    {
      label: '생년월일',
      placeholder: '- 없이 입력해주세요 (ex: 19990123)',
      key: 'birth',
    },
    {label: '주소', placeholder: '주소를 입력하세요', key: 'address'},
    {
      label: '핸드폰 번호',
      placeholder: '- 없이 입력해주세요',
      key: 'phoneNumber',
    },
  ];

  const validatePerson = (person: Person) => {
    return Object.values(person).every(value => value.trim() !== '');
  };

  const handleSave = () => {
    if (validatePerson(currentPerson)) {
      handleAddPersonToList();
      showAlert('저장 완료', '리스트에 저장되었습니다.');
    } else {
      showAlert('저장 실패', '모든 필수 정보를 입력해주세요.');
    }
  };

  const handleFinalSave = async () => {
    if (people.length === 0) {
      showAlert('저장 실패', '저장된 사람이 없습니다.');
      return;
    }

    try {
      const response = await instance.post(`/seniors/regist`, people);

      if (response.status === 200) {
        showAlert('최종 저장 완료', '모든 정보가 저장되었습니다.', () =>
          navigation.navigate('Main'),
        );
      } else {
        throw new Error('Server Error');
      }
    } catch (error) {
      console.error('Error saving data:', error);
      showAlert(
        '저장 실패',
        '서버에 데이터를 저장하는 중 오류가 발생했습니다.',
      );
    }
  };

  return (
    <View
      style={[
        defaultStyle.container,
        {paddingTop: 50, justifyContent: 'flex-start'},
      ]}>
      <BackButton />
      <LogoutButton />
      <CustomText style={enrollStyle.title}>담당 어르신 등록</CustomText>

      <ScrollView style={{width: '100%'}} showsVerticalScrollIndicator={false}>
        <View style={enrollStyle.subContainer}>
          <View style={enrollStyle.nameGenderContainer}>
            <View style={enrollStyle.nameInputContainer}>
              <CustomText style={enrollStyle.subtitle}>이름</CustomText>
              <CustomTextInput
                placeholder="이름"
                style={[defaultStyle.input, {marginBottom: 10}]}
                value={currentPerson.name}
                onChangeText={text =>
                  setCurrentPerson(prev => ({...prev, name: text}))
                }
              />
            </View>
            <View style={enrollStyle.genderInputContainer}>
              <CustomText
                style={StyleSheet.flatten([
                  enrollStyle.subtitle,
                  {marginLeft: 20},
                ])}>
                성별
              </CustomText>
              <View style={enrollStyle.genderContainer}>
                {['MALE', 'FEMALE'].map(gender => (
                  <TouchableOpacity
                    key={gender}
                    style={[
                      enrollStyle.genderButton,
                      currentPerson.gender === gender &&
                        enrollStyle.selectedGender,
                    ]}
                    onPress={() =>
                      setCurrentPerson(prev => ({...prev, gender}))
                    }>
                    <CustomText style={{fontWeight: '600'}}>
                      {gender === 'MALE' ? '남' : '여'}
                    </CustomText>
                  </TouchableOpacity>
                ))}
              </View>
            </View>
          </View>

          {fields.map(({label, placeholder, key}, index) => (
            <View key={index} style={enrollStyle.fieldContainer}>
              <CustomText style={enrollStyle.subtitle}>{label}</CustomText>
              <CustomTextInput
                placeholder={placeholder}
                style={[defaultStyle.input, {marginBottom: 10}]}
                value={currentPerson[key]}
                onChangeText={text =>
                  setCurrentPerson(prev => ({
                    ...prev,
                    [key]:
                      key === 'birth'
                        ? formatBirth(text)
                        : key === 'phoneNumber'
                        ? formatPhoneNumber(text)
                        : text,
                  }))
                }
              />
            </View>
          ))}

          <TouchableOpacity
            onPress={handleSave}
            style={enrollStyle.finalSaveButton}>
            <CustomText style={{fontWeight: '600'}}>저장</CustomText>
          </TouchableOpacity>
        </View>

        {people.length > 0 && (
          <View style={{marginTop: 20}}>
            {people.map((person, index) => (
              <View key={index} style={enrollStyle.personListItem}>
                <CustomText style={{fontWeight: '500'}}>
                  {index + 1}. {person.name} {person.birth}
                </CustomText>
                <TouchableOpacity onPress={() => handleRemovePerson(index)}>
                  <Icon name="delete" size={30} color="#F4A488" />
                </TouchableOpacity>
              </View>
            ))}
          </View>
        )}
      </ScrollView>

      {people.length > 0 && (
        <TouchableOpacity
          onPress={handleFinalSave}
          style={[enrollStyle.finalSaveButton, {marginVertical: 20}]}>
          <CustomText style={{fontWeight: '600'}}>최종 저장</CustomText>
        </TouchableOpacity>
      )}

      <CustomAlert
        visible={alertState.visible}
        title={alertState.title}
        message={alertState.message}
        onClose={alertState.onConfirm}
      />
    </View>
  );
};

export default EnrollScreen;
