import { NativeStackNavigationProp } from '@react-navigation/native-stack';
import { RouteProp } from '@react-navigation/native';

// 로그인 과정에 들어가는 StackParamList
export type AuthStackParamList = {
  Splash: undefined;
  Login: undefined;
  Join: undefined;
  Main: undefined;
  JoinDetail: { isType: 'SOCIAL_WORKER' | 'FAMILY' };
};

export type MainNavigatorParamList = {
  Main: undefined;
  FloatNavigator: undefined;  // 중첩된 FloatNavigator
};

export type FloatNavigatorParamList = {
  MessageScreen: undefined;
};

export type SplashScreenNavigationProp = NativeStackNavigationProp<AuthStackParamList, 'Splash'>;
export type LoginScreenNavigationProp = NativeStackNavigationProp<AuthStackParamList, 'Login'>;
export type JoinScreenNavigationProp = NativeStackNavigationProp<AuthStackParamList, 'Join'>;
export type JoinDetailRouteProp = RouteProp<AuthStackParamList, 'JoinDetail'>;
export type BackToLoginNavigationProp = NativeStackNavigationProp<AuthStackParamList, 'JoinDetail'>;
export type AuthToMainNavigationProp = NativeStackNavigationProp<AuthStackParamList, 'Login'>;
export type MainNavigatorProp = NativeStackNavigationProp<MainNavigatorParamList>;
export type FloatNavigatorProp = NativeStackNavigationProp<FloatNavigatorParamList>;

// 로그인 전후 판단을 위한 Props
export type AuthNavigatorProps = {
  setIsLoggedIn: (loggedIn: boolean) => void;
};

export type LoginScreenProps = {
  setIsLoggedIn: (loggedIn: boolean) => void;
};
