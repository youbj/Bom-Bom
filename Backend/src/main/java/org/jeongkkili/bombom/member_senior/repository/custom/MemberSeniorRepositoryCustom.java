package org.jeongkkili.bombom.member_senior.repository.custom;

import static org.jeongkkili.bombom.member_senior.domain.QMemberSenior.*;

import java.util.List;

import org.jeongkkili.bombom.member.domain.Member;
import org.jeongkkili.bombom.member_senior.exception.AssociationNotFoundException;
import org.jeongkkili.bombom.senior.domain.Senior;
import org.springframework.stereotype.Repository;

import com.querydsl.jpa.impl.JPAQueryFactory;

import lombok.RequiredArgsConstructor;

@RequiredArgsConstructor
@Repository
public class MemberSeniorRepositoryCustom {

	private final JPAQueryFactory queryFactory;

	public Member findBySeniorAndIsSocialWorkerTrue(Senior senior) {
		Member member = queryFactory.select(memberSenior.member)
			.from(memberSenior)
			.where(memberSenior.senior.eq(senior)
				.and(memberSenior.isSocialWorker.isTrue()))
			.fetchOne();
		if(member == null) {
			throw new AssociationNotFoundException("Association between member and senior not found");
		}
		return member;
	}

	public List<Member> findBySenior(Senior senior) {
		List<Member> members = queryFactory.select(memberSenior.member)
			.from(memberSenior)
			.where(memberSenior.senior.eq(senior))
			.fetch();

		if (members.isEmpty()) {
			throw new AssociationNotFoundException("No associations found between member and senior");
		}
		return members;
	}
}
