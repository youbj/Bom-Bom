package org.jeongkkili.bombom.member.controller;

import java.util.List;
import java.util.Map;

import org.jeongkkili.bombom.core.aop.annotation.RequireJwtoken;
import org.jeongkkili.bombom.core.aop.member.MemberContext;
import org.jeongkkili.bombom.member.controller.request.ApproveRequestReq;
import org.jeongkkili.bombom.member.domain.ApproveRequest;
import org.jeongkkili.bombom.member.service.ApproveRequestService;
import org.jeongkkili.bombom.member.service.dto.ApproveRequestDto;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RestController;

import lombok.RequiredArgsConstructor;

@RequiredArgsConstructor
@RestController
public class ApproveRequestController extends MemberController {

	private final ApproveRequestService approveRequestService;

	@RequireJwtoken
	@PostMapping("/approve/request")
	public ResponseEntity<Void> addApproveRequest(@RequestBody ApproveRequestReq req) {
		Long memberId = MemberContext.getMemberId();
		approveRequestService.addApproveRequest(req, memberId);
		return ResponseEntity.ok().build();
	}

	@RequireJwtoken
	@GetMapping("/approve/list")
	public ResponseEntity<List<ApproveRequestDto>> getApproveRequests() {
		Long memberId = MemberContext.getMemberId();
		return ResponseEntity.ok(approveRequestService.getApproveRequests(memberId));
	}

	@RequireJwtoken
	@PostMapping("/approve")
	public ResponseEntity<Void> approveRequest(@RequestBody Map<String, Long> req) {
		Long memberId = MemberContext.getMemberId();
		approveRequestService.approveRequest(req.get("id"), memberId);
		return ResponseEntity.ok().build();
	}

	@RequireJwtoken
	@PostMapping("/reject")
	public ResponseEntity<Void> rejectRequest(@RequestBody Map<String, Long> req) {
		Long memberId = MemberContext.getMemberId();
		approveRequestService.rejectRequest(req.get("id"), memberId);
		return ResponseEntity.ok().build();
	}
}
