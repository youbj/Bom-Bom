package org.jeongkkili.bombom.member.repository;

import org.jeongkkili.bombom.member.domain.Member;
import org.springframework.data.jpa.repository.JpaRepository;

public interface MemberRepository extends JpaRepository<Member, Long> {

	Member findByLoginId(String loginId);
}
