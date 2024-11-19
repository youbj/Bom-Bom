package org.jeongkkili.bombom.core.jwt.dto;

import lombok.Builder;
import lombok.Getter;

@Getter
@Builder
public class Jwtoken {

	private String accessToken;
	private String refreshToken;
}
