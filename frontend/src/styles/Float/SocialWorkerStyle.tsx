import { StyleSheet } from "react-native";

const SocialWorkerStyle = StyleSheet.create({
    container: {
      flex: 1,
      padding: 20,
      paddingBottom: 100,
      backgroundColor: '#fff',
    },
    title: {
      fontSize: 24,
      fontWeight: '600',
      marginVertical: 20,
      textAlign: 'center',
    },
    listContainer: {
      paddingBottom: 20,
    },
    requestItem: {
      backgroundColor: '#FED7C3',
      padding: 15,
      borderRadius: 15,
      marginBottom: 15,
      elevation: 3,
    },
    textContainer: {
      marginBottom: 10,
    },
    name: {
      fontSize: 18,
      fontWeight: '500',
      marginBottom: 5,
    },
    info: {
      fontSize: 14,
      color: '#555',
      marginBottom: 3,
    },
    buttonContainer: {
      flexDirection: 'row',
      justifyContent: 'space-between',
      marginTop: 10,
    },
  });

  export default SocialWorkerStyle;