import 'react-native-reanimated';
import React, {useEffect} from 'react';
import {Alert, Platform, PermissionsAndroid} from 'react-native';
import messaging from '@react-native-firebase/messaging';
import {NavigationContainer} from '@react-navigation/native';
import AuthNavigator from './src/navigation/AuthNavigator';
import MainNavigator from './src/navigation/MainNavigator';
import useAuthStore from './src/stores/useAuthStore';

const App = (): JSX.Element => {
  const {isLoggedIn} = useAuthStore();

  // 알림 권한 요청 함수
  const requestNotificationPermission = async () => {
    if (Platform.OS === 'android' && Platform.Version >= 33) {
      const granted = await PermissionsAndroid.request(
        PermissionsAndroid.PERMISSIONS.POST_NOTIFICATIONS,
      );
      return granted === PermissionsAndroid.RESULTS.GRANTED;
    }
    return true;
  };

  useEffect(() => {
    // 알림 권한 요청
    requestNotificationPermission();

    // 포그라운드에서 메시지 수신 설정
    const unsubscribeForeground = messaging().onMessage(async remoteMessage => {
      Alert.alert('알림 도착', remoteMessage.notification?.title);
    });

    return () => {
      unsubscribeForeground();
    };
  }, []);

  return (
    <NavigationContainer>
      {isLoggedIn ? <MainNavigator /> : <AuthNavigator />}
    </NavigationContainer>
  );
};

export default App;
