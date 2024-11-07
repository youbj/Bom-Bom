import { StyleSheet } from "react-native";

const FamilyStyle = StyleSheet.create({
    container: {
      flex: 1,
      padding: 20,
      backgroundColor: '#fff',
    },
    title: {
      fontSize: 24,
      fontWeight: 'bold',
      textAlign: 'center',
      marginBottom: 30,
    },
    inputContainer: {
      marginBottom: 15,
    },
    label: {
      fontSize: 16,
      fontWeight: '500',
      marginBottom: 5,
      color: '#333',
    },
    input: {
      height: 50,
      backgroundColor: '#FED7C3',
      borderRadius: 25,
      paddingHorizontal: 20,
      fontSize: 16,
      color: '#333',
      // shadowColor: '#000',
      // shadowOffset: { width: 0, height: 2 },
      // shadowOpacity: 0.1,
      // shadowRadius: 5,
      // elevation: 5,
    },
  });

  export default FamilyStyle;