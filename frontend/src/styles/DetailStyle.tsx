import {Dimensions, StyleSheet} from 'react-native';

const {width, height} = Dimensions.get('window');

const detailStyle = StyleSheet.create({
  picture: {
    backgroundColor: 'white',
    borderColor: 'black',
    borderWidth: 2,
    height: 160,
    width: 128,
    marginTop: 100,
    justifyContent: 'center',
    alignItems: 'center',
  },
  button: {
    backgroundColor: '#FED7C3',
    padding: 10,
    marginTop: 20,
    marginBottom: 10,
    borderRadius: 10,
    elevation: 1,
    justifyContent: 'center',
  },
  title: {
    fontSize: 30,
    paddingLeft: 35,
    paddingRight: 5,
  },
  bottomContainer: {
    flex: 1,
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    backgroundColor: '#FED7C3',
    width: '100%',
    paddingVertical: 10,
  },
  subContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
  },
  graphTitle: {
    marginTop: 20,
    fontWeight: '600',
    fontSize: 18,
    color: '#000',
  },
  subTitle: {
    fontSize: 16,
    fontWeight: '600',
    paddingBottom: 5,
  },
  info: {
    justifyContent: 'center',
    alignItems: 'center',
    paddingVertical: 10,
    borderBottomColor: '#000',
    borderBottomWidth: 2,
  },
});

export default detailStyle;
