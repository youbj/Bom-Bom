package org.jeongkkili.bombom.senior.service;

import org.jeongkkili.bombom.senior.domain.Senior;
import org.jeongkkili.bombom.senior.repository.SeniorRepository;
import org.springframework.stereotype.Service;

import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;

@Service
@RequiredArgsConstructor
@Slf4j
public class GetSeniorServiceImpl implements GetSeniorService {

	private final SeniorRepository seniorRepository;

	@Override
	public Senior getSeniorById(Long seniorId) {
		return seniorRepository.getOrThrow(seniorId);
	}
}
