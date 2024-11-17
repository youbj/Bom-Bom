import {StyleSheet} from 'react-native';

const FeelingDetailStyle = StyleSheet.create({
  headerText: {
    fontWeight: '600',
    fontSize: 30,
    marginBottom: 20,
  },
  searchInput: {
    marginHorizontal: 10,
    marginTop: 20,
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: '#FFF5EE',
  },
  listRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    paddingVertical: 10,
    paddingHorizontal: 10,
    width: '100%',
  },
  leftContainer: {
    flex: 1,
    flexDirection: 'row',
    alignItems: 'center',
    paddingVertical: 5,
  },
  rightContainer: {
    flex: 1,
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    backgroundColor: '#FFF5EE',
    paddingVertical: 5,
    paddingHorizontal: 10,
    borderRadius: 10,
  },
  timeline: {
    alignItems: 'center',
    justifyContent: 'center',
    marginRight: 10,
    position: 'relative',
  },
  timelineSpacer: {
    width: 12,
    height: 12,
    backgroundColor: 'transparent',
  },
  dateText: {
    fontSize: 18,
    fontWeight: '600',
    color: '#333',
    marginLeft: 5,
  },
  timeText: {
    fontSize: 14,
    color: '#666',
  },
  emoji: {
    fontSize: 20,
  },
  emptyText: {
    textAlign: 'center',
    marginTop: 20,
    fontSize: 16,
    color: 'gray',
    paddingBottom: 100,
  },
});

export default FeelingDetailStyle;
