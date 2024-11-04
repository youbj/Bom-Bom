package org.jeongkkili.bombom.member_senior.controller;

import org.jeongkkili.bombom.core.aop.annotation.RequireJwtoken;
import org.jeongkkili.bombom.core.aop.member.MemberContext;
import org.jeongkkili.bombom.member_senior.controller.request.AddAssociationReq;
import org.jeongkkili.bombom.member_senior.service.MemberSeniorService;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import lombok.RequiredArgsConstructor;

@RequiredArgsConstructor
@RestController
@RequestMapping("/api/v1/membersenior")
public class MemberSeniorController {

	private final MemberSeniorService memberSeniorService;

	// @RequireJwtoken
	// @PostMapping("/add")
	// public ResponseEntity<Void> addAssociation(@RequestBody AddAssociationReq req) {
	// 	Long memberId = MemberContext.getMemberId();
	// 	// memberSeniorService.addAssociation(memberId, req.getSeniorId());
	// 	return ResponseEntity.ok().build();
	// }
}
