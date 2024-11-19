import React from 'react';
import { TouchableOpacity } from 'react-native';
import Icon from 'react-native-vector-icons/MaterialCommunityIcons';
import { useNavigation } from '@react-navigation/native';


type BackButtonProps = {
  onPress?: () => void;
  color?: string;
  size?: number;
  style?: object;
};

const BackButton = ({ onPress, color = "#000000", size = 30, style }: BackButtonProps): JSX.Element => {
  const navigation = useNavigation();

  const handlePress = () => {
    if (onPress) {
      onPress();
    } else {
      navigation.goBack();
    }
  };

  return (
    <TouchableOpacity style={[{ position: 'absolute', top: 10, left: 10, padding: 10 }, style]} onPress={handlePress}>
      <Icon name="arrow-left" color={color} size={size} />
    </TouchableOpacity>
  );
};

export default BackButton;
