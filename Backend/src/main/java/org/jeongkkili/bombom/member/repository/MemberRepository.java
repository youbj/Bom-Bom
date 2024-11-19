package org.jeongkkili.bombom.member.repository;

import java.util.Optional;

import org.jeongkkili.bombom.member.domain.Member;
import org.jeongkkili.bombom.member.exception.MemberNotFoundException;
import org.springframework.data.jpa.repository.JpaRepository;

public interface MemberRepository extends JpaRepository<Member, Long> {

	Optional<Member> findByLoginId(String loginId);

	default Member getByLoginIdOrThrow(String loginId) {
		return findByLoginId(loginId).orElseThrow(() -> new MemberNotFoundException("Member not found with ID: " + loginId));
	}

	default Member getOrThrow(Long memberId) {
		return findById(memberId).orElseThrow(() -> new MemberNotFoundException("Member not found with ID: " + memberId));
	}
}
