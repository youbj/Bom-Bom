import {NativeStackNavigationProp} from '@react-navigation/native-stack';
import {RouteProp} from '@react-navigation/native';
import {DetailInfo} from '../src/screens/DetailScreen';

// 로그인 과정에 들어가는 StackParamList
export type AuthStackParamList = {
  Splash: undefined;
  Login: undefined;
  Join: undefined;
  Main: undefined;
  JoinDetail: {isType: 'SOCIAL_WORKER' | 'FAMILY'};
};

export type MainNavigatorParamList = {
  Main: undefined;
  FloatNavigator: {screen: keyof FloatNavigatorParamList};
  Enroll: undefined;
  Detail: undefined;
  Revise: {detail: DetailInfo};
};

export type FloatNavigatorParamList = {
  MessageScreen: undefined;
  FamilyVerifyRequestScreen: undefined;
  SocialWorkerApprovalScreen: undefined;
};

export type SplashScreenNavigationProp = NativeStackNavigationProp<
  AuthStackParamList,
  'Splash'
>;
export type LoginScreenNavigationProp = NativeStackNavigationProp<
  AuthStackParamList,
  'Login'
>;
export type JoinScreenNavigationProp = NativeStackNavigationProp<
  AuthStackParamList,
  'Join'
>;
export type JoinDetailRouteProp = RouteProp<AuthStackParamList, 'JoinDetail'>;
export type BackToLoginNavigationProp = NativeStackNavigationProp<
  AuthStackParamList,
  'JoinDetail'
>;
export type AuthToMainNavigationProp = NativeStackNavigationProp<
  AuthStackParamList,
  'Login'
>;
export type MainNavigatorProp =
  NativeStackNavigationProp<MainNavigatorParamList>;
export type FloatNavigatorProp =
  NativeStackNavigationProp<FloatNavigatorParamList>;

// 로그인 전후 판단을 위한 Props
export type AuthNavigatorProps = {
  setIsLoggedIn: (loggedIn: boolean) => void;
};

export type LoginScreenProps = {
  setIsLoggedIn: (loggedIn: boolean) => void;
};

export type SplashScreenProps = {
  setIsLoggedIn: (loggedIn: boolean) => void;
};
// 메인 페이지 이후의 StackParamList

export type MainStackParamList = {
  Main: undefined;
  Enroll: undefined;
  Detail: {seniorId: number};
  Revise: {detail: DetailInfo};
};

export type EnrollStackParamList = {
  Main: {reload: boolean} | undefined;
  Enroll: undefined;
};

export type MainToEnrollNavigationProp = NativeStackNavigationProp<
  MainStackParamList,
  'Main'
>;
export type EnrollToMainNavigationProp = NativeStackNavigationProp<
  MainStackParamList,
  'Enroll'
>;
export type MainToDetailNavigationProp = NativeStackNavigationProp<
  MainStackParamList,
  'Detail'
>;

export type DetailToReviseNavigationProp = NativeStackNavigationProp<
  MainNavigatorParamList,
  'Revise'
>;

export type MainScreenRouteProp = RouteProp<EnrollStackParamList, 'Main'>;
