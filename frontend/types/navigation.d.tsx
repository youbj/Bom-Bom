import { NativeStackNavigationProp } from '@react-navigation/native-stack';
import { RouteProp } from '@react-navigation/native';

// 로그인 과정에 들어가는 StackParamList
export type MainStackParamList = {
  Splash: undefined;
  Login: undefined;
  Join: undefined;
  JoinDetail: { isType: 'SOCIAL_WORKER' | 'FAMILY' };
};

export type SplashScreenNavigationProp = NativeStackNavigationProp<MainStackParamList, 'Splash'>;
export type LoginScreenNavigationProp = NativeStackNavigationProp<MainStackParamList, 'Login'>;
export type JoinScreenNavigationProp = NativeStackNavigationProp<MainStackParamList, 'Join'>;
export type JoinDetailRouteProp = RouteProp<MainStackParamList, 'JoinDetail'>;
