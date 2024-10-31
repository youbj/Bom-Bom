import React from 'react';
import {createNativeStackNavigator} from '@react-navigation/native-stack';
import SplashScreen from '../screens/SplashScreen';
import LoginScreen from '../screens/LoginScreen';
import JoinScreen from '../screens/JoinScreen';
import JoinDetailScreen from '../screens/JoinDetailScreen';

const Stack = createNativeStackNavigator();

const MainNavigator = () => {
  return (
    <Stack.Navigator initialRouteName="Main">
      <Stack.Screen
        name="Main"
        component={SplashScreen}
        options={{headerShown: false}}
      />
      <Stack.Screen
        name="Login"
        component={LoginScreen}
        options={{headerShown: false}}
      />
      <Stack.Screen name="Join" component={JoinScreen} options={{headerShown: false}}/>
      <Stack.Screen name="JoinDetail" component={JoinDetailScreen} options={{headerShown: false}}/>
    </Stack.Navigator>
  );
};

export default MainNavigator;
