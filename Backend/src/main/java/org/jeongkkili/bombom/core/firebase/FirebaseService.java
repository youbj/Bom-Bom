package org.jeongkkili.bombom.core.firebase;

public interface FirebaseService {

	void sendNotification(String token, String title, String body, String screen);

	void sendNotification(String token, String title, String body, String screen, String seniorId);
}
