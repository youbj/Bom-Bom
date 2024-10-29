import { NativeStackNavigationProp } from '@react-navigation/native-stack';

// RootStackParamList 타입 정의
export type useNavigationParamList = {
  Splash: undefined;
  Login: undefined;
};

// 네비게이션 타입 정의
export type SplashScreenNavigationProp = NativeStackNavigationProp<useNavigationParamList, 'Splash'>;
