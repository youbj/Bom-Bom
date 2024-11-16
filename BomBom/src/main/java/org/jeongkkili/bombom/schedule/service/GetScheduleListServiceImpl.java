package org.jeongkkili.bombom.schedule.service;

import java.util.List;

import org.jeongkkili.bombom.member.domain.Member;
import org.jeongkkili.bombom.member.service.MemberService;
import org.jeongkkili.bombom.member_senior.service.MemberSeniorService;
import org.jeongkkili.bombom.schedule.repository.custom.ScheduleRepositoryCustom;
import org.jeongkkili.bombom.schedule.service.dto.ScheduleMonthDto;
import org.jeongkkili.bombom.schedule.service.dto.ScheduleTodayDto;
import org.jeongkkili.bombom.senior.domain.Senior;
import org.jeongkkili.bombom.senior.service.GetSeniorService;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;

@Service
@RequiredArgsConstructor
@Transactional(readOnly = true)
@Slf4j
public class GetScheduleListServiceImpl implements GetScheduleListService {

	private final MemberService memberService;
	private final GetSeniorService getSeniorService;
	private final MemberSeniorService memberSeniorService;
	private final ScheduleRepositoryCustom scheduleRepositoryCustom;

	@Override
	public List<ScheduleMonthDto> getMonthlyScheduleList(Long seniorId, Integer year, Integer month, Long memberId) {
		Member member = memberService.getMemberById(memberId);
		Senior senior = getSeniorService.getSeniorById(seniorId);
		memberSeniorService.checkAssociation(member, senior);
		return scheduleRepositoryCustom.findMonthlyScheduleBySeniorId(senior, year, month);
	}

	@Override
	public List<ScheduleTodayDto> getTodayScheduleList(Long seniorId) {
		Senior senior = getSeniorService.getSeniorById(seniorId);
		return scheduleRepositoryCustom.findTodayScheduleBySeniorId(senior);
	}
}
