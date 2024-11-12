// src/components/FloatingButton.tsx
import React, {useState} from 'react';
import {
  View,
  Text,
  TouchableOpacity,
  StyleSheet,
  Animated,
  Dimensions,
} from 'react-native';
import {useNavigation} from '@react-navigation/native';
import EncryptedStorage from 'react-native-encrypted-storage';
import {MainNavigatorProp} from '../../types/navigation.d';
import FloatingButtonStyle from '../styles/Float/FloatingButtonStyle';
import Icon from 'react-native-vector-icons/MaterialCommunityIcons';

interface FloatingButtonProps {
  toggleOverlay: () => void;
}

const FloatingButton: React.FC<FloatingButtonProps> = ({toggleOverlay}) => {
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
    const session = await EncryptedStorage.getItem('user_session');
    const sessionData = session ? JSON.parse(session) : null;
    const userType = sessionData?.type;
    // const userType = await EncryptedStorage.getItem('userType');
    console.log(userType);
    if (userType === 'FAMILY') {
      navigation.navigate('FloatNavigator', {
        screen: 'FamilyVerifyRequestScreen',
      });
    } else if (userType === 'SOCIAL_WORKER') {
      console.log('여기로 왔니');
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
          <Animated.View
            style={[FloatingButtonStyle.secondaryButton, buttonStyle(-70)]}>
            <TouchableOpacity
              style={FloatingButtonStyle.button}
              onPress={handlePress('Home')}>
              <Icon name="home" style={FloatingButtonStyle.label} />
            </TouchableOpacity>
          </Animated.View>

          <Animated.View
            style={[FloatingButtonStyle.secondaryButton, buttonStyle(-140)]}>
            <TouchableOpacity
              style={FloatingButtonStyle.button}
              onPress={handlePressMessage}>
              <Icon name="email" style={FloatingButtonStyle.label} />
            </TouchableOpacity>
          </Animated.View>

          <Animated.View
            style={[FloatingButtonStyle.secondaryButton, buttonStyle(-210)]}>
            <TouchableOpacity
              style={FloatingButtonStyle.button}
              onPress={handlePressVerify}>
              <Icon name="account-check" style={FloatingButtonStyle.label} />
            </TouchableOpacity>
          </Animated.View>
        </>
      )}

      {/* Main Floating Button */}
      <TouchableOpacity onPress={toggleMenu} style={FloatingButtonStyle.fab}>
        <Icon
          name={isOpen ? 'close-thick' : 'plus-thick'}
          style={FloatingButtonStyle.fabText}
        />
      </TouchableOpacity>
    </View>
  );
};

export default FloatingButton;
