import { StyleSheet } from "react-native";

const enrollStyle = StyleSheet.create({
  title: {
    fontSize: 40,
    marginBottom: 30,
  },
  subContainer: {
    flexDirection: 'column',
    justifyContent: 'space-between',
  },
  nameGenderContainer: {
    flexDirection: 'row', 
    justifyContent: 'space-between', 
    marginBottom: 20,
  },
  nameInputContainer: {
    flex: 1, 
    marginRight: 10,
  },
  genderInputContainer: {
    flex: 1, 
  },
  fieldContainer: {
    marginBottom: 20, 
    alignItems: 'flex-start',
  },
  subtitle: {
    marginLeft: 10,
    marginBottom: 10,
    fontSize: 15,
    fontWeight: '500',
  },
  rowContainer: {
    flexDirection: 'row',
    alignItems: 'center',
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

  personListItem: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    padding: 10,
    backgroundColor: '#F5F7FA',
    marginVertical: 5,
    borderRadius: 10,
    elevation: 2,
  },
  
  finalSaveButton: {
    backgroundColor: '#FED7C3',
    padding: 15,
    alignItems: 'center',
    borderRadius: 5,
  },
});

export default enrollStyle;
