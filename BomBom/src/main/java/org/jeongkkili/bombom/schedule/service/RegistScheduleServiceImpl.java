package org.jeongkkili.bombom.schedule.service;

import org.jeongkkili.bombom.member.domain.Member;
import org.jeongkkili.bombom.member.service.MemberService;
import org.jeongkkili.bombom.member_senior.service.MemberSeniorService;
import org.jeongkkili.bombom.schedule.controller.request.RegistScheduleReq;
import org.jeongkkili.bombom.schedule.domain.Schedule;
import org.jeongkkili.bombom.schedule.repository.ScheduleRepository;
import org.jeongkkili.bombom.senior.domain.Senior;
import org.jeongkkili.bombom.senior.service.GetSeniorService;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;

@Service
@RequiredArgsConstructor
@Transactional
@Slf4j
public class RegistScheduleServiceImpl implements RegistScheduleService {

	private final MemberService memberService;
	private final GetSeniorService getSeniorService;
	private final MemberSeniorService memberSeniorService;
	private final ScheduleRepository scheduleRepository;

	@Override
	public void registSchedule(RegistScheduleReq req, Long memberId) {
		Member member = memberService.getMemberById(memberId);
		Senior senior = getSeniorService.getSeniorById(req.getSeniorId());
		memberSeniorService.checkAssociation(member, senior);
		scheduleRepository.save(Schedule.builder()
			.senior(senior)
			.scheduleAt(req.getScheduleAt())
			.memo(req.getMemo())
			.build());
	}
}
