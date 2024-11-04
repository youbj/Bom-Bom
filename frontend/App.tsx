// App.tsx
import React, { useState } from 'react';
import { NavigationContainer } from '@react-navigation/native';
import AuthNavigator from './src/navigation/AuthNavigator';
import MainNavigator from './src/navigation/MainNavigator';
import FloatingButton from './src/components/FloatingButton';
import Overlay from './src/components/Overlay';

const App = (): JSX.Element => {
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [isOverlayVisible, setOverlayVisible] = useState(false);

  const toggleOverlay = () => {
    setOverlayVisible(!isOverlayVisible);
  };

  return (
    <NavigationContainer>
      {isLoggedIn ? (
        <>
          <MainNavigator />
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
