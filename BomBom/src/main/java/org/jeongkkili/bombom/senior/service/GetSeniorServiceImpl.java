package org.jeongkkili.bombom.senior.service;

import java.util.List;

import org.jeongkkili.bombom.member.domain.Member;
import org.jeongkkili.bombom.member.service.MemberService;
import org.jeongkkili.bombom.member_senior.service.MemberSeniorService;
import org.jeongkkili.bombom.senior.domain.Senior;
import org.jeongkkili.bombom.senior.repository.SeniorRepository;
import org.jeongkkili.bombom.senior.repository.custom.SeniorRepositoryCustom;
import org.jeongkkili.bombom.senior.service.dto.GetSeniorDetailDto;
import org.jeongkkili.bombom.senior.service.dto.GetSeniorListDto;
import org.springframework.stereotype.Service;

import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;

@Service
@RequiredArgsConstructor
@Slf4j
public class GetSeniorServiceImpl implements GetSeniorService {

	private final SeniorRepository seniorRepository;
	private final MemberService memberService;
	private final MemberSeniorService memberSeniorService;
	private final SeniorRepositoryCustom seniorRepositoryCustom;

	@Override
	public Senior getSeniorById(Long seniorId) {
		return seniorRepository.getOrThrow(seniorId);
	}

	@Override
	public List<GetSeniorListDto> getSeniorList(Long memberId) {
		Member member = memberService.getMemberById(memberId);
		return seniorRepositoryCustom.getSeniorList(member);
	}

	@Override
	public GetSeniorDetailDto getSeniorDetail(Long memberId, Long seniorId) {
		Member member = memberService.getMemberById(memberId);
		Senior senior = seniorRepository.getOrThrow(seniorId);
		memberSeniorService.checkAssociation(member, senior);
		return GetSeniorDetailDto.toDto(senior);
	}
}
