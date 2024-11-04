package org.jeongkkili.bombom.senior.service;

import java.util.List;

import org.jeongkkili.bombom.senior.service.dto.GetSeniorListDto;

public interface GetSeniorListService {

	List<GetSeniorListDto> getSeniorList(Long memberId);
}
