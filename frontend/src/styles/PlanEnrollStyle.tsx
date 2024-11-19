import {StyleSheet} from 'react-native';

const PlanEnrollStyle = StyleSheet.create({
  title: {
    fontWeight: '600',
    fontSize: 30,
    marginTop: 50,
    marginBottom: 30,
    alignSelf: 'center',
  },
  subTitle: {
    fontWeight: '500',
    fontSize: 20,
    textAlign: 'left',
    paddingLeft: 10,
    paddingBottom: 10,
  },
  button: {
    backgroundColor: '#FED7C3',
    marginTop: 5,
    marginRight: 5,
    paddingHorizontal: 13,
    paddingVertical: 10,
    alignItems: 'flex-end',
    borderRadius: 5,
    elevation: 2,
  },
  buttonText: {
    fontSize: 16,
    fontWeight: '600',
  },
});

export default PlanEnrollStyle;
