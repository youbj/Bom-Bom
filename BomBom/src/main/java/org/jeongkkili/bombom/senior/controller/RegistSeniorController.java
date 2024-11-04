package org.jeongkkili.bombom.senior.controller;

import java.util.List;

import org.jeongkkili.bombom.core.aop.annotation.RequireJwtoken;
import org.jeongkkili.bombom.core.aop.member.MemberContext;
import org.jeongkkili.bombom.senior.controller.request.RegisterSeniorReq;
import org.jeongkkili.bombom.senior.service.RegisterSeniorService;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RestController;

import lombok.RequiredArgsConstructor;

@RequiredArgsConstructor
@RestController
public class RegistSeniorController extends SeniorController {

	private final RegisterSeniorService registerSeniorService;

	@RequireJwtoken
	@PostMapping("/regist")
	public ResponseEntity<Void> registSenior(@RequestBody List<RegisterSeniorReq> reqList) {
		Long memberId = MemberContext.getMemberId();
		registerSeniorService.registerSenior(reqList, memberId);
		return ResponseEntity.ok().build();
	}
}
