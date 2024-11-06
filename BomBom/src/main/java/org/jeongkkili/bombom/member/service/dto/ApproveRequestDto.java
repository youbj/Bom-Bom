package org.jeongkkili.bombom.member.service.dto;

import java.time.LocalDateTime;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Getter;

@Getter
@Builder
@AllArgsConstructor
public class ApproveRequestDto {

	private Long id;
	private String familyName;
	private String seniorName;
	private LocalDateTime createdAt;
}
