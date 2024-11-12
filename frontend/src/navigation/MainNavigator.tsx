import React, { useEffect, useState, createContext, useContext } from 'react';
import { createNativeStackNavigator } from '@react-navigation/native-stack';
import { useNavigationState } from '@react-navigation/native';
import EncryptedStorage from 'react-native-encrypted-storage';
import MainScreen from '../screens/MainScreen';
import DetailScreen from '../screens/DetailScreen';
import FloatNavigator from './FloatNavigator';
import EnrollScreen from '../screens/EnrollScreen';
import FloatingButton from '../components/FloatingButton';
import Overlay from '../components/Overlay';

const UserTypeContext = createContext<string | null>(null);
export const useUserType = () => useContext(UserTypeContext);

const Stack = createNativeStackNavigator();

const MainNavigator = (): JSX.Element => {
  const [userType, setUserType] = useState<string | null>(null);
  const [isFloatingButtonOpen, setFloatingButtonOpen] = useState(false);

  const isDetailScreen = useNavigationState(state => 
    state?.routes?.some(route => route.name === 'Detail') ?? false
  );

  useEffect(() => {
    const fetchUserType = async () => {
      const session = await EncryptedStorage.getItem('user_session');
      const sessionData = session ? JSON.parse(session) : null;
      setUserType(sessionData?.type || null);
    };

    fetchUserType();
  }, []);

  const toggleFloatingButton = () => {
    setFloatingButtonOpen(prev => !prev); // 버튼 열림/닫힘 상태를 토글
  };

  return (
    <UserTypeContext.Provider value={userType}>
      <Stack.Navigator>
        <Stack.Screen
          name="Main"
          component={MainScreen}
          options={{ headerShown: false }}
        />
        <Stack.Screen
          name="FloatNavigator"
          options={{ headerShown: false }}
        >
          {() => <FloatNavigator userType={userType} />}
        </Stack.Screen>
        <Stack.Screen
          name="Enroll"
          component={EnrollScreen}
          options={{ headerShown: false }}
        />
        <Stack.Screen
          name="Detail"
          component={DetailScreen}
          options={{ headerShown: false }}
        />
      </Stack.Navigator>

      {/* Overlay와 FloatingButton이 동일한 상태로 제어됨 */}
      {isFloatingButtonOpen && <Overlay onClose={toggleFloatingButton} />}
      <FloatingButton
        toggleOverlay={toggleFloatingButton} // 버튼이 클릭되면 열림/닫힘 토글
        isDetailScreen={isDetailScreen}
        isOpen={isFloatingButtonOpen}
        setIsOpen={setFloatingButtonOpen}
      />
    </UserTypeContext.Provider>
  );
};

export default MainNavigator;
