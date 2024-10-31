import React, {useEffect, useRef} from 'react';
import {View, Image, Animated} from 'react-native';
import {useNavigation} from '@react-navigation/native';
import {SplashScreenNavigationProp} from '../../types/navigation.d';

import defaultStyle from '../styles/DefaultStyles';
import splashStyles from '../styles/SplashStyles';
import CustomText from '../components/CustomText';

const SplashScreen = (): JSX.Element => {
  const opacity = useRef(new Animated.Value(1)).current;
  const navigation = useNavigation<SplashScreenNavigationProp>();

  useEffect(() => {
    const timeoutId = setTimeout(() => {
      Animated.timing(opacity, {
        toValue: 0,
        duration: 1000,
        useNativeDriver: true,
      }).start(() => {
        navigation.navigate('Login');
      });
    }, 1500);
    return () => clearTimeout(timeoutId);
  }, [navigation, opacity]);

  return (
    <Animated.View style={[defaultStyle.container, {opacity}]}>
      <Image
        source={require('../assets/images/logo.png')}
        style={splashStyles.logo}
      />

      <View style={splashStyles.spacing} />

      <CustomText style={splashStyles.text}>봄 : 봄</CustomText>
    </Animated.View>
  );
};

export default SplashScreen;
