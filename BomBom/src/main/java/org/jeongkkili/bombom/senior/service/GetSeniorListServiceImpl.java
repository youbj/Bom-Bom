package org.jeongkkili.bombom.senior.service;

import java.util.List;

import org.jeongkkili.bombom.member.domain.Member;
import org.jeongkkili.bombom.member.repository.MemberRepository;
import org.jeongkkili.bombom.senior.repository.custom.SeniorRepositoryCustom;
import org.jeongkkili.bombom.senior.service.dto.GetSeniorListDto;
import org.springframework.stereotype.Service;

import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;

@Service
@RequiredArgsConstructor
@Slf4j
public class GetSeniorListServiceImpl implements GetSeniorListService {

	private final MemberRepository memberRepository;
	private final SeniorRepositoryCustom seniorRepositoryCustom;

	@Override
	public List<GetSeniorListDto> getSeniorList(Long memberId) {
		Member member = memberRepository.getOrThrow(memberId);
		return seniorRepositoryCustom.getSeniorList(member);
	}
}
