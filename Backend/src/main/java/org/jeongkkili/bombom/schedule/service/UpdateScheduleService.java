package org.jeongkkili.bombom.schedule.service;

import org.jeongkkili.bombom.schedule.controller.request.UpdateScheduleReq;

public interface UpdateScheduleService {

	void updateSchedule(Long scheduleId, Long memberId, UpdateScheduleReq req);
}
