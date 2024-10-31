import React from 'react';
import { createNativeStackNavigator } from '@react-navigation/native-stack';
import SplashScreen from '../screens/SplashScreen';
import LoginScreen from '../screens/LoginScreen';
import JoinScreen from '../screens/JoinScreen';
import JoinDetailScreen from '../screens/JoinDetailScreen';

const Stack = createNativeStackNavigator();

type AuthNavigatorProps = {
  setIsLoggedIn: (loggedIn: boolean) => void;
};

const AuthNavigator = ({ setIsLoggedIn }: AuthNavigatorProps) => {
  return (
    <Stack.Navigator initialRouteName="Splash">
      <Stack.Screen
        name="Splash"
        component={SplashScreen}
        options={{ headerShown: false }}
      />
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
