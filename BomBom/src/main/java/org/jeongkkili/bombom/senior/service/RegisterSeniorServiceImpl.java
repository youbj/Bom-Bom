package org.jeongkkili.bombom.senior.service;

import java.util.List;

import org.jeongkkili.bombom.member.domain.Member;
import org.jeongkkili.bombom.member.service.MemberService;
import org.jeongkkili.bombom.member_senior.domain.MemberSenior;
import org.jeongkkili.bombom.member_senior.service.MemberSeniorService;
import org.jeongkkili.bombom.senior.controller.request.RegisterSeniorReq;
import org.jeongkkili.bombom.senior.domain.Senior;
import org.jeongkkili.bombom.senior.repository.SeniorRepository;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;

@Service
@RequiredArgsConstructor
@Transactional
@Slf4j
public class RegisterSeniorServiceImpl implements RegisterSeniorService {

	private final MemberService memberService;
	private final MemberSeniorService memberSeniorService;
	private final SeniorRepository seniorRepository;

	@Override
	public void registerSenior(List<RegisterSeniorReq> reqList, Long memberId) {
		Member member = memberService.getMemberById(memberId);
		List<Senior> seniors = reqList.stream()
			.map(req -> Senior.builder()
				.name(req.getName())
				.phoneNumber(req.getPhoneNumber())
				.address(req.getAddress())
				.birth(req.getBirth())
				.gender(req.getGender())
				.profileImg("https://jungkkiri.s3.ap-northeast-2.amazonaws.com/senior_profile_img/0/07610884-fe0c-4943-9bc7-0f12a7cbc256%EC%BA%A1%EC%B2%98.PNG")
				.build())
			.toList();
		List<Senior> savedSeniors = seniorRepository.saveAll(seniors);

		List<MemberSenior> associations = savedSeniors.stream()
			.map(senior -> MemberSenior.builder()
				.member(member)
				.senior(senior)
				.isSocialWorker(true)
				.build())
			.toList();
		memberSeniorService.addAssociation(associations);
	}
}
