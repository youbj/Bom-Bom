package org.jeongkkili.bombom.senior.controller;

import org.jeongkkili.bombom.core.aop.annotation.RequireJwtoken;
import org.jeongkkili.bombom.core.aop.member.MemberContext;
import org.jeongkkili.bombom.senior.controller.request.RegisterSeniorReq;
import org.jeongkkili.bombom.senior.domain.Senior;
import org.jeongkkili.bombom.senior.service.SeniorService;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import lombok.RequiredArgsConstructor;

@RequiredArgsConstructor
@RestController
@RequestMapping("/api/v1/seniors")
public class SeniorController {

	private final SeniorService seniorService;

	@RequireJwtoken
	@PostMapping("/regist")
	public ResponseEntity<Void> registSenior(@RequestBody RegisterSeniorReq req) {
		Long memberId = MemberContext.getMemberId();
		seniorService.registerSenior(req, memberId);
		return ResponseEntity.ok().build();
	}
}
