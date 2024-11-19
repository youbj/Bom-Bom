package org.jeongkkili.bombom.conversation.service.dto;

import java.time.LocalDate;
import java.time.LocalTime;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Getter;

@Getter
@Builder
@AllArgsConstructor
public class GetConvListDto {

	private Double avgScore;
	private LocalDate startDate;
	private LocalTime endTime;
}
