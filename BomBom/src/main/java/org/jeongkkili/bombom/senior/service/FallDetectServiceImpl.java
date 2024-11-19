package org.jeongkkili.bombom.senior.service;

import java.util.List;

import org.jeongkkili.bombom.member.domain.Member;
import org.jeongkkili.bombom.member.service.NotificationService;
import org.jeongkkili.bombom.member_senior.service.MemberSeniorService;
import org.jeongkkili.bombom.senior.domain.Senior;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;

@Service
@RequiredArgsConstructor
@Transactional
@Slf4j
public class FallDetectServiceImpl implements FallDetectService {

	private final GetSeniorService getSeniorService;
	private final MemberSeniorService memberSeniorService;
	private final NotificationService notificationService;

	@Override
	public void fallDetect(Long seniorId) {
		Senior senior = getSeniorService.getSeniorById(seniorId);
		List<Member> members = memberSeniorService.getMembersBySenior(senior);
		for (Member member : members) {
			notificationService.notifyUser(member.getId(), "낙상 감지", senior.getName() + "님의 낙상이 감지되었습니다.", "Detail", String.valueOf(seniorId));
		}
	}
}
