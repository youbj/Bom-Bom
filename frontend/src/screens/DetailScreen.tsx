import React, {useCallback, useEffect, useState} from 'react';
import {View, Image, TouchableOpacity, StyleSheet} from 'react-native';
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
  DetailToPlanNavigationProp,
  MainStackParamList,
  DetailToFeelingNavigationProp,
} from '../../types/navigation.d';
import EncryptedStorage from 'react-native-encrypted-storage';
import DonutChart from '../components/DonutChart';
import Icon from 'react-native-vector-icons/MaterialCommunityIcons';
import CustomAlert from '../components/CustomAlert';

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
  todayEmotion: number;
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
    todayEmotion: 0,
  });

  const [type, setType] = useState<string>('');
  const [imageUri, setImageUri] = useState<string | null>(null);

  const [alertState, setAlertState] = useState({
    visible: false,
    title: '',
    message: '',
  });

  const route = useRoute<DetailScreenRouteProp>();
  const {seniorId} = route.params;
  const reviseNavigation = useNavigation<DetailToReviseNavigationProp>();
  const planNavigation = useNavigation<DetailToPlanNavigationProp>();
  const feelingNavigation = useNavigation<DetailToFeelingNavigationProp>();

  const showAlert = (title: string, message: string) => {
    setAlertState({visible: true, title, message});
  };

  const fetchType = async () => {
    try {
      const session = await EncryptedStorage.getItem('user_session');
      setType(session ? JSON.parse(session).type : '');
    } catch (error) {
      console.error('type 가져오기 오류:', error);
    }
  };

  const fetchDetailList = async () => {
    try {
      const response = await instance.get(`/seniors/detail`, {
        params: {'senior-id': seniorId},
      });
      setDetail(response.data);
      setImageUri(response.data.profileImgUrl);
    } catch (error) {
      showAlert('오류', '어르신 정보 불러오기에 실패했습니다.');
      console.error('Detail fetch error:', error);
    }
  };

  const showImagePicker = () => {
    launchImageLibrary({mediaType: 'photo'}, res => {
      if (res.assets?.[0]?.uri) {
        setImageUri(res.assets[0].uri);
        showAlert('이미지', '이미지 선택이 완료되었습니다.');
      } else {
        showAlert('이미지', '이미지 선택이 취소되었습니다.');
      }
    });
  };

  const saveImage = async () => {
    if (!imageUri) return;

    const formdata = new FormData();
    formdata.append('profileImg', {
      uri: imageUri,
      name: 'profile.jpg',
      type: 'image/jpeg',
    });
    formdata.append('senior-id', JSON.stringify(seniorId));

    try {
      await instance.post(`/seniors/profile`, formdata, {
        headers: {'Content-Type': 'multipart/form-data'},
      });
      showAlert('성공', '이미지가 성공적으로 저장되었습니다.');
    } catch (error) {
      showAlert('오류', '이미지 저장에 실패했습니다.');
      console.error('Image save error:', error);
    }
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

      <View style={{flex: 3, alignItems: 'center'}}>
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
            onPress={imageUri ? saveImage : showImagePicker}
            style={detailStyle.button}>
            <CustomText style={{fontWeight: '600'}}>
              {imageUri ? '저장' : '이미지 업로드'}
            </CustomText>
          </TouchableOpacity>
        ) : (
          <Icon
            name="heart"
            color="red"
            size={40}
            style={{marginVertical: 20}}
          />
        )}

        <View
          style={{
            flexDirection: 'row',
            justifyContent: 'space-between',
            alignItems: 'center',
          }}>
          <CustomText style={detailStyle.title}>{detail.name}</CustomText>
          <TouchableOpacity
            onPress={() => reviseNavigation.navigate('Revise', {detail})}>
            <Icon name="eraser" color="black" size={30} />
          </TouchableOpacity>
        </View>
        <CustomText>{`${detail.age}세 / ${
          detail.gender === 'MALE' ? '남' : '여'
        }`}</CustomText>
      </View>

      <View style={{flex: 2, position: 'relative'}}>
        <View style={detailStyle.bottomContainer}>
          <View style={detailStyle.subContainer}>
            <DonutChart progress={detail.todayEmotion} />
            <CustomText style={detailStyle.graphTitle}>
              오늘의 행복지수
            </CustomText>
            <TouchableOpacity
              onPress={() =>
                feelingNavigation.navigate('FeelingDetail', {seniorId})
              }>
              <CustomText
                style={[
                  detailStyle.graphTitle,
                  {color: '#FF6F61', marginTop: 5},
                ]}>
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
                <CustomText
                  key={
                    index
                  }>{`${member.memberName} ${member.memberPhoneNumber}`}</CustomText>
              ))}
            </View>
          </View>

          <TouchableOpacity
            onPress={() => planNavigation.navigate('Plan', {seniorId})}
            style={{position: 'absolute', top: 10, right: 10}}>
            <Icon name="calendar" size={30} color="#000" />
          </TouchableOpacity>
        </View>
      </View>

      <CustomAlert
        visible={alertState.visible}
        title={alertState.title}
        message={alertState.message}
        onClose={() => setAlertState({...alertState, visible: false})}
      />
    </View>
  );
};

export default DetailScreen;
