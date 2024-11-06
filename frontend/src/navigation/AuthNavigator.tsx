import React from 'react';
import { createNativeStackNavigator } from '@react-navigation/native-stack';
import SplashScreen from '../screens/Auth/SplashScreen';
import LoginScreen from '../screens/Auth/LoginScreen';
import JoinScreen from '../screens/Auth/JoinScreen';
import JoinDetailScreen from '../screens/Auth/JoinDetailScreen';
import { AuthNavigatorProps } from '../../types/navigation.d';

const Stack = createNativeStackNavigator();

const AuthNavigator = ({ setIsLoggedIn }: AuthNavigatorProps) => {
  return (
    <Stack.Navigator initialRouteName="Splash">
      <Stack.Screen
        name="Splash"
        options={{ headerShown: false }}
      >
        {props => <SplashScreen {...props} setIsLoggedIn={setIsLoggedIn} />}
      </Stack.Screen>
      <Stack.Screen
        name="Login"
        options={{ headerShown: false }}
      >
        {props => <LoginScreen {...props} setIsLoggedIn={setIsLoggedIn} />}
      </Stack.Screen>
      <Stack.Screen
        name="Join"
        component={JoinScreen}
        options={{ headerShown: false }}
      />
      <Stack.Screen
        name="JoinDetail"
        component={JoinDetailScreen}
        options={{ headerShown: false }}
      />
    </Stack.Navigator>
  );
};

export default AuthNavigator;
