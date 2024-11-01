package org.jeongkkili.bombom.senior.service;

import org.jeongkkili.bombom.senior.controller.request.RegisterSeniorReq;
import org.jeongkkili.bombom.senior.domain.Senior;

public interface SeniorService {

	void registerSenior(RegisterSeniorReq req, Long memberId);
}
