package org.jeongkkili.bombom.qualify.controller;

import org.jeongkkili.bombom.qualify.controller.request.VerifyReq;
import org.jeongkkili.bombom.qualify.service.QualifyService;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RestController;

import lombok.RequiredArgsConstructor;

@RequiredArgsConstructor
@RestController
public class QualifyNumController extends QualifyController {

	private final QualifyService qualifyService;

	@PostMapping("/verify")
	public ResponseEntity<Boolean> verifyQualifyNum(@RequestBody VerifyReq req) {
		return ResponseEntity.ok(qualifyService.verifyQualifyNumber(req.getQualifyNumber()));
	}
}
