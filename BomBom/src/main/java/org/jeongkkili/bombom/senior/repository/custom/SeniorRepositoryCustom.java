package org.jeongkkili.bombom.senior.repository.custom;

import static org.jeongkkili.bombom.senior.domain.QSenior.senior;
import static org.jeongkkili.bombom.member_senior.domain.QMemberSenior.memberSenior;

import java.util.List;

import org.jeongkkili.bombom.member.domain.Member;
import org.jeongkkili.bombom.senior.service.dto.GetSeniorListDto;
import org.springframework.stereotype.Repository;

import com.querydsl.core.types.Projections;
import com.querydsl.jpa.impl.JPAQueryFactory;

import lombok.RequiredArgsConstructor;

@RequiredArgsConstructor
@Repository
public class SeniorRepositoryCustom {

	private final JPAQueryFactory queryFactory;

	public List<GetSeniorListDto> getSeniorList(Member member) {
		return queryFactory.select(Projections.constructor(GetSeniorListDto.class,
				senior.id,
				senior.name,
				senior.address,
				senior.gender.stringValue(),
				senior.birth
			))
			.from(memberSenior)
			.join(memberSenior.senior, senior)
			.where(
				memberSenior.member.eq(member)
			)
			.fetch();
	}
}
