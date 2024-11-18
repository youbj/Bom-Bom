package org.jeongkkili.bombom.member.service;

public interface NotificationService {

	void notifyUser(Long memberId, String title, String message, String screen);
}
