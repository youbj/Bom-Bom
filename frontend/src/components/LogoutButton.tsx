import React from 'react';
import {TouchableOpacity, StyleSheet} from 'react-native';
import useAuthStore from '../stores/useAuthStore';
import Icon from 'react-native-vector-icons/MaterialCommunityIcons';
import EncryptedStorage from 'react-native-encrypted-storage';
import CookieManager from '@react-native-cookies/cookies';

const LogoutButton = (): JSX.Element => {
  const setIsLoggedIn = useAuthStore(state => state.setIsLoggedIn);

  const handleLogout = async () => {
    try {
      await EncryptedStorage.removeItem('user_session');

      await CookieManager.clearAll();

      setIsLoggedIn(false);
    } catch (error) {
      console.error('로그아웃 실패:', error);
    }
  };

  return (
    <TouchableOpacity onPress={handleLogout} style={styles.button}>
      <Icon name="logout" style={styles.iconStyle} />
    </TouchableOpacity>
  );
};

const styles = StyleSheet.create({
  button: {
    position: 'absolute',
    top: 10,
    right: 10,
    padding: 10,
  },

  iconStyle: {
    color: '#000000',
    fontSize: 30,
  },
});

export default LogoutButton;
