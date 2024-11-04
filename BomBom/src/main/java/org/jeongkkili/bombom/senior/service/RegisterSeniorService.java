package org.jeongkkili.bombom.senior.service;

import java.util.List;

import org.jeongkkili.bombom.senior.controller.request.RegisterSeniorReq;

public interface RegisterSeniorService {

	void registerSenior(List<RegisterSeniorReq> reqList, Long memberId);
}
