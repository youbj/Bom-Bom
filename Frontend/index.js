/**
 * @format
 */

import messaging from '@react-native-firebase/messaging';
import {AppRegistry} from 'react-native';
import App from './App';
import {name as appName} from './app.json';

// 백그라운드 메시지 처리
messaging().setBackgroundMessageHandler(async remoteMessage => {
  console.log('백그라운드 메시지 처리:', remoteMessage);
});

AppRegistry.registerComponent(appName, () => App);
