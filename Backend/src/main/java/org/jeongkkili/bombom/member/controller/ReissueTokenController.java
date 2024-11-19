package org.jeongkkili.bombom.member.controller;

import org.jeongkkili.bombom.member.controller.request.ReissueReq;
import org.jeongkkili.bombom.member.service.ReissueTokenService;
import org.jeongkkili.bombom.member.service.dto.ReissueDto;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RestController;

import lombok.RequiredArgsConstructor;

@RequiredArgsConstructor
@RestController
public class ReissueTokenController extends MemberController {

	private final ReissueTokenService reissueTokenService;

	@PostMapping("/reissue")
	public ResponseEntity<ReissueDto> reissueToken(@RequestBody ReissueReq req) {
		return ResponseEntity.ok(reissueTokenService.reissueToken(req.getRefreshToken()));
	}
}
