package org.jeongkkili.bombom.schedule.service;

import org.jeongkkili.bombom.schedule.controller.request.RegistScheduleReq;

public interface RegistScheduleService {

	void registSchedule(RegistScheduleReq req, Long memberId);
}
