package org.jeongkkili.bombom.schedule.service;

import java.util.List;

import org.jeongkkili.bombom.schedule.service.dto.ScheduleMonthDto;
import org.jeongkkili.bombom.schedule.service.dto.ScheduleTodayDto;

public interface GetScheduleListService {

	List<ScheduleMonthDto> getMonthlyScheduleList(Long seniorId, Integer year, Integer month, Long memberId);

	List<ScheduleTodayDto> getTodayScheduleList(Long seniorId);
}
