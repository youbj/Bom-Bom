import {StyleSheet} from 'react-native';

const joinStyle = StyleSheet.create({
  title: {
    fontSize: 60,
  },
  buttons: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    gap: 50,
  },
  icon: {
    color: 'black',
    fontSize: 45,
    textAlign: 'center',
  },
  button: {
    justifyContent: 'center',
    alignItems: 'center',
    width: 130,
    height: 180,
    backgroundColor: '#FED7C3',
    borderRadius: 12,
    elevation: 2,
  },
  buttonText: {
    textAlign: 'center',
    fontSize: 25,
    fontWeight: '400',
  },
});

export default joinStyle;
