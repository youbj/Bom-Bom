package org.jeongkkili.bombom.conversation.service;

import java.util.List;

import org.jeongkkili.bombom.conversation.service.dto.GetConvListDto;
import org.jeongkkili.bombom.senior.domain.Senior;

public interface GetConvService {

	List<GetConvListDto> getConvList(Long memberId, Long seniorId);

	Double getTodayEmotion(Senior senior);
}
