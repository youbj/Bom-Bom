package org.jeongkkili.bombom.member.repository;

import java.util.List;
import java.util.Optional;

import org.jeongkkili.bombom.member.domain.ApproveRequest;
import org.jeongkkili.bombom.member.domain.Member;
import org.jeongkkili.bombom.member.exception.ApproveReqNotFoundException;
import org.springframework.data.jpa.repository.JpaRepository;

public interface ApproveRequestRepository extends JpaRepository<ApproveRequest, Long> {

	Optional<ApproveRequest> findById(Long id);

	List<ApproveRequest> findByMemberOrderByCreatedAtDesc(Member member);

	default ApproveRequest getOrThrow(Long id) {
		return findById(id).orElseThrow(() -> new ApproveReqNotFoundException("Approve Not Found with ID: " + id));
	}
}
