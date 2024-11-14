import {StyleSheet} from 'react-native';

const PlanStyle = StyleSheet.create({
  title: {
    fontSize: 30,
    textAlign: 'center',
    marginTop: 60,
    marginBottom: 30,
    fontWeight: '600',
  },
  subTitle: {
    fontSize: 20,
    textAlign: 'center',
    fontWeight: '500',
  },
  calendar: {
    borderRadius: 10,
    overflow: 'hidden',
    minWidth: '95%',
    elevation: 5,
    paddingVertical: 10,
  },
  button: {
    backgroundColor: '#FED7C3',
    marginTop: 20,
    padding: 10,
    alignItems: 'flex-end',
    borderRadius: 5,
    elevation: 2,
  },
  buttonText: {
    fontWeight: '600',
  },
});

export default PlanStyle;
