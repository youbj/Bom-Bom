package org.jeongkkili.bombom.member.service;

import org.jeongkkili.bombom.core.firebase.FirebaseService;
import org.jeongkkili.bombom.member.domain.Member;
import org.jeongkkili.bombom.member.domain.MemberFcmToken;
import org.jeongkkili.bombom.member.repository.MemberFcmTokenRepository;
import org.springframework.stereotype.Service;

import jakarta.transaction.Transactional;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;

@Service
@RequiredArgsConstructor
@Transactional
@Slf4j
public class NotificationServiceImpl implements NotificationService {

	private final MemberFcmTokenRepository memberFcmTokenRepository;
	private final FirebaseService firebaseService;
	private final MemberService memberService;

	@Override
	public void notifyUser(Long memberId, String title, String message) {
		Member member = memberService.getMemberById(memberId);
		MemberFcmToken fcmToken = memberFcmTokenRepository.findByMemberId(memberId);
		firebaseService.sendNotification(fcmToken.getFcmToken(), title, message);
	}
}
