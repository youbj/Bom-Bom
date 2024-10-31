import React from 'react'
import { View, TouchableOpacity } from 'react-native'

import { useNavigation } from '@react-navigation/native';

import CustomText from '../components/CustomText'
import { MainToRecordNavigationProp } from '../../types/navigation.d';

const MainScreen = () => {
  const navigation = useNavigation<MainToRecordNavigationProp>();
  const onPress = () => {
    navigation.navigate('Record')
  }
  return (
    <View>
      <TouchableOpacity onPress={onPress}>
        <CustomText>Record</CustomText>
      </TouchableOpacity>
      <CustomText>Hi!</CustomText>
    </View>
  )
}

export default MainScreen;