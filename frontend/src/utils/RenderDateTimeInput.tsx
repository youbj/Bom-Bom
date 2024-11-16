import React from 'react';
import {View, StyleSheet} from 'react-native';
import CustomText from '../components/CustomText';
import CustomTextInput from '../components/CustomTextInput';
import defaultStyle from '../styles/DefaultStyle';
import {formatBirth, formatTime} from './Format';
import PlanEnrollStyle from '../styles/PlanEnrollStyle';

export const renderDateTimeInput = (
  label: string,
  dateValue: string,
  setDate: (text: string) => void,
  timeValue: string,
  setTime: (text: string) => void,
  styles?: {
    containerStyle?: object;
    labelStyle?: object;
    inputStyle?: object;
  },
) => (
  <>
    <CustomText
      style={StyleSheet.flatten([
        PlanEnrollStyle.subTitle,
        styles?.labelStyle,
      ])}>
      {label}
    </CustomText>
    <View
      style={[
        {
          flexDirection: 'row',
          justifyContent: 'space-between',
          width: '100%',
          marginBottom: 15,
        },
        styles?.containerStyle,
      ]}>
      <View style={{width: '48%'}}>
        <CustomTextInput
          placeholder="YYYY-MM-DD"
          value={dateValue}
          onChangeText={text => setDate(formatBirth(text))}
          style={[defaultStyle.input, styles?.inputStyle]}
        />
      </View>
      <View style={{width: '48%'}}>
        <CustomTextInput
          placeholder="HH:MM"
          value={timeValue}
          onChangeText={text => setTime(formatTime(text))}
          style={[defaultStyle.input, styles?.inputStyle]}
        />
      </View>
    </View>
  </>
);
