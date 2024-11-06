package org.jeongkkili.bombom.member.service;

import org.jeongkkili.bombom.member.domain.Member;
import org.jeongkkili.bombom.member.domain.MemberFcmToken;
import org.jeongkkili.bombom.member.repository.MemberFcmTokenRepository;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;

@Service
@RequiredArgsConstructor
@Transactional
@Slf4j
public class FcmTokenServiceImpl implements FcmTokenService {

	private final MemberService memberService;
	private final MemberFcmTokenRepository fcmTokenRepository;

	@Override
	public void saveOrUpdateFcmToken(Long memberId, String fcmToken) {
		MemberFcmToken existingToken = fcmTokenRepository.findByMemberId(memberId);

		if (existingToken != null) {
			existingToken.updateFcmToken(fcmToken);
		} else {
			Member member = memberService.getMemberById(memberId);
			MemberFcmToken newToken = MemberFcmToken.builder()
				.member(member)
				.fcmToken(fcmToken)
				.build();
			fcmTokenRepository.save(newToken);
		}
	}
}
