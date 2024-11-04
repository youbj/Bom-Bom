package org.jeongkkili.bombom.schedule.service;

import java.util.List;

import org.jeongkkili.bombom.schedule.service.dto.ScheduleMonthDto;

public interface GetScheduleListService {

	List<ScheduleMonthDto> getMonthlyScheduleList(Long seniorId, Integer year, Integer month, Long memberId);
}
