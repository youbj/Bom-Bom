import React from 'react';
import {View, StyleSheet} from 'react-native';
import CustomText from './CustomText';
import {AnimatedCircularProgress} from 'react-native-circular-progress';

const DonutChart = ({progress}: {progress: number}) => {
  return (
    <View style={styles.container}>
      <AnimatedCircularProgress
        size={150} // 도넛 크기
        width={15} // 두께
        fill={progress} // 진행률 (0~100)
        tintColor="#FF6F61" // 진행된 부분 색상
        backgroundColor="#fff" // 배경 부분 색상
        rotation={0} // 시작 위치를 위쪽으로 설정
        lineCap="round" // 끝부분을 둥글게 설정
      >
        {fill => (
          <CustomText style={styles.progressText}>{`${Math.round(
            fill,
          )}%`}</CustomText>
        )}
      </AnimatedCircularProgress>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    justifyContent: 'center',
    alignItems: 'center',
  },
  progressText: {
    fontSize: 24,
    fontWeight: '600',
    color: '#333',
  },
});

export default DonutChart;
