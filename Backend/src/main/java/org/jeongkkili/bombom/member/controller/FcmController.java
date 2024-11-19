package org.jeongkkili.bombom.member.controller;

import java.util.Map;

import org.jeongkkili.bombom.core.aop.annotation.RequireJwtoken;
import org.jeongkkili.bombom.core.aop.member.MemberContext;
import org.jeongkkili.bombom.member.service.FcmTokenService;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RestController;

import lombok.RequiredArgsConstructor;

@RequiredArgsConstructor
@RestController
public class FcmController extends MemberController {

	private final FcmTokenService fcmTokenService;

	@RequireJwtoken
	@PostMapping("/fcmtoken")
	public ResponseEntity<Void> registFcmToken(@RequestBody Map<String, String> req) {
		Long memberId = MemberContext.getMemberId();
		String fcmToken = req.get("fcmToken");
		fcmTokenService.saveOrUpdateFcmToken(memberId, fcmToken);
		return ResponseEntity.ok().build();
	}
}
