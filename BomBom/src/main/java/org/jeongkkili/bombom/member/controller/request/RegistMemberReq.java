package org.jeongkkili.bombom.member.controller.request;

import lombok.AccessLevel;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Getter;
import lombok.NoArgsConstructor;

@Getter
@Builder
@AllArgsConstructor
@NoArgsConstructor(access = AccessLevel.PROTECTED)
public class RegistMemberReq {

	private String loginId;
	private String password;
	private String name;
	private String phoneNumber;
	private String type;
}
