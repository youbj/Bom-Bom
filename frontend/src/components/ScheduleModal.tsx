import React from 'react';
import {View, Modal, TouchableOpacity, StyleSheet} from 'react-native';
import CustomText from './CustomText';
import CustomTextInput from './CustomTextInput';
import {renderDateTimeInput} from '../utils/RenderDateTimeInput';
import defaultStyle from '../styles/DefaultStyle';
import PlanStyle from '../styles/PlanStyle';

interface ScheduleModalProps {
  modalVisible: boolean;
  editedSchedule: {startAt: string; endAt: string; memo: string};
  setEditedSchedule: (schedule: {
    startAt: string;
    endAt: string;
    memo: string;
  }) => void;
  closeModal: () => void;
  handleEdit: () => void;
  handleDelete: () => void;
}

const ScheduleModal = ({
  modalVisible,
  editedSchedule,
  setEditedSchedule,
  closeModal,
  handleEdit,
  handleDelete,
}: ScheduleModalProps): JSX.Element => {
  const handleDateChange = (type: 'startAt' | 'endAt', date: string) => {
    const currentTime = editedSchedule[type]?.split('T')[1] || '';
    setEditedSchedule({
      ...editedSchedule,
      [type]: date ? `${date}T${currentTime}` : `T${currentTime}`,
    });
  };

  const handleTimeChange = (type: 'startAt' | 'endAt', time: string) => {
    const currentDate = editedSchedule[type]?.split('T')[0] || '';
    setEditedSchedule({
      ...editedSchedule,
      [type]: time ? `${currentDate}T${time}` : `${currentDate}T`,
    });
  };

  return (
    <Modal visible={modalVisible} transparent={true} animationType="slide">
      <View
        style={{
          flex: 1,
          justifyContent: 'center',
          alignItems: 'center',
          backgroundColor: 'rgba(0,0,0,0.5)',
        }}>
        <View
          style={{
            width: '88%',
            padding: 20,
            backgroundColor: 'white',
            borderRadius: 10,
          }}>
          <View style={{alignItems: 'center'}}>
            <CustomText
              style={{
                fontWeight: '600',
                fontSize: 23,
                marginBottom: 20,
                textAlign: 'center',
              }}>
              일정 수정
            </CustomText>
          </View>
          {renderDateTimeInput(
            '시작 일정',
            editedSchedule.startAt?.split('T')[0] || '',
            date => handleDateChange('startAt', date),
            editedSchedule.startAt?.split('T')[1]?.slice(0, 5) || '',
            time => handleTimeChange('startAt', time),
          )}
          {renderDateTimeInput(
            '종료 일정',
            editedSchedule.endAt?.split('T')[0] || '',
            date => handleDateChange('endAt', date),
            editedSchedule.endAt?.split('T')[1]?.slice(0, 5) || '',
            time => handleTimeChange('endAt', time),
          )}

          <CustomText
            style={{
              fontWeight: '500',
              marginBottom: 10,
              paddingLeft: 10,
              fontSize: 16,
            }}>
            메모
          </CustomText>
          <CustomTextInput
            value={editedSchedule.memo}
            onChangeText={text =>
              setEditedSchedule({...editedSchedule, memo: text})
            }
            style={defaultStyle.input}
          />
          <View
            style={{
              flexDirection: 'row',
              justifyContent: 'space-between',
              marginHorizontal: 15,
              gap: 30,
            }}>
            <TouchableOpacity
              onPress={handleEdit}
              style={[PlanStyle.button, {flex: 1, alignItems: 'center'}]}>
              <CustomText
                style={StyleSheet.flatten([
                  PlanStyle.buttonText,
                  {fontSize: 16},
                ])}>
                수정
              </CustomText>
            </TouchableOpacity>
            <TouchableOpacity
              onPress={handleDelete}
              style={[PlanStyle.button, {flex: 1, alignItems: 'center'}]}>
              <CustomText
                style={StyleSheet.flatten([
                  PlanStyle.buttonText,
                  {fontSize: 16},
                ])}>
                삭제
              </CustomText>
            </TouchableOpacity>
          </View>
          <TouchableOpacity onPress={closeModal} style={{marginTop: 15}}>
            <CustomText
              style={{
                textAlign: 'center',
                fontSize: 18,
                color: '#FF8C69',
                fontWeight: '600',
              }}>
              닫기
            </CustomText>
          </TouchableOpacity>
        </View>
      </View>
    </Modal>
  );
};

export default ScheduleModal;
