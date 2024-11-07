import React from 'react';
import {createNativeStackNavigator} from '@react-navigation/native-stack';
import MainScreen from '../screens/MainScreen';
import FloatNavigator from './FloatNavigator';
import {MainNavigatorParamList} from '../../types/navigation.d';
import EnrollScreen from '../screens/EnrollScreen';

interface MainNavigatorProps {
  userType: string | null;
  setIsLoggedIn: React.Dispatch<React.SetStateAction<boolean>>;
}

const Stack = createNativeStackNavigator<MainNavigatorParamList>();

const MainNavigator = ({
  userType,
  setIsLoggedIn,
}: MainNavigatorProps): JSX.Element => {
  return (
    <Stack.Navigator>
      <Stack.Screen
        name="Main"
        children={() => (
          <MainScreen userType={userType} setIsLoggedIn={setIsLoggedIn} />
        )} // userType 추가 전달
        options={{headerShown: false}}
      />
      <Stack.Screen
        name="FloatNavigator"
        children={() => <FloatNavigator userType={userType} />}
        options={{headerShown: false}}
      />
      <Stack.Screen
        name="Enroll"
        component={EnrollScreen}
        options={{headerShown: false}}
      />
    </Stack.Navigator>
  );
};

export default MainNavigator;
