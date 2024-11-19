package org.jeongkkili.bombom.senior.controller;

import org.jeongkkili.bombom.core.aop.annotation.RequireJwtoken;
import org.jeongkkili.bombom.core.aop.member.MemberContext;
import org.jeongkkili.bombom.senior.service.DeleteSeniorService;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import lombok.RequiredArgsConstructor;

@RequiredArgsConstructor
@RestController
public class DeleteSeniorController extends SeniorController {

	private final DeleteSeniorService deleteSeniorService;

	@RequireJwtoken
	@DeleteMapping("/delete")
	public ResponseEntity<Void> deleteSenior(@RequestParam("senior-id") Long seniorId) {
		Long memberId = MemberContext.getMemberId();
		deleteSeniorService.deleteSenior(memberId, seniorId);
		return ResponseEntity.ok().build();
	}
}
