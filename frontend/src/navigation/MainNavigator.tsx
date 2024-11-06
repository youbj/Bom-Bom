import React from 'react';
import {createNativeStackNavigator, NativeStackNavigationProp} from '@react-navigation/native-stack';
import MainScreen from '../screens/MainScreen';
import FloatNavigator from './FloatNavigator';
import { MainNavigatorParamList } from '../../types/navigation.d';
import EnrollScreen from '../screens/EnrollScreen';

interface MainNavigatorProps {
  userType: string | null;
}

const Stack = createNativeStackNavigator<MainNavigatorParamList>();

const MainNavigator: React.FC<MainNavigatorProps> = ({ userType }) => {
  
  return (
    <Stack.Navigator>
      <Stack.Screen name="Main" component={MainScreen} options={{headerShown: false}}></Stack.Screen>
      <Stack.Screen
        name="FloatNavigator"
        children={() => <FloatNavigator userType={userType} />}
        options={{ headerShown: false }}
      />
      <Stack.Screen name="Enroll" component={EnrollScreen} options={{headerShown: false}}></Stack.Screen>
    </Stack.Navigator>
  );
};

export default MainNavigator;
