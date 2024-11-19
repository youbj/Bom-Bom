package org.jeongkkili.bombom.senior.service;

import org.jeongkkili.bombom.member.domain.Member;
import org.jeongkkili.bombom.member.service.MemberService;
import org.jeongkkili.bombom.member_senior.service.MemberSeniorService;
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
public class DeleteSeniorServiceImpl implements DeleteSeniorService {

	private final MemberService memberService;
	private final MemberSeniorService memberSeniorService;
	private final SeniorRepository seniorRepository;

	@Override
	public void deleteSenior(Long memberId, Long seniorId) {
		Member member = memberService.getMemberById(memberId);
		Senior senior = seniorRepository.getOrThrow(seniorId);
		memberSeniorService.checkAssociation(member ,senior);
		senior.getMemberSeniors().clear();
		seniorRepository.delete(senior);
	}
}
