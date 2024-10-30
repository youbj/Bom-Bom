import React from 'react';
import {Text as RNText, TextProps, TextStyle} from 'react-native';
import { getFontFamily, flattenStyle } from '../utils/FontUtils';

interface CustomTextProps extends TextProps {
  style?: TextStyle;
}

const CustomText: React.FC<CustomTextProps> = ({style, ...props}) => {
  const flattenedStyle = flattenStyle(style || {});
  const fontWeight = flattenedStyle.fontWeight ?? '400';
  const fontFamily = getFontFamily(fontWeight);

  const customStyle = [    
    flattenedStyle,
    { fontFamily },
  ];

  return <RNText style={customStyle} {...props} />;
};

export default CustomText;
