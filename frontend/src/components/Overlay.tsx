// src/components/Overlay.tsx
import React from 'react';
import { StyleSheet, TouchableWithoutFeedback, View } from 'react-native';
import { BlurView } from '@react-native-community/blur';

interface OverlayProps {
  onClose: () => void; // 클릭 시 호출할 함수
}

const Overlay: React.FC<OverlayProps> = ({ onClose }) => {
  return (
    <TouchableWithoutFeedback onPress={onClose}>
      <View style={styles.container}>
        <BlurView
          style={styles.overlay}
          blurType="light"
          blurAmount={2}
          reducedTransparencyFallbackColor="rgba(0, 0, 0, 0.5)"
        />
      </View>
    </TouchableWithoutFeedback>
  );
};

export default Overlay;

const styles = StyleSheet.create({
  container: {
    ...StyleSheet.absoluteFillObject,
    zIndex: 500,
  },
  overlay: {
    flex: 1,
  },
});
