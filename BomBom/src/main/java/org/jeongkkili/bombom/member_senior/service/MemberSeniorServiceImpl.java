package org.jeongkkili.bombom.member_senior.service;

import java.util.List;

import org.jeongkkili.bombom.member.domain.Member;
import org.jeongkkili.bombom.member_senior.domain.MemberSenior;
import org.jeongkkili.bombom.member_senior.repository.MemberSeniorRepository;
import org.jeongkkili.bombom.senior.domain.Senior;
import org.springframework.stereotype.Service;

import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;

@Service
@RequiredArgsConstructor
@Slf4j
public class MemberSeniorServiceImpl implements MemberSeniorService {

	private final MemberSeniorRepository memberSeniorRepository;

	@Override
	public void addAssociation(List<MemberSenior> associations) {
		memberSeniorRepository.saveAll(associations);
	}

	@Override
	public boolean checkAssociation(Member member, Senior senior) {
		return memberSeniorRepository.getOrThrow(member, senior) != null;
	}

	@Override
	public Member getSocialWorker(Senior senior) {
		return memberSeniorRepository.getSocialWorkerIdBySeniorOrThrow(senior);
	}
}
