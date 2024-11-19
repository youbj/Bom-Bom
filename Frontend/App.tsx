import React, {useEffect, useState} from 'react';
import messaging from '@react-native-firebase/messaging';
import {NavigationContainer} from '@react-navigation/native';
import {createNavigationContainerRef} from '@react-navigation/native';
import AuthNavigator from './src/navigation/AuthNavigator';
import MainNavigator from './src/navigation/MainNavigator';
import useAuthStore from './src/stores/useAuthStore';
import {MainStackParamList} from './types/navigation.d';
import CustomAlert from './src/components/CustomAlert';

export const navigationRef = createNavigationContainerRef<MainStackParamList>();

const App = (): JSX.Element => {
  const {isLoggedIn} = useAuthStore();

  // CustomAlert 상태 관리
  const [alertState, setAlertState] = useState({
    visible: false,
    title: '',
    message: '',
  });

  const showAlert = (title: string, message: string) => {
    setAlertState({visible: true, title, message});
  };

  const handleNavigation = (
    screen: keyof MainStackParamList,
    seniorId?: string,
  ) => {
    const screenMap: Record<keyof MainStackParamList, () => void> = {
      Main: () => navigationRef.navigate('Main'),
      Detail: () =>
        seniorId
          ? navigationRef.navigate('Detail', {seniorId: Number(seniorId)})
          : undefined,
      Plan: () =>
        seniorId
          ? navigationRef.navigate('Plan', {seniorId: Number(seniorId)})
          : undefined,
      FeelingDetail: () =>
        seniorId
          ? navigationRef.navigate('FeelingDetail', {
              seniorId: Number(seniorId),
            })
          : undefined,
      FloatNavigator: () => {}, // 추가된 키 기본값 처리
      Enroll: () => {},
      Revise: () => {},
      PlanEnroll: () => {},
    };

    screenMap[screen]?.();
  };

  useEffect(() => {
    console.log('자동 로그인 확인 과정:', isLoggedIn);

    const processNotification = async () => {
      if (!navigationRef.isReady() || !isLoggedIn) {
        console.log('네비게이션 준비 중 또는 로그인이 필요합니다.');
        return;
      }

      const initialNotification = await messaging().getInitialNotification();
      if (initialNotification?.data?.screen) {
        const {screen, 'senior-id': seniorId} = initialNotification.data;

        if (typeof seniorId === 'string') {
          handleNavigation(screen as keyof MainStackParamList, seniorId);
        } else {
          console.warn('Invalid seniorId type:', typeof seniorId, seniorId);
        }
      }
    };

    const unsubscribeForeground = messaging().onMessage(async remoteMessage => {
      showAlert(
        remoteMessage.notification?.title ?? '알림',
        remoteMessage.notification?.body ?? '내용 없음',
      );
    });

    const unsubscribeNotificationOpened = messaging().onNotificationOpenedApp(
      remoteMessage => {
        const {screen, 'senior-id': seniorId} = remoteMessage.data || {};

        if (navigationRef.isReady() && isLoggedIn) {
          if (typeof seniorId === 'string') {
            handleNavigation(screen as keyof MainStackParamList, seniorId);
          } else {
            console.warn('Invalid seniorId type:', typeof seniorId, seniorId);
          }
        }
      },
    );

    if (isLoggedIn) {
      processNotification();
    }

    return () => {
      unsubscribeForeground();
      unsubscribeNotificationOpened();
    };
  }, [isLoggedIn]);

  return (
    <>
      <NavigationContainer ref={navigationRef}>
        {isLoggedIn ? <MainNavigator /> : <AuthNavigator />}
      </NavigationContainer>

      {/* CustomAlert 추가 */}
      <CustomAlert
        visible={alertState.visible}
        title={alertState.title}
        message={alertState.message}
        onClose={() => setAlertState({...alertState, visible: false})}
      />
    </>
  );
};

export default App;
