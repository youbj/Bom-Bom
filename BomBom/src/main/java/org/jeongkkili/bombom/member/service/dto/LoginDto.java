package org.jeongkkili.bombom.member.service.dto;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Getter;

@Getter
@Builder
@AllArgsConstructor
public class LoginDto {

	private String loginId;
	private String name;
	private String phoneNumber;
	private String accessToken;
	private String refreshToken;

}
