import React, {useState, useEffect} from 'react';
import {View, TouchableOpacity, Animated} from 'react-native';
import {useNavigation} from '@react-navigation/native';
import EncryptedStorage from 'react-native-encrypted-storage';
import {MainNavigatorProp} from '../../types/navigation.d';
import FloatingButtonStyle from '../styles/Float/FloatingButtonStyle';
import Icon from 'react-native-vector-icons/MaterialCommunityIcons';
import Overlay from './Overlay';
import {useUserType} from '../navigation/MainNavigator';

interface FloatingButtonProps {
  toggleOverlay: () => void;
  isDetailScreen: boolean;
  isOpen: boolean;
  setIsOpen: (open: boolean) => void;
}

const FloatingButton: React.FC<FloatingButtonProps> = ({isDetailScreen}) => {
  const [isOpen, setIsOpen] = useState(false);
  const animation = useState(new Animated.Value(0))[0];
  const navigation = useNavigation<MainNavigatorProp>();
  const userType = useUserType();

  useEffect(() => {
    Animated.timing(animation, {
      toValue: isDetailScreen ? 0.5 : 0,
      duration: 300,
      useNativeDriver: true,
    }).start();
  }, [isDetailScreen]);

  const toggleMenu = () => {
    const toValue = isOpen ? 0 : 1;
    Animated.timing(animation, {
      toValue,
      duration: 300,
      useNativeDriver: true,
    }).start();
    setIsOpen(!isOpen);
  };

  const closeMenu = () => {
    Animated.timing(animation, {
      toValue: 0,
      duration: 300,
      useNativeDriver: true,
    }).start();
    setIsOpen(false);
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

  const handlePressVerify = () => {
    toggleMenu();
    if (userType === 'FAMILY') {
      navigation.navigate('FloatNavigator', {
        screen: 'FamilyVerifyRequestScreen',
      });
    } else if (userType === 'SOCIAL_WORKER') {
      navigation.navigate('FloatNavigator', {
        screen: 'SocialWorkerApprovalScreen',
      });
    }
  };

  const handlePressMessage = () => {
    closeMenu();
    navigation.navigate('FloatNavigator', {screen: 'MessageScreen'});
  };

  const handlePressMain = () => {
    closeMenu();
    navigation.navigate('Main');
  };

  return (
    <>
      {isOpen && <Overlay onClose={closeMenu} />}

      <View
        style={[
          FloatingButtonStyle.container,
          isDetailScreen && {bottom: '42%'},
        ]}>
        {isOpen && (
          <>
            <Animated.View
              style={[FloatingButtonStyle.secondaryButton, buttonStyle(-70)]}>
              <TouchableOpacity
                style={FloatingButtonStyle.button}
                onPress={handlePressMain}>
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

        <TouchableOpacity onPress={toggleMenu} style={FloatingButtonStyle.fab}>
          <Icon
            name={isOpen ? 'close-thick' : 'plus-thick'}
            style={FloatingButtonStyle.fabText}
          />
        </TouchableOpacity>
      </View>
    </>
  );
};

export default FloatingButton;
