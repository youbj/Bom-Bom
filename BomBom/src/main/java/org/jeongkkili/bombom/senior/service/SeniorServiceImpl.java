package org.jeongkkili.bombom.senior.service;

import java.util.List;

import org.jeongkkili.bombom.member.domain.Member;
import org.jeongkkili.bombom.member.repository.MemberRepository;
import org.jeongkkili.bombom.member_senior.service.MemberSeniorService;
import org.jeongkkili.bombom.senior.controller.request.RegisterSeniorReq;
import org.jeongkkili.bombom.senior.domain.Senior;
import org.jeongkkili.bombom.senior.repository.SeniorRepository;
import org.jeongkkili.bombom.senior.repository.custom.SeniorRepositoryCustom;
import org.jeongkkili.bombom.senior.service.dto.GetSeniorListDto;
import org.springframework.stereotype.Service;

import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;

@Service
@RequiredArgsConstructor
@Slf4j
public class SeniorServiceImpl implements SeniorService {

	private final MemberRepository memberRepository;
	private final MemberSeniorService memberSeniorService;
	private final SeniorRepository seniorRepository;
	private final SeniorRepositoryCustom seniorRepositoryCustom;

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

	@Override
	public List<GetSeniorListDto> getSeniorList(Long memberId) {
		Member member = memberRepository.getOrThrow(memberId);
		return seniorRepositoryCustom.getSeniorList(member);
	}
}
