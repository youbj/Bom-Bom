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
          <Animated.View style={[styles.secondaryButton, buttonStyle(-50)]}>
            <TouchableOpacity style={styles.button} onPress={handlePress('Home')}>
              <Text style={styles.label}>Home</Text>
            </TouchableOpacity>
          </Animated.View>

          <Animated.View style={[styles.secondaryButton, buttonStyle(-100)]}>
            <TouchableOpacity style={styles.button} onPress={handlePress('Message')}>
              <Text style={styles.label}>Message</Text>
            </TouchableOpacity>
          </Animated.View>

          <Animated.View style={[styles.secondaryButton, buttonStyle(-150)]}>
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
    position: 'absolute', // FloatingButton을 화면에 고정
    right: width * 0.05,
    bottom: height * 0.05,
    alignItems: 'center',
    justifyContent: 'center',
  },
  fab: {
    backgroundColor: '#6200ee',
    width: 60,
    height: 60,
    borderRadius: 30,
    alignItems: 'center',
    justifyContent: 'center',
    elevation: 8,
  },
  fabText: {
    color: 'white',
    fontSize: 24,
    fontWeight: 'bold',
  },
  secondaryButton: {
    position: 'absolute', // secondaryButton 위치를 고정
    right: width * 0.05 + 5,
    bottom: height * 0.15,
  },
  button: {
    backgroundColor: '#6200ee',
    width: 50,
    height: 50,
    borderRadius: 25,
    alignItems: 'center',
    justifyContent: 'center',
  },
  label: {
    color: 'white',
    fontSize: 12,
  },
});
