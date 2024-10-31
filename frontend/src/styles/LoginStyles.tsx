import {StyleSheet} from 'react-native';

const loginStyle = StyleSheet.create({
  title: {
    fontSize: 32,
    fontWeight: '400',
  },
  logo: {
    width: 128,
    height: 128,
    marginBottom: 16,
  },
  passwordInput: {
    flex: 1,
    width: '100%',
    height: 40,
    backgroundColor: '#F5F7FA',
    borderColor: '#E5E8EB',
    borderWidth: 1,
    borderRadius: 12,
    paddingHorizontal: 16,
    marginBottom: 16,
    flexDirection: 'row',
    alignItems: 'center',
  },
  iconContainer: {
    width: 30,
  },
  longSpace: {
    height: 100,
  },
  button: {
    width: '100%',
    height: 40,
    backgroundColor: '#FED7C3',
    justifyContent: 'center',
    alignItems: 'center',
    borderRadius: 12,
    elevation: 2,
  },
  buttonText: {
    color: '#FFFFFF',
    fontSize: 16,
    fontWeight: '600',
  },
  space: {
    height: 16,
  },
  rowContainer: {
    flexDirection: 'row',
    alignSelf: 'flex-end',
    justifyContent: 'flex-end',
    alignItems: 'center',
  },
  text: {
    fontWeight: '600',
    fontSize: 16,
    color: '#aaa',
  },
  transparentButton: {
    backgroundColor: '#fff',
    elevation: 0,
  },
});

export default loginStyle;
