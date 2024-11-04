package org.jeongkkili.bombom.senior.controller;

import java.util.List;

import org.jeongkkili.bombom.core.aop.annotation.RequireJwtoken;
import org.jeongkkili.bombom.core.aop.member.MemberContext;
import org.jeongkkili.bombom.senior.controller.request.RegisterSeniorReq;
import org.jeongkkili.bombom.senior.domain.Senior;
import org.jeongkkili.bombom.senior.service.SeniorService;
import org.jeongkkili.bombom.senior.service.dto.GetSeniorListDto;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import lombok.RequiredArgsConstructor;

@RequiredArgsConstructor
@RestController
@RequestMapping("/api/v1/seniors")
public class SeniorController {

	private final SeniorService seniorService;

	@RequireJwtoken
	@PostMapping("/regist")
	public ResponseEntity<Void> registSenior(@RequestBody List<RegisterSeniorReq> reqList) {
		Long memberId = MemberContext.getMemberId();
		seniorService.registerSenior(reqList, memberId);
		return ResponseEntity.ok().build();
	}

	@RequireJwtoken
	@GetMapping("/list")
	public ResponseEntity<List<GetSeniorListDto>> getSeniorList() {
		Long memberId = MemberContext.getMemberId();
		return ResponseEntity.ok(seniorService.getSeniorList(memberId));
	}

}
