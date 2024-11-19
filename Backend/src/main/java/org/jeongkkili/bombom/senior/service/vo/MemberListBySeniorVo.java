package org.jeongkkili.bombom.senior.service.vo;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Getter;

@Getter
@Builder
@AllArgsConstructor
public class MemberListBySeniorVo {

	private String memberName;
	private String memberPhoneNumber;
}
