import React from 'react';
import { TouchableOpacity } from 'react-native';
import Icon from 'react-native-vector-icons/MaterialCommunityIcons';
import EncryptedStorage from 'react-native-encrypted-storage';
import CookieManager from '@react-native-cookies/cookies';

type LogoutButtonProps = {
  onPress?: () => void;
  color?: string;
  size?: number;
  style?: object;
};

const LogoutButton = ({ onPress, color = "#000000", size = 30, style }: LogoutButtonProps): JSX.Element => {
  const handleLogout = async () => {
    try {
      await EncryptedStorage.removeItem('user_session');

      await CookieManager.clearAll();
      
    } catch (error) {
      console.error('로그아웃 실패:', error);
    }

    if (onPress) {
      onPress();
    }
  };

  return (
    <TouchableOpacity style={[{ position: 'absolute', top: 10, right: 10, padding: 10 }, style]} onPress={handleLogout}>
      <Icon name="logout" color={color} size={size} />
    </TouchableOpacity>
  );
};

export default LogoutButton;
