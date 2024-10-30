package org.jeongkkili.bombom.member.controller;

import org.jeongkkili.bombom.member.controller.request.CheckIdReq;
import org.jeongkkili.bombom.member.controller.request.LoginReq;
import org.jeongkkili.bombom.member.controller.request.RegistMemberReq;
import org.jeongkkili.bombom.member.service.MemberService;
import org.jeongkkili.bombom.member.service.dto.LoginDto;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RestController;

import lombok.RequiredArgsConstructor;

@RequiredArgsConstructor
@RestController
public class AuthController extends MemberController{

	private final MemberService memberService;

	@PostMapping("/regist")
	public ResponseEntity<Void> regist(@RequestBody RegistMemberReq req) {
		memberService.registMember(req);
		return ResponseEntity.ok().build();
	}

	@PostMapping("/login")
	public ResponseEntity<LoginDto> login(@RequestBody LoginReq req) {
		return ResponseEntity.ok(memberService.login(req));
	}

	@PostMapping("/checkid")
	public ResponseEntity<Boolean> checkAlreadyExistId(@RequestBody CheckIdReq req) {
		return ResponseEntity.ok(memberService.checkAlreadyExistId(req.getLoginId()));
	}
}
