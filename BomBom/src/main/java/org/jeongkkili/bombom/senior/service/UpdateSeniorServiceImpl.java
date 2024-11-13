package org.jeongkkili.bombom.senior.service;

import org.jeongkkili.bombom.senior.controller.request.UpdateSeniorReq;
import org.jeongkkili.bombom.senior.domain.Senior;
import org.jeongkkili.bombom.senior.repository.SeniorRepository;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;

@Service
@RequiredArgsConstructor
@Transactional
@Slf4j
public class UpdateSeniorServiceImpl implements UpdateSeniorService {

	private final SeniorRepository seniorRepository;

	@Override
	public void updateSenior(Long seniorId, UpdateSeniorReq req) {
		Senior senior = seniorRepository.getOrThrow(seniorId);
		senior.updateInfo(req.getName(), req.getPhoneNumber(), req.getAddress(), req.getGender(), req.getBirth());
	}
}
