package org.jeongkkili.bombom.senior.controller;

import java.util.List;

import org.jeongkkili.bombom.core.aop.annotation.RequireJwtoken;
import org.jeongkkili.bombom.core.aop.member.MemberContext;
import org.jeongkkili.bombom.senior.service.GetSeniorListService;
import org.jeongkkili.bombom.senior.service.dto.GetSeniorListDto;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

import lombok.RequiredArgsConstructor;

@RequiredArgsConstructor
@RestController
public class GetSeniorListController extends SeniorController {

	private final GetSeniorListService getSeniorListService;

	@RequireJwtoken
	@GetMapping("/list")
	public ResponseEntity<List<GetSeniorListDto>> getSeniorList() {
		Long memberId = MemberContext.getMemberId();
		return ResponseEntity.ok(getSeniorListService.getSeniorList(memberId));
	}
}
