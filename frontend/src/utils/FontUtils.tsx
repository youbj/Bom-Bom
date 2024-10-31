import { StyleSheet, TextStyle } from 'react-native';

export const getFontFamily = (fontWeight: TextStyle['fontWeight']) => {
  switch (fontWeight) {
    case '100': return 'Paperlogy-1Thin';
    case '200': return 'Paperlogy-2ExtraLight';
    case '300': return 'Paperlogy-3Light';
    case '400': return 'Paperlogy-4Regular';
    case '500': return 'Paperlogy-5Medium';
    case '600': return 'Paperlogy-6SemiBold';
    case '700': return 'Paperlogy-7Bold';
    case '800': return 'Paperlogy-8ExtraBold';
    case '900': return 'Paperlogy-9Black';
    default: return 'Paperlogy-4Regular';
  }
};

export const flattenStyle = (style: any): TextStyle => {
  return StyleSheet.flatten(style) as TextStyle;
};
