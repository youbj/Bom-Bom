package org.jeongkkili.bombom.senior.controller;

import org.jeongkkili.bombom.member_senior.service.MemberSeniorService;
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

	@PostMapping("/regist")
	public ResponseEntity<Void> registSenior(@RequestBody RegisterSeniorReq req) {
		seniorService.registerSenior(Senior.builder()
			.name(req.getName())
			.phoneNumber(req.getPhoneNumber())
			.address(req.getAddress())
			.birth(req.getBirth())
			.gender(req.getGender())
			.build(), req.getLoginId());
		return ResponseEntity.ok().build();
	}
}
