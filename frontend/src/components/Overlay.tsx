// src/components/Overlay.tsx
import React from 'react';
import { StyleSheet } from 'react-native';
import { BlurView } from '@react-native-community/blur';

interface OverlayProps {
    onClose: () => void; // 클릭 시 호출할 함수
}

const Overlay: React.FC<OverlayProps> = ({ onClose }) => {
  return (
    <BlurView
      style={styles.overlay}
      blurType="light"
      blurAmount={2}
      reducedTransparencyFallbackColor="rgba(0, 0, 0, 0.5)"
      pointerEvents="box-only" // 오버레이의 터치 이벤트를 무시하여 뒤 UI에 영향 없도록 설정
    />
  );
};

export default Overlay;

const styles = StyleSheet.create({
  overlay: {
    position: 'absolute',
    top: 0,
    left: 0,
    right: 0,
    bottom: 0,
    zIndex: 500,
  },
});
