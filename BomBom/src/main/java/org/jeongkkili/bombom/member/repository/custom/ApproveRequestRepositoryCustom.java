package org.jeongkkili.bombom.member.repository.custom;

import static org.jeongkkili.bombom.member.domain.QApproveRequest.*;

import java.util.List;

import org.jeongkkili.bombom.member.domain.ApproveRequest;
import org.jeongkkili.bombom.member.domain.ApproveType;
import org.jeongkkili.bombom.member.domain.Member;
import org.jeongkkili.bombom.member.service.dto.ApproveRequestDto;
import org.springframework.stereotype.Repository;

import com.querydsl.core.types.Projections;
import com.querydsl.jpa.impl.JPAQueryFactory;

import lombok.RequiredArgsConstructor;

@RequiredArgsConstructor
@Repository
public class ApproveRequestRepositoryCustom {

	private final JPAQueryFactory queryFactory;

	public List<ApproveRequestDto> getRequestList(Member member) {
		return queryFactory.select(Projections.constructor(ApproveRequestDto.class,
			approveRequest.member.id,
			approveRequest.familyName,
			approveRequest.seniorName,
			approveRequest.createdAt
			))
			.from(approveRequest)
			.where(approveRequest.type.eq(ApproveType.PENDING))
			.orderBy(approveRequest.createdAt.desc())
			.fetch();
	}

	public ApproveRequest getRequestByFamilyIdAndSeniorId(Long familyId, Long seniorId) {
		return queryFactory.selectFrom(approveRequest)
			.where(approveRequest.familyId.eq(familyId)
				.and(approveRequest.seniorId.eq(seniorId))
				.and(approveRequest.type.eq(ApproveType.PENDING)))
			.fetchOne();
	}
}
