// FloatingButton.tsx
import React, { useState } from 'react';
import { View, Text, TouchableOpacity, StyleSheet, Animated, Dimensions } from 'react-native';

const { width, height } = Dimensions.get('window');

const FloatingButton: React.FC = () => {
  const [isOpen, setIsOpen] = useState<boolean>(false);
  const animation = useState(new Animated.Value(0))[0];

  const toggleMenu = () => {
    const toValue = isOpen ? 0 : 1;

    Animated.timing(animation, {
      toValue,
      duration: 300,
      useNativeDriver: true,
    }).start();

    setIsOpen(!isOpen);
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

  const handlePress = (message: string) => () => {
    console.log(message);
  };

  return (
    <View style={styles.container}>
      {isOpen && (
        <>
          <Animated.View style={[styles.secondaryButton, buttonStyle(-70)]}>
            <TouchableOpacity style={styles.button} onPress={handlePress('Home')}>
              <Text style={styles.label}>Home</Text>
            </TouchableOpacity>
          </Animated.View>

          <Animated.View style={[styles.secondaryButton, buttonStyle(-140)]}>
            <TouchableOpacity style={styles.button} onPress={handlePress('Message')}>
              <Text style={styles.label}>Message</Text>
            </TouchableOpacity>
          </Animated.View>

          <Animated.View style={[styles.secondaryButton, buttonStyle(-210)]}>
            <TouchableOpacity style={styles.button} onPress={handlePress('Verify')}>
              <Text style={styles.label}>Verify</Text>
            </TouchableOpacity>
          </Animated.View>
        </>
      )}

      <TouchableOpacity onPress={toggleMenu} style={styles.fab}>
        <Text style={styles.fabText}>+</Text>
      </TouchableOpacity>
    </View>
  );
};

export default FloatingButton;


const styles = StyleSheet.create({
  container: {
    position: 'absolute',
    right: '5%', // 화면 오른쪽에 5% 여백
    bottom: '5%', // 화면 아래쪽에 5% 여백
    alignItems: 'center', // secondaryButton들이 fab과 중앙 정렬되도록 설정
  },
  fab: {
    backgroundColor: '#6200ee',
    width: width * 0.15, // 화면 너비의 15% 크기로 설정
    height: width * 0.15,
    borderRadius: (width * 0.15) / 2,
    alignItems: 'center',
    justifyContent: 'center',
    elevation: 8,
  },
  fabText: {
    color: 'white',
    fontSize: width * 0.08,
    fontWeight: 'bold',
  },
  secondaryButton: {
    position: 'absolute',
    right: (width * 0.15 - width * 0.125) / 2, // fab의 너비와 secondaryButton 너비를 기준으로 중앙 맞춤
    bottom: height * 0.03,
  },
  button: {
    backgroundColor: '#6200ee',
    width: width * 0.125, // 화면 너비의 12.5% 크기로 설정
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
