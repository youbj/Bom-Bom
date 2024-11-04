package org.jeongkkili.bombom.schedule.controller;

import org.jeongkkili.bombom.schedule.controller.request.RegistScheduleReq;
import org.jeongkkili.bombom.schedule.service.RegistScheduleService;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RestController;

import lombok.RequiredArgsConstructor;

@RequiredArgsConstructor
@RestController
public class RegistScheduleController extends ScheduleController {

	private final RegistScheduleService registScheduleService;

	@PostMapping("/regist")
	public ResponseEntity<Void> registSchedule(@RequestBody RegistScheduleReq req) {
		registScheduleService.registSchedule(req);
		return ResponseEntity.ok().build();
	}
}
