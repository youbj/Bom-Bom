import React from 'react';
import {View, StyleSheet, Text} from 'react-native';
import {BarChart} from 'react-native-gifted-charts';
import moment from 'moment';
import 'moment/locale/ko';

interface WeeklyChartProps {
  rawData: (number | null)[]; // 데이터 배열
}

interface ChartDataItem {
  value: number;
  label: string;
  frontColor: string;
  barBorderRadius: number;
}

const WeeklyChart = ({rawData}: WeeklyChartProps): JSX.Element => {
  const last7Days = Array.from({length: 7}, (_, i) =>
    moment()
      .utcOffset(9)
      .subtract(6 - i, 'days')
      .format('dd DD'),
  );

  // 값에 따른 색상 계산 함수
  const calculateColor = (value: number | null): string => {
    if (value === null || value === 0) return '#d3d3d3'; // null과 0은 회색
    if (value < 50) {
      // 파랑 계열 (0~50)
      return `rgba(133, 193, 233, ${1 - (value / 50) * 0.7})`;
    } else {
      // 빨강 계열 (50~100)
      return `rgba(246, 108, 69, ${((value - 50) * 7) / 500 + 0.3})`;
    }
  };

  // BarChart에 맞는 데이터로 변환
  const chartData = rawData.map((value, index) => ({
    value: value !== null ? Math.round(value) : 0, // null을 0으로 처리
    label: last7Days[index], // 날짜를 라벨로 설정
    frontColor: calculateColor(value), // 색상 계산 결과 적용
    barBorderRadius: value !== null && value > 0 ? 10 : 0, // 윗부분만 둥글게
  }));

  return (
    <View style={{paddingTop: 20, marginLeft: -25}}>
      {/* BarChart */}
      <View>
        <BarChart
          data={chartData} // 데이터
          isAnimated
          barWidth={25}
          spacing={15}
          barBorderRadius={2}
          hideRules
          yAxisThickness={2}
          xAxisThickness={2}
          noOfSections={5}
          maxValue={100}
          stepValue={20}
          xAxisLabelTextStyle={styles.axisText}
          yAxisTextStyle={styles.axisText}
          renderTooltip={(item: ChartDataItem) => (
            <Text style={[styles.dataPointText]}>{item.value}</Text>
          )}
        />
      </View>
    </View>
  );
};

const styles = StyleSheet.create({
  axisText: {
    fontFamily: 'Paperlogy-6SemiBold',
    fontSize: 12,
    color: '#333',
  },
  dataPointText: {
    position: 'absolute',
    textAlign: 'center',
    fontFamily: 'Paperlogy-6SemiBold',
    fontSize: 12,
    color: '#333',
    top: 40,
    left: 4,
  },
});

export default WeeklyChart;
