import React, {useCallback, useEffect, useState} from 'react';
import {View, Alert, Image, TouchableOpacity, StyleSheet} from 'react-native';
import {launchImageLibrary} from 'react-native-image-picker';
import instance from '../api/axios';
import BackButton from '../components/BackButton';
import LogoutButton from '../components/LogoutButton';
import CustomText from '../components/CustomText';
import defaultStyle from '../styles/DefaultStyle';
import detailStyle from '../styles/DetailStyle';
import {
  RouteProp,
  useNavigation,
  useRoute,
  useFocusEffect,
} from '@react-navigation/native';
import {
  DetailToReviseNavigationProp,
  MainStackParamList,
} from '../../types/navigation.d';
import EncryptedStorage from 'react-native-encrypted-storage';
import DonutChart from '../components/DonutChart';
import Icon from 'react-native-vector-icons/MaterialCommunityIcons';

type DetailScreenRouteProp = RouteProp<MainStackParamList, 'Detail'>;

export interface DetailInfo {
  seniorId: number;
  name: string;
  address: string;
  phoneNumber: string;
  profileImgUrl: string | null;
  gender: string;
  age: number;
  birth: string;
  familyList: Array<{
    memberName: string;
    memberPhoneNumber: string;
  }>;
}

const DetailScreen = (): JSX.Element => {
  const [detail, setDetail] = useState<DetailInfo>({
    seniorId: 0,
    name: '',
    address: '',
    phoneNumber: '',
    profileImgUrl: null,
    gender: '',
    age: 0,
    birth: '',
    familyList: [],
  });
  const [type, setType] = useState<string>('');
  const [imageUri, setImageUri] = useState<string | null>(null);
  const [isImageSelected, setIsImageSelected] = useState<boolean>(false);
  const route = useRoute<DetailScreenRouteProp>();
  const {seniorId} = route.params;
  const progress = 76;
  const reviseNavigation = useNavigation<DetailToReviseNavigationProp>();

  const fetchType = async () => {
    try {
      const session = await EncryptedStorage.getItem('user_session');
      const storedType = session ? JSON.parse(session).type : '';
      setType(storedType);
    } catch (error) {
      console.error('type 가져오기 오류:', error);
    }
  };

  const fetchDetailList = async () => {
    try {
      const response = await instance.get(`/seniors/detail`, {
        params: {'senior-id': seniorId},
      });
      const data = response.data;
      if (response.status === 200) {
        setDetail(data);
        setImageUri(data.profileImgUrl);
      }
    } catch {
      Alert.alert('어르신 정보 불러오기에 실패했습니다.');
    }
  };

  const ShowPicker = () => {
    const options = {
      mediaType: 'photo' as const,
    };

    launchImageLibrary(options, res => {
      if (res.assets && res.assets[0]) {
        const uri = res.assets[0].uri ?? '';
        console.log(uri);
        Alert.alert('이미지', '선택 완료');

        // 이미지 URI를 상태에 반영
        setImageUri(uri);
        setIsImageSelected(true); // 이미지가 선택되었음을 표시
      } else {
        Alert.alert('이미지 선택이 취소되었습니다.');
      }
    });
  };

  const saveImage = async () => {
    if (!imageUri) return;

    const formdata = new FormData();

    // 이미지 파일 추가
    formdata.append('profileImg', {
      uri: imageUri,
      name: 'abc.jpg',
      type: 'image/jpeg',
    });

    // Add the senior ID as additional form data
    formdata.append('senior-id', JSON.stringify(seniorId)); // Stringify if JSON format is needed

    try {
      const uploadResponse = await instance.post(`/seniors/profile`, formdata, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });

      if (uploadResponse.status === 200) {
        Alert.alert('이미지 저장 성공');
        setIsImageSelected(false);
      }
    } catch (error) {
      Alert.alert('이미지 저장에 실패했습니다.');
      console.error(error);
    }
  };

  const onRevise = () => {
    reviseNavigation.navigate('Revise', {detail});
  };

  useFocusEffect(
    useCallback(() => {
      fetchType();
      fetchDetailList();
    }, []),
  );

  return (
    <View
      style={[
        defaultStyle.container,
        {justifyContent: 'flex-start', padding: 0},
      ]}>
      <BackButton />
      <LogoutButton />
      <View style={detailStyle.picture}>
        {imageUri && (
          <Image
            source={{uri: imageUri}}
            style={{width: '100%', height: '100%'}}
          />
        )}
      </View>
      {type === 'SOCIAL_WORKER' ? (
        <TouchableOpacity
          onPress={isImageSelected ? saveImage : ShowPicker}
          style={detailStyle.button}>
          <CustomText style={{fontWeight: '600'}}>
            {isImageSelected ? '저장' : '이미지 업로드'}
          </CustomText>
        </TouchableOpacity>
      ) : (
        <View style={{marginTop: 20, marginBottom: 5}}>
          <Icon name="heart" color="red" size={40} />
        </View>
      )}

      <View
        style={{
          flexDirection: 'row',
          justifyContent: 'space-between',
          alignItems: 'center',
        }}>
        <CustomText style={detailStyle.title}>{detail.name}</CustomText>
        <TouchableOpacity onPress={onRevise}>
          <Icon name="eraser" color="black" size={30} />
        </TouchableOpacity>
      </View>
      <CustomText>
        {detail.age}세 / {detail.gender === 'MALE' ? '남' : '여'}
      </CustomText>
      <View style={{flex: 1}}>
        <View style={detailStyle.bottomContainer}>
          <View style={detailStyle.subContainer}>
            <DonutChart progress={progress} />
            <CustomText style={detailStyle.graphTitle}>
              오늘의 행복지수
            </CustomText>
            <TouchableOpacity>
              <CustomText
                style={StyleSheet.flatten([
                  detailStyle.graphTitle,
                  {color: '#FF6F61', marginTop: 5},
                ])}>
                전체 행복지수 보기 <Icon name="heart" size={20} />
              </CustomText>
            </TouchableOpacity>
          </View>
          <View style={detailStyle.subContainer}>
            <View style={detailStyle.info}>
              <CustomText style={detailStyle.subTitle}>주소</CustomText>
              <CustomText>{detail.address}</CustomText>
            </View>
            <View style={detailStyle.info}>
              <CustomText style={detailStyle.subTitle}>핸드폰</CustomText>
              <CustomText>{detail.phoneNumber}</CustomText>
            </View>
            <View style={[detailStyle.info, {borderBottomWidth: 0}]}>
              <CustomText style={detailStyle.subTitle}>가족</CustomText>
              {detail.familyList.map((member, index) => (
                <CustomText key={index}>
                  {member.memberName} {member.memberPhoneNumber}
                </CustomText>
              ))}
            </View>
          </View>
        </View>
      </View>
    </View>
  );
};

export default DetailScreen;
