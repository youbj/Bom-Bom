package org.jeongkkili.bombom.senior.service;

import java.util.List;

import org.jeongkkili.bombom.senior.controller.request.RegisterSeniorReq;
import org.jeongkkili.bombom.senior.service.dto.GetSeniorListDto;

public interface SeniorService {

	void registerSenior(RegisterSeniorReq req, Long memberId);

	List<GetSeniorListDto> getSeniorList(Long memberId);
}
