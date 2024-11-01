package org.jeongkkili.bombom.senior.service;

import org.jeongkkili.bombom.member_senior.service.MemberSeniorService;
import org.jeongkkili.bombom.senior.controller.request.RegisterSeniorReq;
import org.jeongkkili.bombom.senior.domain.Senior;
import org.jeongkkili.bombom.senior.repository.SeniorRepository;
import org.springframework.stereotype.Service;

import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;

@Service
@RequiredArgsConstructor
@Slf4j
public class SeniorServiceImpl implements SeniorService {

	private final MemberSeniorService memberSeniorService;
	private final SeniorRepository seniorRepository;

	@Override
	public void registerSenior(RegisterSeniorReq req, Long memberId) {
		Senior senior =  seniorRepository.save(Senior.builder()
				.name(req.getName())
				.phoneNumber(req.getPhoneNumber())
				.address(req.getAddress())
				.birth(req.getBirth())
				.gender(req.getGender())
			.build());
		memberSeniorService.addAssociation(memberId, senior.getId());
	}
}
