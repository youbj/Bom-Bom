import {StyleSheet} from 'react-native';

const joinDetailStyle = StyleSheet.create({
  title: {
    alignItems: 'center',
    fontSize: 30,
  },
  space: {
    height: 40,
  },
  subContainer: {
    alignItems: 'flex-start',
    width: '100%',
  },
  input: {
    flex: 1,
    height: 40,
    backgroundColor: '#F5F7FA',
    borderColor: '#E5E8EB',
    borderWidth: 1,
    borderRadius: 12,
    paddingHorizontal: 16,
    marginBottom: 16,
  },
  subtitle: {
    fontSize: 20,
    marginLeft: 5,
    marginBottom: 10,
  },
  subSpace: {
    flexDirection: 'row',
    alignItems: 'center',
    width: '100%'
  },
  button: {
    marginTop: -18,
    width: 80,
    padding: 10,
    marginLeft: 10,
    backgroundColor: '#FED7C3',
    borderRadius: 12,
    elevation: 2,
  },
  buttonText: {
    textAlign: 'center',
    fontWeight: '500',
  }
});

export default joinDetailStyle;
