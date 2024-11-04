package org.jeongkkili.bombom.schedule.service.dto;

import java.time.LocalDateTime;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Getter;

@Getter
@Builder
@AllArgsConstructor
public class ScheduleMonthDto {

	private Long scheduleId;
	private String memo;
	private LocalDateTime date;
}
