package org.jeongkkili.bombom.schedule.service;

import org.jeongkkili.bombom.member.domain.Member;
import org.jeongkkili.bombom.member.service.MemberService;
import org.jeongkkili.bombom.member_senior.service.MemberSeniorService;
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
public class DeleteScheduleServiceImpl implements DeleteScheduleService {

	private final ScheduleRepository scheduleRepository;
	private final MemberSeniorService memberSeniorService;
	private final MemberService memberService;

	@Override
	public void deleteSchedule(Long memberId, Long scheduleId) {
		Schedule schedule = scheduleRepository.getOrThrow(scheduleId);
		Member member = memberService.getMemberById(memberId);
		memberSeniorService.checkAssociation(member, schedule.getSenior());
		scheduleRepository.delete(schedule);
	}
}
