package org.jeongkkili.bombom.member_senior.repository;

import java.util.Optional;

import org.jeongkkili.bombom.member.domain.Member;
import org.jeongkkili.bombom.member_senior.domain.MemberSenior;
import org.jeongkkili.bombom.member_senior.exception.AssociationNotFoundException;
import org.jeongkkili.bombom.senior.domain.Senior;
import org.springframework.data.jpa.repository.JpaRepository;

public interface MemberSeniorRepository extends JpaRepository<MemberSenior, Long> {

	Optional<MemberSenior> findByMemberAndSenior(Member member, Senior senior);

	default MemberSenior getOrThrow(Member member, Senior senior) {
		return findByMemberAndSenior(member, senior)
			.orElseThrow(() -> new AssociationNotFoundException("Association between member and senior not found"));
	}
}
