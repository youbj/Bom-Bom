package org.jeongkkili.bombom.member.service.dto;

import org.jeongkkili.bombom.member.domain.Type;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Getter;

@Getter
@Builder
@AllArgsConstructor
public class ReissueDto {

	private Type type;
	private String accessToken;
	private String refreshToken;
}
