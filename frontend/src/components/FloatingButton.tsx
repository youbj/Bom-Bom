// src/components/FloatingButton.tsx
import React, { useState } from 'react';
import { View, Text, TouchableOpacity, StyleSheet, Animated, Dimensions } from 'react-native';
import { useNavigation } from '@react-navigation/native';
import EncryptedStorage from 'react-native-encrypted-storage';
import { MainNavigatorProp } from '../../types/navigation.d'

const { width, height } = Dimensions.get('window');

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
    let userType = 'socialWorker';
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
    <View style={styles.container}>
      {/* Secondary Buttons */}
      {isOpen && (
        <>
          <Animated.View style={[styles.secondaryButton, buttonStyle(-70)]}>
            <TouchableOpacity style={styles.button} onPress={handlePress('Home')}>
              <Text style={styles.label}>Home</Text>
            </TouchableOpacity>
          </Animated.View>

          <Animated.View style={[styles.secondaryButton, buttonStyle(-140)]}>
            <TouchableOpacity style={styles.button} onPress={handlePressMessage}>
              <Text style={styles.label}>Message</Text>
            </TouchableOpacity>
          </Animated.View>

          <Animated.View style={[styles.secondaryButton, buttonStyle(-210)]}>
            <TouchableOpacity style={styles.button} onPress={handlePressVerify}>
              <Text style={styles.label}>Verify</Text>
            </TouchableOpacity>
          </Animated.View>
        </>
      )}

      {/* Main Floating Button */}
      <TouchableOpacity onPress={toggleMenu} style={styles.fab}>
      <Text style={styles.fabText}>{isOpen ? 'X' : '+'}</Text>
      </TouchableOpacity>
    </View>
  );
};

export default FloatingButton;

const styles = StyleSheet.create({
  container: {
    position: 'absolute',
    right: '5%',
    bottom: '5%',
    alignItems: 'center',
    zIndex: 1000, // Ensure FloatingButton is above other elements
  },
  fab: {
    backgroundColor: '#6200ee',
    width: width * 0.15,
    height: width * 0.15,
    borderRadius: (width * 0.15) / 2,
    alignItems: 'center',
    justifyContent: 'center',
    elevation: 8,
    zIndex: 1001, // Floating button above overlay
  },
  fabText: {
    color: 'white',
    fontSize: width * 0.08,
    fontWeight: 'bold',
  },
  secondaryButton: {
    position: 'absolute',
    right: (width * 0.15 - width * 0.125) / 2,
    bottom: height * 0.03,
    zIndex: 1001,
  },
  button: {
    backgroundColor: '#6200ee',
    width: width * 0.125,
    height: width * 0.125,
    borderRadius: (width * 0.125) / 2,
    alignItems: 'center',
    justifyContent: 'center',
  },
  label: {
    color: 'white',
    fontSize: width * 0.03,
  },
});
