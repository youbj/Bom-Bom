import React from 'react';
import {
  TextInput as RNTextInput,
  TextInputProps,
  View,
  TextStyle,
} from 'react-native';
import { getFontFamily, flattenStyle } from '../utils/FontUtils';

interface CustomTextInputProps extends TextInputProps {
  right?: JSX.Element;
}

const CustomTextInput: React.FC<CustomTextInputProps> = ({
  style,
  right,
  ...props
}) => {
  const flattenedStyle = flattenStyle(style || {}) as TextStyle; 
  const fontWeight = flattenedStyle.fontWeight || '400';
  const customStyle = [
    { fontFamily: getFontFamily(fontWeight) },
    flattenedStyle,
  ];

  return (
    <View style={{ flexDirection: 'row', alignItems: 'center' }}>
      <RNTextInput
        style={[customStyle, { flex: 1, paddingRight: 30 }]}
        {...props}
      />
      <View style={{ position: 'absolute', top: 10, right: 15 }}>{right}</View>
    </View>
  );
};

export default CustomTextInput;
