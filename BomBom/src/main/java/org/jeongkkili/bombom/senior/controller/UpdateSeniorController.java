package org.jeongkkili.bombom.senior.controller;

import org.jeongkkili.bombom.core.aop.annotation.RequireJwtoken;
import org.jeongkkili.bombom.core.aop.member.MemberContext;
import org.jeongkkili.bombom.senior.controller.request.UpdateSeniorReq;
import org.jeongkkili.bombom.senior.service.UpdateSeniorService;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.PatchMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import lombok.RequiredArgsConstructor;

@RequiredArgsConstructor
@RestController
public class UpdateSeniorController extends SeniorController {

	private final UpdateSeniorService updateSeniorService;

	@RequireJwtoken
	@PatchMapping("/update")
	public ResponseEntity<Void> updateSenior(@RequestParam("senior-id") Long seniorId, @RequestBody UpdateSeniorReq req) {
		Long memberId = MemberContext.getMemberId();
		updateSeniorService.updateSenior(seniorId, memberId, req);
		return ResponseEntity.ok().build();
	}
}
