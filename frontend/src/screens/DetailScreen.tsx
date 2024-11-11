import React from 'react';
import { View } from 'react-native';
import CustomText from '../components/CustomText';
import { RouteProp, useRoute } from '@react-navigation/native';
import { MainStackParamList } from '../../types/navigation.d';

type DetailScreenRouteProp = RouteProp<MainStackParamList, 'Detail'>;

const DetailScreen = () => {
  const route = useRoute<DetailScreenRouteProp>();
  const { seniorId } = route.params;

  return (
    <View>
      <CustomText>Senior ID: {seniorId}</CustomText>
      <CustomText>Hello world!</CustomText>
    </View>
  );
};

export default DetailScreen;
