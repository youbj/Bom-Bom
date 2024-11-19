package org.jeongkkili.bombom.member_senior.service;

import java.util.List;

import org.jeongkkili.bombom.member.domain.Member;
import org.jeongkkili.bombom.member_senior.domain.MemberSenior;
import org.jeongkkili.bombom.member_senior.repository.MemberSeniorRepository;
import org.jeongkkili.bombom.member_senior.repository.custom.MemberSeniorRepositoryCustom;
import org.jeongkkili.bombom.senior.domain.Senior;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;

@Service
@RequiredArgsConstructor
@Transactional
@Slf4j
public class MemberSeniorServiceImpl implements MemberSeniorService {

	private final MemberSeniorRepository memberSeniorRepository;
	private final MemberSeniorRepositoryCustom memberSeniorRepositoryCustom;

	@Override
	public void addAssociation(List<MemberSenior> associations) {
		memberSeniorRepository.saveAll(associations);
	}

	@Override
	public void addAssociation(Member member, Senior senior) {
		memberSeniorRepository.save(MemberSenior.builder()
				.member(member)
				.senior(senior)
				.isSocialWorker(false)
			.build());
	}

	@Override
	public void checkAssociation(Member member, Senior senior) {
		memberSeniorRepository.getOrThrow(member, senior);
	}

	@Override
	public Member getSocialWorker(Senior senior) {
		return memberSeniorRepositoryCustom.findBySeniorAndIsSocialWorkerTrue(senior);
	}

	@Override
	public List<Member> getMembersBySenior(Senior senior) {
		return memberSeniorRepositoryCustom.findBySenior(senior);
	}

	@Override
	public boolean existAssociation(Member member, Senior senior) {
		return memberSeniorRepository.findByMemberAndSenior(member, senior).isPresent();
	}
}
