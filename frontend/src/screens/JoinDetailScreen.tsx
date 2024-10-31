import React from 'react'
import { View } from 'react-native';
import { useRoute } from '@react-navigation/native';
import { JoinDetailRouteProp } from '../../types/navigation.d';

import CustomText from '../components/CustomText';

const JoinDetailScreen = (): JSX.Element => {
  const route = useRoute<JoinDetailRouteProp>();
  const { isType } = route.params;
  
  return (
    <View>
      <CustomText>Hi!</CustomText>
    </View>
  )
}

export default JoinDetailScreen;