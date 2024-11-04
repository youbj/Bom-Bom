package org.jeongkkili.bombom.schedule.controller;

import java.util.List;

import org.jeongkkili.bombom.core.aop.annotation.RequireJwtoken;
import org.jeongkkili.bombom.core.aop.member.MemberContext;
import org.jeongkkili.bombom.schedule.service.GetScheduleListService;
import org.jeongkkili.bombom.schedule.service.dto.ScheduleMonthDto;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import lombok.RequiredArgsConstructor;

@RequiredArgsConstructor
@RestController
public class GetScheduleListController extends ScheduleController {

	private final GetScheduleListService getScheduleListService;

	@RequireJwtoken
	@GetMapping
	public ResponseEntity<List<ScheduleMonthDto>> getScheduleList(
		@RequestParam("senior-id") Long seniorId,
		@RequestParam("year") Integer year,
		@RequestParam("month") Integer month
	) {
		Long memberId = MemberContext.getMemberId();
		return ResponseEntity.ok(getScheduleListService.getMonthlyScheduleList(seniorId, year, month, memberId));
	}
}
