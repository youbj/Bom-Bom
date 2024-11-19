package org.jeongkkili.bombom.senior.controller;

import java.util.List;

import org.jeongkkili.bombom.core.aop.annotation.RequireJwtoken;
import org.jeongkkili.bombom.core.aop.member.MemberContext;
import org.jeongkkili.bombom.senior.service.GetSeniorService;
import org.jeongkkili.bombom.senior.service.dto.GetSeniorDetailDto;
import org.jeongkkili.bombom.senior.service.dto.GetSeniorListDto;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import lombok.RequiredArgsConstructor;

@RequiredArgsConstructor
@RestController
public class GetSeniorController extends SeniorController {

	private final GetSeniorService getSeniorService;

	@RequireJwtoken
	@GetMapping("/list")
	public ResponseEntity<List<GetSeniorListDto>> getSeniorList() {
		Long memberId = MemberContext.getMemberId();
		return ResponseEntity.ok(getSeniorService.getSeniorList(memberId));
	}

	@RequireJwtoken
	@GetMapping("/detail")
	public ResponseEntity<GetSeniorDetailDto> getSeniorDetail(@RequestParam("senior-id") Long seniorId) {
		Long memberId = MemberContext.getMemberId();
		return ResponseEntity.ok(getSeniorService.getSeniorDetail(memberId, seniorId));
	}
}
