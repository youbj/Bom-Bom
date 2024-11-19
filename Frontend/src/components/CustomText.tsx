import React from 'react';
import {Text as RNText, TextProps, TextStyle} from 'react-native';
import {getFontFamily, flattenStyle} from '../utils/FontUtils';

interface CustomTextProps extends TextProps {
  style?: TextStyle | TextStyle[]; // 배열 형태도 허용
}

const CustomText: React.FC<CustomTextProps> = ({style, ...props}) => {
  // 스타일을 항상 배열로 처리
  const flattenedStyles = Array.isArray(style) ? style : [style];
  const flattenedStyle = flattenStyle(flattenedStyles);

  const fontWeight = flattenedStyle.fontWeight ?? '400';
  const fontFamily = getFontFamily(fontWeight);

  const customStyle = [
    flattenedStyle,
    {fontFamily}, // 폰트 스타일 추가
  ];

  return <RNText style={customStyle} {...props} />;
};

export default CustomText;
