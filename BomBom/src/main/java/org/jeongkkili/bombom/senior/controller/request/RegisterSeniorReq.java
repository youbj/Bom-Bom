package org.jeongkkili.bombom.senior.controller.request;

import java.util.Date;

import org.jeongkkili.bombom.senior.domain.Gender;

import lombok.AccessLevel;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Getter;
import lombok.NoArgsConstructor;

@Getter
@Builder
@AllArgsConstructor
@NoArgsConstructor(access = AccessLevel.PROTECTED)
public class RegisterSeniorReq {

	private String loginId;
	private String name;
	private String phoneNumber;
	private String address;
	private Date birth;
	private Gender gender;
}
