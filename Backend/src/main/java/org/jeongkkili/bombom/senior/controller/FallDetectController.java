package org.jeongkkili.bombom.senior.controller;

import org.jeongkkili.bombom.senior.service.FallDetectService;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import lombok.RequiredArgsConstructor;

@RequiredArgsConstructor
@RestController
public class FallDetectController extends SeniorController {

	private final FallDetectService fallDetectService;

	@PostMapping("/detect")
	public ResponseEntity<Void> fallDetect(@RequestParam("senior-id") Long seniorId) {
		fallDetectService.fallDetect(seniorId);
		return ResponseEntity.ok().build();
	}
}
