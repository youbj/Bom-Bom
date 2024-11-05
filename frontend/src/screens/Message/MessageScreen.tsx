// src/pages/MessagePage.tsx
import React, { useState } from 'react';
import { View, TouchableOpacity, StyleSheet } from 'react-native';
import { useNavigation } from '@react-navigation/native';
import Icon from 'react-native-vector-icons/MaterialCommunityIcons'; // Adjust based on your icon library
import CustomText from '../../components/CustomText';
import CustomTextInput from '../../components/CustomTextInput';

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
    <View style={styles.container}>
      <TouchableOpacity style={styles.backIcon} onPress={handleBack}>
        <Icon
          name="arrow-left"
          color="#000000"
          size={30}
          style={{ marginTop: -1, marginLeft: -3 }}
        />
      </TouchableOpacity>
      <CustomText style={styles.title}>단체 대화 보내기</CustomText>
      <CustomTextInput
        style={styles.input}
        placeholder="대화를 입력해주세요."
        value={message}
        onChangeText={setMessage}
      />
      <TouchableOpacity style={styles.button} onPress={handleSend}>
        <CustomText style={styles.buttonText}>Send</CustomText>
      </TouchableOpacity>
    </View>
  );
};

export default MessageScreen;

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: 'center',
    padding: 20,
    backgroundColor: '#fff',
  },
  backIcon: {
    position: 'absolute',
    top: 10,
    left: 10,
    padding: 10,
  },
  title: {
    fontSize: 24,
    fontWeight: 'bold',
    marginBottom: 20,
    textAlign: 'center',
  },
  input: {
    height: 40,
    borderColor: '#ccc',
    borderWidth: 1,
    paddingHorizontal: 10,
    marginBottom: 20,
  },
  button: {
    backgroundColor: '#FED7C3',
    paddingVertical: 10,
    borderRadius: 5,
    alignItems: 'center',
  },
  buttonText: {
    color: '#000',
    fontSize: 16,
    fontWeight: 'bold',
  },
});
