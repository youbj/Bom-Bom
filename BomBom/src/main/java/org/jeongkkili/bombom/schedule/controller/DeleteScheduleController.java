package org.jeongkkili.bombom.schedule.controller;

import org.jeongkkili.bombom.core.aop.annotation.RequireJwtoken;
import org.jeongkkili.bombom.core.aop.member.MemberContext;
import org.jeongkkili.bombom.schedule.service.DeleteScheduleService;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import lombok.RequiredArgsConstructor;

@RequiredArgsConstructor
@RestController
public class DeleteScheduleController extends ScheduleController {

	private final DeleteScheduleService deleteScheduleService;

	@RequireJwtoken
	@DeleteMapping("/delete")
	public ResponseEntity<Void> deleteSchedule(@RequestParam("schedule-id") Long scheduleId) {
		Long memberId = MemberContext.getMemberId();
		deleteScheduleService.deleteSchedule(memberId, scheduleId);
		return ResponseEntity.ok().build();
	}
}
