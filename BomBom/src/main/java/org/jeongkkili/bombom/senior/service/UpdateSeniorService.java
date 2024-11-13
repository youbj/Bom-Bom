package org.jeongkkili.bombom.senior.service;

import org.jeongkkili.bombom.senior.controller.request.UpdateSeniorReq;

public interface UpdateSeniorService {

	void updateSenior(Long seniorId, UpdateSeniorReq req);
}
