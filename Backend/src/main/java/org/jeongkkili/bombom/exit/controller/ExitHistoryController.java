package org.jeongkkili.bombom.exit.controller;

import org.jeongkkili.bombom.exit.controller.request.ExitReq;
import org.jeongkkili.bombom.exit.service.ExitHistoryService;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import lombok.RequiredArgsConstructor;

@RequiredArgsConstructor
@RestController
@RequestMapping("/api/v1/exit")
public class ExitHistoryController {

	private final ExitHistoryService exitHistoryService;

	@PostMapping("/start")
	public ResponseEntity<Void> addExitHistory(@RequestBody ExitReq req) {
		exitHistoryService.addExitHistory(req.getSeniorId());
		return ResponseEntity.ok().build();
	}
}
