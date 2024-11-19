package org.jeongkkili.bombom.schedule.controller;

import org.jeongkkili.bombom.core.aop.annotation.RequireJwtoken;
import org.jeongkkili.bombom.core.aop.member.MemberContext;
import org.jeongkkili.bombom.schedule.controller.request.UpdateScheduleReq;
import org.jeongkkili.bombom.schedule.service.UpdateScheduleService;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.PatchMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import lombok.RequiredArgsConstructor;

@RequiredArgsConstructor
@RestController
public class UpdateScheduleController extends ScheduleController {

	private final UpdateScheduleService updateScheduleService;

	@RequireJwtoken
	@PatchMapping("/update")
	public ResponseEntity<Void> updateSchedule(@RequestParam("schedule-id") Long scheduleId, @RequestBody UpdateScheduleReq req) {
		Long memberId = MemberContext.getMemberId();
		updateScheduleService.updateSchedule(scheduleId, memberId, req);
		return ResponseEntity.ok().build();
	}
}
