import {Dimensions, StyleSheet} from 'react-native';

const {width, height} = Dimensions.get('window');

const detailStyle = StyleSheet.create({
  picture: {
    backgroundColor: 'white',
    borderColor: 'black',
    borderWidth: 2,
    height: 180,
    width: 144,
    marginTop: 100,
  },
  button: {
    backgroundColor: '#FED7C3',
    padding: 10,
    marginTop: 20,
    marginBottom: 10,
    borderRadius: 10,
    elevation: 1,
  },
  title: {
    fontSize: 30,
  },
  bottomContainer: {
    flex: 1,
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    backgroundColor: '#FED7C3',
    width: '100%',
    marginTop: 30,
    paddingVertical: 10,
  },
  subContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
  },
});

export default detailStyle;
