package org.jeongkkili.bombom.core.config.firebase;

import java.io.InputStream;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Configuration;

import com.google.auth.oauth2.GoogleCredentials;
import com.google.firebase.FirebaseApp;
import com.google.firebase.FirebaseOptions;

import jakarta.annotation.PostConstruct;

@Configuration
public class FirebaseConfig {

	@Value("${firebase.config.file}")
	private String firebaseConfigPath;

	@PostConstruct
	public void initialize() {
		try {
			InputStream serviceAccount = getClass().getClassLoader().getResourceAsStream(firebaseConfigPath);
			FirebaseOptions options = FirebaseOptions.builder()
				.setCredentials(GoogleCredentials.fromStream(serviceAccount))
				.build();
			if (FirebaseApp.getApps().isEmpty()) {
				FirebaseApp.initializeApp(options);
				// System.out.println("FirebaseApp has been initialized");
			}
		} catch (Exception e) {
			e.printStackTrace();
		}
	}
}
