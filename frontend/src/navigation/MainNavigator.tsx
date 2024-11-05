import React from 'react';
import {createNativeStackNavigator} from '@react-navigation/native-stack';
import MainScreen from '../screens/MainScreen';
import EnrollScreen from '../screens/EnrollScreen';


const Stack = createNativeStackNavigator();

const MainNavigator = () => {
  
  return (
    <Stack.Navigator initialRouteName="Main">
      <Stack.Screen name="Main" component={MainScreen} options={{headerShown: false}}></Stack.Screen>
      <Stack.Screen name="Enroll" component={EnrollScreen} options={{headerShown: false}}></Stack.Screen>
    </Stack.Navigator>
  );
};

export default MainNavigator;
