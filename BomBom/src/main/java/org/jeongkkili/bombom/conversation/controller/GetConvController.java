package org.jeongkkili.bombom.conversation.controller;

import java.util.List;

import org.jeongkkili.bombom.conversation.service.GetConvService;
import org.jeongkkili.bombom.conversation.service.dto.GetConvListDto;
import org.jeongkkili.bombom.core.aop.annotation.RequireJwtoken;
import org.jeongkkili.bombom.core.aop.member.MemberContext;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import lombok.RequiredArgsConstructor;

@RequiredArgsConstructor
@RestController
public class GetConvController extends ConversationController {

	private final GetConvService getConvService;

	@RequireJwtoken
	@GetMapping("/list")
	public ResponseEntity<List<GetConvListDto>> getConvList(@RequestParam("senior-id") Long seniorId) {
		Long memberId = MemberContext.getMemberId();
		return ResponseEntity.ok(getConvService.getConvList(memberId, seniorId));
	}
}
