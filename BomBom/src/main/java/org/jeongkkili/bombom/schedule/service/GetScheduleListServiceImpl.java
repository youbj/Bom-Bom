package org.jeongkkili.bombom.schedule.service;

import java.util.List;

import org.jeongkkili.bombom.schedule.repository.custom.ScheduleRepositoryCustom;
import org.jeongkkili.bombom.schedule.service.dto.ScheduleMonthDto;
import org.jeongkkili.bombom.senior.domain.Senior;
import org.jeongkkili.bombom.senior.repository.SeniorRepository;
import org.springframework.stereotype.Service;

import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;

@Service
@RequiredArgsConstructor
@Slf4j
public class GetScheduleListServiceImpl implements GetScheduleListService {

	private final SeniorRepository seniorRepository;
	private final ScheduleRepositoryCustom scheduleRepositoryCustom;

	@Override
	public List<ScheduleMonthDto> getMonthlyScheduleList(Long seniorId, Integer year, Integer month) {
		Senior senior = seniorRepository.getOrThrow(seniorId);
		return scheduleRepositoryCustom.findMonthlyScheduleBySeniorId(senior, year, month);
	}
}
