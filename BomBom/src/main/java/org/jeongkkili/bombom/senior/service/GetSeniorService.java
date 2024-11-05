package org.jeongkkili.bombom.senior.service;

import java.util.List;

import org.jeongkkili.bombom.senior.domain.Senior;
import org.jeongkkili.bombom.senior.service.dto.GetSeniorDetailDto;
import org.jeongkkili.bombom.senior.service.dto.GetSeniorListDto;

public interface GetSeniorService {

	Senior getSeniorById(Long seniorId);

	List<GetSeniorListDto> getSeniorList(Long memberId);

	GetSeniorDetailDto getSeniorDetail(Long memberId, Long seniorId);
}
