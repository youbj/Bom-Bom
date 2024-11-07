package org.jeongkkili.bombom.conversation.service;

import java.util.List;

import org.jeongkkili.bombom.conversation.repository.ConversationRepository;
import org.jeongkkili.bombom.conversation.repository.custom.ConversationRepositoryCustom;
import org.jeongkkili.bombom.conversation.service.dto.GetConvListDto;
import org.jeongkkili.bombom.member.domain.Member;
import org.jeongkkili.bombom.member.service.MemberService;
import org.jeongkkili.bombom.member_senior.service.MemberSeniorService;
import org.jeongkkili.bombom.senior.domain.Senior;
import org.jeongkkili.bombom.senior.service.GetSeniorService;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;

@Service
@RequiredArgsConstructor
@Transactional
@Slf4j
public class GetConvServiceImpl implements GetConvService {

	private final GetSeniorService getSeniorService;
	private final MemberService memberService;
	private final MemberSeniorService memberSeniorService;
	private final ConversationRepository convRepository;
	private final ConversationRepositoryCustom convRepositoryCustom;

	@Override
	public List<GetConvListDto> getConvList(Long memberId, Long seniorId) {
		Member member = memberService.getMemberById(memberId);
		Senior senior = getSeniorService.getSeniorById(seniorId);
		memberSeniorService.checkAssociation(member, senior);
		return convRepositoryCustom.getConversationList(senior);
	}
}
