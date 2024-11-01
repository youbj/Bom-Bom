package org.jeongkkili.bombom.member_senior.service;

import org.jeongkkili.bombom.member.domain.Member;
import org.jeongkkili.bombom.member.repository.MemberRepository;
import org.jeongkkili.bombom.member_senior.domain.MemberSenior;
import org.jeongkkili.bombom.member_senior.repository.MemberSeniorRepository;
import org.jeongkkili.bombom.senior.domain.Senior;
import org.jeongkkili.bombom.senior.repository.SeniorRepository;
import org.springframework.stereotype.Service;

import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;

@Service
@RequiredArgsConstructor
@Slf4j
public class MemberSeniorServiceImpl implements MemberSeniorService {

	private final MemberSeniorRepository memberSeniorRepository;
	private final MemberRepository memberRepository;
	private final SeniorRepository seniorRepository;

	@Override
	public void addAssociation(Long memberId, Long seniorId) {
		Member member = memberRepository.getOrThrow(memberId);
		Senior senior = seniorRepository.getOrThrow(seniorId);
		memberSeniorRepository.save(MemberSenior.builder().member(member).senior(senior).build());
	}
}
