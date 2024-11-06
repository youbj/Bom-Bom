import {useState} from 'react';
import {useNavigation} from '@react-navigation/native';
import {EnrollToMainNavigationProp} from '../../types/navigation.d';
import {View, TouchableOpacity, ScrollView, Alert} from 'react-native';
import {StyleSheet} from 'react-native';

import enrollStyle from '../styles/EnrollStyle';
import defaultStyle from '../styles/DefaultStyle';

import CustomText from '../components/CustomText';
import CustomTextInput from '../components/CustomTextInput';
import Icon from 'react-native-vector-icons/MaterialCommunityIcons';
import BackButton from '../components/BackButton';
import LogoutButton from '../components/LogoutButton';

type Person = {
  name: string;
  gender: string;
  birthDate: string;
  address: string;
  phone: string;
};

const EnrollScreen = () => {
  const navigation = useNavigation<EnrollToMainNavigationProp>();

  const [people, setPeople] = useState<Person[]>([]);
  const [currentPerson, setCurrentPerson] = useState<Person>({
    name: '',
    gender: '',
    birthDate: '',
    address: '',
    phone: '',
  });

  const handleAddPersonToList = () => {
    setPeople([...people, currentPerson]);
    setCurrentPerson({
      name: '',
      gender: '',
      birthDate: '',
      address: '',
      phone: '',
    });
  };

  const handleRemovePerson = (index: number) => {
    const updatedPeople = [...people];
    updatedPeople.splice(index, 1);
    setPeople(updatedPeople);
  };

  const formatBirthDate = (input: string) => {
    const births = input.replace(/[^\d]/g, '');
    const limitedBirths = births.slice(0, 8);

    if (limitedBirths.length < 5) return births;
    if (limitedBirths.length < 7)
      return `${limitedBirths.slice(0, 4)}-${limitedBirths.slice(4)}`;
    return `${limitedBirths.slice(0, 4)}-${limitedBirths.slice(
      4,
      6,
    )}-${limitedBirths.slice(6)}`;
  };

  const formatPhoneNumber = (input: string) => {
    const numbers = input.replace(/[^\d]/g, '');
    const limitedNumbers = numbers.slice(0, 11);

    if (limitedNumbers.length < 4) return limitedNumbers;
    if (limitedNumbers.length < 8)
      return `${limitedNumbers.slice(0, 3)}-${limitedNumbers.slice(3)}`;
    return `${limitedNumbers.slice(0, 3)}-${limitedNumbers.slice(
      3,
      7,
    )}-${limitedNumbers.slice(7)}`;
  };

  const fields: {label: string; placeholder: string; key: keyof Person}[] = [
    {
      label: '생년월일',
      placeholder: '- 없이 입력해주세요            ex) 19990123',
      key: 'birthDate',
    },
    {label: '주소', placeholder: '주소', key: 'address'},
    {
      label: '핸드폰 번호',
      placeholder: '- 없이 입력해주세요',
      key: 'phone',
    },
  ];

  const validatePerson = (person: Person) => {
    return (
      person.name.trim() !== '' &&
      person.gender.trim() !== '' &&
      person.birthDate.trim() !== '' &&
      person.address.trim() !== '' &&
      person.phone.trim() !== ''
    );
  };

  const handleSave = () => {
    if (validatePerson(currentPerson)) {
      handleAddPersonToList();
      Alert.alert('저장 완료', '리스트에 저장되었습니다.');
    } else {
      Alert.alert('저장 실패', '모든 필수 정보를 입력해주세요.');
    }
  };

  const handleFinalSave = async () => {
    if (people.length > 0) {
      try {
        Alert.alert(
          '최종 저장 완료',
          '모든 정보가 서버에 저장되었습니다.',
          [
            {
              text: '확인',
              onPress: () => navigation.navigate('Main'),
            },
          ],
          {cancelable: false},
        );
      } catch (error) {
        Alert.alert(
          '저장 실패',
          '서버에 데이터를 저장하는 중 오류가 발생했습니다.',
        );
      }
    } else {
      Alert.alert('저장 실패', '저장된 사람이 없습니다.');
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
                  setCurrentPerson({...currentPerson, name: text})
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
                <TouchableOpacity
                  style={[
                    enrollStyle.genderButton,
                    currentPerson.gender === 'MALE' &&
                      enrollStyle.selectedGender,
                  ]}
                  onPress={() =>
                    setCurrentPerson({...currentPerson, gender: 'MALE'})
                  }>
                  <CustomText style={{fontWeight: '600'}}>남</CustomText>
                </TouchableOpacity>
                <TouchableOpacity
                  style={[
                    enrollStyle.genderButton,
                    currentPerson.gender === 'FEMALE' &&
                      enrollStyle.selectedGender,
                  ]}
                  onPress={() =>
                    setCurrentPerson({...currentPerson, gender: 'FEMALE'})
                  }>
                  <CustomText style={{fontWeight: '600'}}>녀</CustomText>
                </TouchableOpacity>
              </View>
            </View>
          </View>

          {fields.map((field, fieldIndex) => (
            <View key={fieldIndex} style={enrollStyle.fieldContainer}>
              <CustomText style={enrollStyle.subtitle}>
                {field.label}
              </CustomText>
              <CustomTextInput
                placeholder={field.placeholder}
                style={[defaultStyle.input, {marginBottom: 10}]}
                value={currentPerson[field.key]}
                onChangeText={text => {
                  if (field.key === 'birthDate') {
                    setCurrentPerson({
                      ...currentPerson,
                      birthDate: formatBirthDate(text),
                    });
                  } else if (field.key === 'phone') {
                    setCurrentPerson({
                      ...currentPerson,
                      phone: formatPhoneNumber(text),
                    });
                  } else {
                    setCurrentPerson({...currentPerson, [field.key]: text});
                  }
                }}
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
                  {index + 1}. {person.name} {person.birthDate}
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
    </View>
  );
};

export default EnrollScreen;
