// App.tsx
import React, {useEffect, useState} from 'react';
import {NavigationContainer} from '@react-navigation/native';
import AuthNavigator from './src/navigation/AuthNavigator';
import MainNavigator from './src/navigation/MainNavigator';
import FloatingButton from './src/components/FloatingButton';
import Overlay from './src/components/Overlay';
import EncryptedStorage from 'react-native-encrypted-storage';
import SplashScreen from './src/screens/Auth/SplashScreen';
import useAuthStore from './src/stores/useAuthStore'; // Zustand store import

const App = (): JSX.Element => {
  const {isLoggedIn, setIsLoggedIn} = useAuthStore(); // useAuthStore 사용
  const [isLoading, setIsLoading] = useState(true);
  const [isOverlayVisible, setOverlayVisible] = useState(false);
  const [userType, setUserType] = useState<string | null>(null); // User type: 'family' or 'socialWorker'

  useEffect(() => {
    const fetchUserType = async () => {
      const session = await EncryptedStorage.getItem('user_session');
      const sessionData = session ? JSON.parse(session) : null;
      const type = sessionData?.type;
      setUserType(type);
    };
    if (isLoggedIn) {
      fetchUserType();
    }
  }, [isLoggedIn]);

  const toggleOverlay = () => {
    setOverlayVisible(!isOverlayVisible);
  };

  return (
    <NavigationContainer>
      {isLoggedIn ? (
        <>
          <MainNavigator userType={userType} setIsLoggedIn={setIsLoggedIn} />
          {/* 오버레이 */}
          {isOverlayVisible && <Overlay onClose={toggleOverlay} />}
          {/* 플로팅 버튼 */}
          <FloatingButton toggleOverlay={toggleOverlay} />
        </>
      ) : (
        <AuthNavigator setIsLoggedIn={setIsLoggedIn} />
      )}
    </NavigationContainer>
  );
};

export default App;
