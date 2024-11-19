package org.jeongkkili.bombom.member.service;

public interface FcmTokenService {

	void saveOrUpdateFcmToken(Long memberId, String fcmToken);
}
