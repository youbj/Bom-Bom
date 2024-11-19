package org.jeongkkili.bombom.senior.service;

import org.jeongkkili.bombom.member.domain.Member;
import org.jeongkkili.bombom.member.service.MemberService;
import org.jeongkkili.bombom.member_senior.service.MemberSeniorService;
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

	private final MemberService memberService;
	private final SeniorRepository seniorRepository;
	private final MemberSeniorService memberSeniorService;

	@Override
	public void updateSenior(Long seniorId, Long memberId, UpdateSeniorReq req) {
		Senior senior = seniorRepository.getOrThrow(seniorId);
		Member member = memberService.getMemberById(memberId);
		memberSeniorService.checkAssociation(member, senior);
		senior.updateInfo(req.getName(), req.getPhoneNumber(), req.getAddress(), req.getGender(), req.getBirth());
	}
}
