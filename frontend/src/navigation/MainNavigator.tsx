import React from 'react';
import {createNativeStackNavigator} from '@react-navigation/native-stack';
import MainScreen from '../screens/MainScreen';
import DetailScreen from '../screens/DetailScreen';
import FloatNavigator from './FloatNavigator';
import {MainNavigatorParamList} from '../../types/navigation.d';
import EnrollScreen from '../screens/EnrollScreen';

interface MainNavigatorProps {
  userType: string | null;
  setIsLoggedIn: (loggedIn: boolean) => void;
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
          <MainScreen />
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
        children={() => <EnrollScreen />}
        options={{headerShown: false}}
      />
      <Stack.Screen
        name="Detail"
        component={DetailScreen}
        options={{headerShown: false}}
      />
    </Stack.Navigator>
  );
};

export default MainNavigator;
