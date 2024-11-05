package org.jeongkkili.bombom.member.repository;

import java.util.List;

import org.jeongkkili.bombom.member.domain.ApproveRequest;
import org.jeongkkili.bombom.member.domain.Member;
import org.springframework.data.jpa.repository.JpaRepository;

public interface ApproveRequestRepository extends JpaRepository<ApproveRequest, Long> {

	List<ApproveRequest> findByMemberOrderByCreatedAtDesc(Member member);
}
