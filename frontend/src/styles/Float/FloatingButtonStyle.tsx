import { Dimensions, StyleSheet } from "react-native";

const { width, height } = Dimensions.get('window');

const FloatingButtonStyle = StyleSheet.create({
    container: {
      position: 'absolute',
      right: '5%',
      bottom: '5%',
      alignItems: 'center',
      zIndex: 1000, // Ensure FloatingButton is above other elements
    },
    fab: {
      backgroundColor: '#6200ee',
      width: width * 0.15,
      height: width * 0.15,
      borderRadius: (width * 0.15) / 2,
      alignItems: 'center',
      justifyContent: 'center',
      elevation: 8,
      zIndex: 1001, // Floating button above overlay
    },
    fabText: {
      color: 'white',
      fontSize: width * 0.08,
      fontWeight: 'bold',
    },
    secondaryButton: {
      position: 'absolute',
      right: (width * 0.15 - width * 0.125) / 2,
      bottom: height * 0.03,
      zIndex: 1001,
    },
    button: {
      backgroundColor: '#6200ee',
      width: width * 0.125,
      height: width * 0.125,
      borderRadius: (width * 0.125) / 2,
      alignItems: 'center',
      justifyContent: 'center',
    },
    label: {
      color: 'white',
      fontSize: width * 0.03,
    },
  });
  
  export default FloatingButtonStyle;