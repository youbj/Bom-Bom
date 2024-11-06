package org.jeongkkili.bombom.member.service.dto;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Getter;

@Getter
@Builder
@AllArgsConstructor
public class ReissueDto {

	private String accessToken;
	private String refreshToken;
}
