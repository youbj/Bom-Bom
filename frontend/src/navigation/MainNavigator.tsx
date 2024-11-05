import React from 'react';
import {createNativeStackNavigator, NativeStackNavigationProp} from '@react-navigation/native-stack';
import MainScreen from '../screens/MainScreen';
import FloatNavigator from './FloatNavigator';
import { MainNavigatorParamList } from '../../types/navigation.d';
import EnrollScreen from '../screens/EnrollScreen';

const Stack = createNativeStackNavigator<MainNavigatorParamList>();

const MainNavigator = () => {
  
  return (
    <Stack.Navigator>
      <Stack.Screen name="Main" component={MainScreen} options={{headerShown: false}}></Stack.Screen>
      <Stack.Screen name="FloatNavigator" component={FloatNavigator} options={{ headerShown: false }} />
      <Stack.Screen name="Enroll" component={EnrollScreen} options={{headerShown: false}}></Stack.Screen>
    </Stack.Navigator>
  );
};

export default MainNavigator;
