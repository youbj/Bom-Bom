package org.jeongkkili.bombom.member.service;

import org.jeongkkili.bombom.core.jwt.JwtProvider;
import org.jeongkkili.bombom.core.jwt.dto.Jwtoken;
import org.jeongkkili.bombom.member.service.dto.ReissueDto;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;

@Service
@RequiredArgsConstructor
@Transactional
@Slf4j
public class ReissueTokenServiceImpl implements ReissueTokenService {

	private final JwtProvider jwtProvider;

	@Override
	public ReissueDto reissueToken(String refreshToken) {
		Long memberId = jwtProvider.getMemberIdFromRefreshToken(refreshToken);
		jwtProvider.deleteRefreshToken(refreshToken);
		Jwtoken newToken = jwtProvider.createToken(memberId);
		return ReissueDto.builder()
			.accessToken(newToken.getAccessToken())
			.refreshToken(newToken.getRefreshToken())
			.build();
	}
}
