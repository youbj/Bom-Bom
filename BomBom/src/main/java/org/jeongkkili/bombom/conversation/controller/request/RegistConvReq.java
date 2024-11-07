package org.jeongkkili.bombom.conversation.controller.request;

import lombok.AccessLevel;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Getter;
import lombok.NoArgsConstructor;

@Getter
@Builder
@AllArgsConstructor
@NoArgsConstructor(access = AccessLevel.PROTECTED)
public class RegistConvReq {

	private Long seniorId;
	private String summary;
	private Double emotion;
}
