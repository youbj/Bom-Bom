import React from 'react';
import { View, Text, StyleSheet, Image } from 'react-native';

const MainScreen = () => {
  return (
    <View style={styles.container}>
      <Image source={require('../../assets/logo.png')} style={styles.logo} />

      <View style={styles.spacing} />

      <Text style={styles.text}>봄 : 봄</Text>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
  },
  logo: {
    width: 128,
    height: 128,
  },
  text: {
    fontSize: 32,
    fontWeight: 'bold',
  },
  spacing: {
   height: 20, 
  }
});

export default MainScreen;
