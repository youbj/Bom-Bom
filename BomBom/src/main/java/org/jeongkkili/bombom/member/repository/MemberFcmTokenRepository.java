package org.jeongkkili.bombom.member.repository;

import org.jeongkkili.bombom.member.domain.MemberFcmToken;
import org.springframework.data.jpa.repository.JpaRepository;

public interface MemberFcmTokenRepository extends JpaRepository<MemberFcmToken, Long> {

	MemberFcmToken findByMemberId(Long memberId);
}
