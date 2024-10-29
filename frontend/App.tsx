import React from 'react';
import { Text, TextProps, StyleSheet, View } from 'react-native';
import {NavigationContainer} from '@react-navigation/native';
import MainNavigator from './src/navigation/MainNavigator';

const App = (): JSX.Element => {
  return (
    <NavigationContainer>
      <MainNavigator />
    </NavigationContainer>
  );
};

export default App;
