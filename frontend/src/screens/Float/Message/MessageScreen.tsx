// src/pages/MessagePage.tsx
import React, { useState } from 'react';
import { View, TouchableOpacity } from 'react-native';
import { useNavigation } from '@react-navigation/native';
import Icon from 'react-native-vector-icons/MaterialCommunityIcons'; // Adjust based on your icon library
import CustomText from '../../../components/CustomText';
import CustomTextInput from '../../../components/CustomTextInput';
import MessageStyle from '../../../styles/Float/MessageStyle'
import BackButton from '../../../components/BackButton';

const MessageScreen: React.FC = () => {
  const [message, setMessage] = useState('');
  const navigation = useNavigation();

  const handleSend = () => {
    console.log('Message sent:', message);
    setMessage(''); // Clear the input field after sending the message
  };

  const handleBack = () => {
    navigation.goBack(); // Navigate to the previous screen
  };

  return (
    <View style={MessageStyle.container}>
      <BackButton/>
      <CustomText style={MessageStyle.title}>단체 대화 보내기</CustomText>
      <CustomTextInput
        style={MessageStyle.input}
        placeholder="대화를 입력해주세요."
        value={message}
        onChangeText={setMessage}
      />
      <TouchableOpacity style={MessageStyle.button} onPress={handleSend}>
        <CustomText style={MessageStyle.buttonText}>Send</CustomText>
      </TouchableOpacity>
    </View>
  );
};

export default MessageScreen;


