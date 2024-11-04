package org.jeongkkili.bombom.schedule.service;

import org.jeongkkili.bombom.schedule.controller.request.RegistScheduleReq;
import org.jeongkkili.bombom.schedule.domain.Schedule;
import org.jeongkkili.bombom.schedule.repository.ScheduleRepository;
import org.jeongkkili.bombom.senior.domain.Senior;
import org.jeongkkili.bombom.senior.repository.SeniorRepository;
import org.springframework.stereotype.Service;

import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;

@Service
@RequiredArgsConstructor
@Slf4j
public class RegistScheduleServiceImpl implements RegistScheduleService {

	private final SeniorRepository seniorRepository;
	private final ScheduleRepository scheduleRepository;

	@Override
	public void registSchedule(RegistScheduleReq req) {
		Senior senior = seniorRepository.getOrThrow(req.getSeniorId());
		scheduleRepository.save(Schedule.builder()
			.senior(senior)
			.scheduleAt(req.getScheduleAt())
			.memo(req.getMemo())
			.build());
	}
}
