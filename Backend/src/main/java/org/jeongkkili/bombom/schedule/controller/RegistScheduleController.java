package org.jeongkkili.bombom.schedule.controller;

import org.jeongkkili.bombom.core.aop.annotation.RequireJwtoken;
import org.jeongkkili.bombom.core.aop.member.MemberContext;
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

	@RequireJwtoken
	@PostMapping("/regist")
	public ResponseEntity<Void> registSchedule(@RequestBody RegistScheduleReq req) {
		Long memberId = MemberContext.getMemberId();
		registScheduleService.registSchedule(req, memberId);
		return ResponseEntity.ok().build();
	}
}
