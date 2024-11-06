package org.jeongkkili.bombom.member.service;

import org.jeongkkili.bombom.member.service.dto.ReissueDto;

public interface ReissueTokenService {

	ReissueDto reissueToken(String refreshToken);
}
