package org.jeongkkili.bombom.schedule.service.dto;

import java.time.LocalTime;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Getter;

@Getter
@Builder
@AllArgsConstructor
public class ScheduleTodayDto {

	private String memo;
	private String time;
}
