import {StyleSheet} from 'react-native';

const MainStyle = StyleSheet.create({
  title: {
    fontSize: 30,
    fontWeight: '600',
    marginVertical: 15,
    marginLeft: 5,
  },

  menu: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    height: 40,
    paddingHorizontal: 10,
    marginBottom: 5,
  },

  arr: {
    flex: 1,
    flexDirection: 'row',
  },

  arrText: {
    fontSize: 17,
    fontWeight: '600',
  },
  list: {
    flexDirection: 'row',
    backgroundColor: '#FED7C3',
    width: '100%',
    height: 70,
    paddingHorizontal: 30,
    justifyContent: 'space-between',
    alignItems: 'center',
    borderRadius: 12,
    elevation: 2,
  },
  subList: {
    maxWidth: '50%',
  },
  listText: {
    fontSize: 20,
    fontWeight: '500',
  },
  addText: {
    fontSize: 15,
    color: '#555555',
    fontWeight: '400',
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
  },
});

export default MainStyle;
