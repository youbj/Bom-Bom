// src/components/FloatingButton.tsx
import React, { useState } from 'react';
import { View, Text, TouchableOpacity, StyleSheet, Animated, Dimensions } from 'react-native';
import { useNavigation } from '@react-navigation/native';
import EncryptedStorage from 'react-native-encrypted-storage';
import { MainNavigatorProp } from '../../types/navigation.d'
import FloatingButtonStyle from '../styles/Float/FloatingButtonStyle';

interface FloatingButtonProps {
  toggleOverlay: () => void;
}

const FloatingButton: React.FC<FloatingButtonProps> = ({ toggleOverlay }) => {
  const [isOpen, setIsOpen] = useState(false);
  const animation = useState(new Animated.Value(0))[0];
  const navigation = useNavigation<MainNavigatorProp>();

  const toggleMenu = () => {
    const toValue = isOpen ? 0 : 1;

    Animated.timing(animation, {
      toValue,
      duration: 300,
      useNativeDriver: true,
    }).start();

    setIsOpen(!isOpen);
    toggleOverlay();
  };

  const buttonStyle = (position: number) => ({
    transform: [
      {
        translateY: animation.interpolate({
          inputRange: [0, 1],
          outputRange: [0, position],
        }),
      },
    ],
    opacity: animation,
  });

  const handlePressVerify = async () => {
    toggleMenu();
    // const userType = await EncryptedStorage.getItem('userType');
    let userType = 'family';
    console.log(userType);
    if (userType === 'family') {
      navigation.navigate('FloatNavigator', {
        screen: 'FamilyVerifyRequestScreen',
      });
    } else if (userType === 'socialWorker') {
      navigation.navigate('FloatNavigator', {
        screen: 'SocialWorkerApprovalScreen',
      });
    }
  };
  

  const handlePressMessage = () => {
    toggleMenu(); // 메뉴 닫기
    navigation.navigate('FloatNavigator', {screen: 'MessageScreen'});
  };

  const handlePress = (message: string) => () => {
    console.log(message);
  };

  return (
    <View style={FloatingButtonStyle.container}>
      {/* Secondary Buttons */}
      {isOpen && (
        <>
          <Animated.View style={[FloatingButtonStyle.secondaryButton, buttonStyle(-70)]}>
            <TouchableOpacity style={FloatingButtonStyle.button} onPress={handlePress('Home')}>
              <Text style={FloatingButtonStyle.label}>Home</Text>
            </TouchableOpacity>
          </Animated.View>

          <Animated.View style={[FloatingButtonStyle.secondaryButton, buttonStyle(-140)]}>
            <TouchableOpacity style={FloatingButtonStyle.button} onPress={handlePressMessage}>
              <Text style={FloatingButtonStyle.label}>Message</Text>
            </TouchableOpacity>
          </Animated.View>

          <Animated.View style={[FloatingButtonStyle.secondaryButton, buttonStyle(-210)]}>
            <TouchableOpacity style={FloatingButtonStyle.button} onPress={handlePressVerify}>
              <Text style={FloatingButtonStyle.label}>Verify</Text>
            </TouchableOpacity>
          </Animated.View>
        </>
      )}

      {/* Main Floating Button */}
      <TouchableOpacity onPress={toggleMenu} style={FloatingButtonStyle.fab}>
      <Text style={FloatingButtonStyle.fabText}>{isOpen ? 'X' : '+'}</Text>
      </TouchableOpacity>
    </View>
  );
};

export default FloatingButton;

