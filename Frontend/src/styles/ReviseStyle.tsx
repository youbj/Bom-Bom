import {StyleSheet} from 'react-native';

const ReviseStyle = StyleSheet.create({
  title: {
    fontWeight: '600',
    fontSize: 30,
    marginTop: 50,
  },
  subtitle: {
    fontWeight: '500',
    fontSize: 20,
    marginVertical: 10,
    alignSelf: 'flex-start',
    paddingLeft: 10,
  },
  genderContainer: {
    flexDirection: 'row',
    marginLeft: 10,
  },

  genderButton: {
    paddingHorizontal: 12,
    paddingVertical: 8,
    backgroundColor: '#F5F7FA',
    marginHorizontal: 5,
    borderRadius: 5,
    elevation: 5,
  },

  selectedGender: {
    backgroundColor: '#FED7C3',
  },
  button: {
    backgroundColor: '#FED7C3',
    padding: 15,
    marginTop: 10,
    marginBottom: 10,
    borderRadius: 10,
    elevation: 2,
  },
  buttonText: {
    fontSize: 20,
    fontWeight: '500',
  },
});

export default ReviseStyle;
