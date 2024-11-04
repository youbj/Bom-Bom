package org.jeongkkili.bombom.senior.service;

import java.util.List;

import org.jeongkkili.bombom.member.domain.Member;
import org.jeongkkili.bombom.member.repository.MemberRepository;
import org.jeongkkili.bombom.member_senior.domain.MemberSenior;
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
public class RegisterSeniorServiceImpl implements RegisterSeniorService {

	private final MemberRepository memberRepository;
	private final MemberSeniorService memberSeniorService;
	private final SeniorRepository seniorRepository;

	@Override
	public void registerSenior(List<RegisterSeniorReq> reqList, Long memberId) {
		Member member = memberRepository.getOrThrow(memberId);
		List<Senior> seniors = reqList.stream()
			.map(req -> Senior.builder()
				.name(req.getName())
				.phoneNumber(req.getPhoneNumber())
				.address(req.getAddress())
				.birth(req.getBirth())
				.gender(req.getGender())
				.build())
			.toList();
		List<Senior> savedSeniors = seniorRepository.saveAll(seniors);

		List<MemberSenior> associations = savedSeniors.stream()
			.map(senior -> MemberSenior.builder()
				.member(member)
				.senior(senior)
				.build())
			.toList();
		memberSeniorService.addAssociation(associations);
	}
}
