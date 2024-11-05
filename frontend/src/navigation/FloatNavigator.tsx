// src/navigation/FloatNavigator.tsx
import React from 'react';
import { createNativeStackNavigator } from '@react-navigation/native-stack';
import MessageScreen from '../screens/Message/MessageScreen';
import { FloatNavigatorParamList } from '../../types/navigation.d';

const Stack = createNativeStackNavigator<FloatNavigatorParamList>();

const FloatNavigator: React.FC = () => (
  <Stack.Navigator>
    <Stack.Screen name="MessageScreen" component={MessageScreen} options={{ headerShown:false }} />
  </Stack.Navigator>
);

export default FloatNavigator;
