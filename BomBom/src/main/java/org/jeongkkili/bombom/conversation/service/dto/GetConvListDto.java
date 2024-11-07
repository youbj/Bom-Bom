package org.jeongkkili.bombom.conversation.service.dto;

import java.time.LocalDateTime;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Getter;

@Getter
@Builder
@AllArgsConstructor
public class GetConvListDto {

	private Double emotion;
	private LocalDateTime createdAt;
}
