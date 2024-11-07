package org.jeongkkili.bombom.conversation.service;

import java.util.List;

import org.jeongkkili.bombom.conversation.service.dto.GetConvListDto;

public interface GetConvService {

	List<GetConvListDto> getConvList(Long memberId, Long seniorId);
}
