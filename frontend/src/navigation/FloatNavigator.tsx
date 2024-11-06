// src/navigation/FloatNavigator.tsx
import React from 'react';
import { createNativeStackNavigator } from '@react-navigation/native-stack';
import MessageScreen from '../screens/Float/Message/MessageScreen';
import FamilyVerifyRequestScreen from '../screens/Float/Verify/FamilyVerifyRequestScreen';
import SocialWorkerApprovalScreen from '../screens/Float/Verify/SocialWorkerApprovalScreen';
import { FloatNavigatorParamList } from '../../types/navigation.d';

interface FloatNavigatorProps {
  userType: string | null;
}

const Stack = createNativeStackNavigator<FloatNavigatorParamList>();

const FloatNavigator: React.FC<FloatNavigatorProps> = ({ userType }) => (
  <Stack.Navigator>
    <Stack.Screen name="MessageScreen" component={MessageScreen} options={{ headerShown:false }} />
    {userType === 'family' ? (
      <Stack.Screen
        name="FamilyVerifyRequestScreen"
        component={FamilyVerifyRequestScreen}
        options={{ headerShown:false }}
      />
    ) : userType === 'socialWorker' ? (
      <Stack.Screen
        name="SocialWorkerApprovalScreen"
        component={SocialWorkerApprovalScreen}
        options={{ headerShown:false }}
      />
    ) : null}
  </Stack.Navigator>
);

export default FloatNavigator;
