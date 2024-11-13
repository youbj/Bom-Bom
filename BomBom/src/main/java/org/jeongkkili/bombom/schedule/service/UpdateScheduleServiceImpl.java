package org.jeongkkili.bombom.schedule.service;

import org.jeongkkili.bombom.member.domain.Member;
import org.jeongkkili.bombom.member.service.MemberService;
import org.jeongkkili.bombom.member_senior.service.MemberSeniorService;
import org.jeongkkili.bombom.schedule.controller.request.UpdateScheduleReq;
import org.jeongkkili.bombom.schedule.domain.Schedule;
import org.jeongkkili.bombom.schedule.repository.ScheduleRepository;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;

@Service
@RequiredArgsConstructor
@Transactional
@Slf4j
public class UpdateScheduleServiceImpl implements UpdateScheduleService {

	private final ScheduleRepository scheduleRepository;
	private final MemberService memberService;
	private final MemberSeniorService memberSeniorService;

	@Override
	public void updateSchedule(Long scheduleId, Long memberId, UpdateScheduleReq req) {
		Schedule schedule = scheduleRepository.getOrThrow(scheduleId);
		Member member = memberService.getMemberById(memberId);
		memberSeniorService.checkAssociation(member, schedule.getSenior());
		schedule.updateSchedule(req.getScheduleAt(), req.getMemo());
	}
}
