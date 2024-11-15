package org.jeongkkili.bombom.schedule.controller.request;

import java.time.LocalDateTime;

import lombok.AccessLevel;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Getter;
import lombok.NoArgsConstructor;

@Getter
@Builder
@AllArgsConstructor
@NoArgsConstructor(access = AccessLevel.PROTECTED)
public class RegistScheduleReq {

	private Long seniorId;
	private LocalDateTime startAt;
	private LocalDateTime endAt;
	private String memo;
}
