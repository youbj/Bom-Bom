import React from 'react';
import {Text as RNText, TextProps, StyleSheet, TextStyle} from 'react-native';
import { getFontFamily, flattenStyle } from '../utils/FontUtils';

interface CustomTextProps extends TextProps {
  style?: TextStyle;
}

const CustomText: React.FC<CustomTextProps> = ({style, ...props}) => {
  const flattenedStyle = flattenStyle(style);
  const fontFamily = getFontFamily(flattenedStyle.fontWeight);

  const customStyle = [    
    flattenedStyle,
    { fontFamily },
  ];

  return <RNText style={customStyle} {...props} />;
};

export default CustomText;
