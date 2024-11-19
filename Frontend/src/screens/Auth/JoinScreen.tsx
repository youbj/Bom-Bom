import React, {useState} from 'react';
import {View, TouchableOpacity} from 'react-native';
import CustomText from '../../components/CustomText';
import {useNavigation} from '@react-navigation/native';

import defaultStyle from '../../styles/DefaultStyle';
import joinStyle from '../../styles/Auth/JoinStyle';
import Icon from 'react-native-vector-icons/MaterialCommunityIcons';
import {JoinScreenNavigationProp} from '../../../types/navigation.d';
import BackButton from '../../components/BackButton';

const JoinScreen = (): JSX.Element => {
  const navigation = useNavigation<JoinScreenNavigationProp>();
  const [isType, setIsType] = useState('');
  const onPress = (type: 'SOCIAL_WORKER' | 'FAMILY') => {
    setIsType(type);
    navigation.navigate('JoinDetail', {isType: type});
  };

  return (
    <View style={defaultStyle.container}>
      <BackButton />
      <CustomText style={joinStyle.title}>회원 가입</CustomText>
      <View style={{height: 20}}></View>
      <CustomText style={{fontSize: 20, color: '#aaa'}}>
        어떻게 방문하셨나요?
      </CustomText>
      <View style={{height: 70}}></View>
      <View style={joinStyle.buttons}>
        <TouchableOpacity
          onPress={() => onPress('SOCIAL_WORKER')}
          style={joinStyle.button}>
          <Icon style={joinStyle.icon} name="hand-heart" />
          <View style={{height: 25}}></View>
          <CustomText style={joinStyle.buttonText}>사 회</CustomText>
          <CustomText style={joinStyle.buttonText}>복지사</CustomText>
        </TouchableOpacity>
        <TouchableOpacity
          onPress={() => onPress('FAMILY')}
          style={joinStyle.button}>
          <Icon
            style={[joinStyle.icon, {fontSize: 50}]}
            name="account-multiple"
          />
          <View style={{height: 20}}></View>
          <CustomText style={joinStyle.buttonText}>고령자</CustomText>
          <CustomText style={joinStyle.buttonText}>가 족</CustomText>
        </TouchableOpacity>
      </View>
    </View>
  );
};

export default JoinScreen;
