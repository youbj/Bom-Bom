package org.jeongkkili.bombom.conversation.repository.custom;

import static org.jeongkkili.bombom.conversation.domain.QConversation.*;

import java.time.LocalDate;
import java.time.LocalDateTime;
import java.time.LocalTime;
import java.util.List;

import org.jeongkkili.bombom.conversation.service.dto.GetConvListDto;
import org.jeongkkili.bombom.senior.domain.Senior;
import org.springframework.stereotype.Repository;

import com.querydsl.core.types.Projections;
import com.querydsl.jpa.impl.JPAQueryFactory;

import lombok.RequiredArgsConstructor;

@RequiredArgsConstructor
@Repository
public class ConversationRepositoryCustom {

	private final JPAQueryFactory queryFactory;

	public List<GetConvListDto> getConversationList(Senior senior) {
		return queryFactory.select(Projections.constructor(GetConvListDto.class,
			conversation.avgScore,
			conversation.startDate,
			conversation.endTime
			))
			.from(conversation)
			.where(conversation.senior.eq(senior))
			.orderBy(conversation.endTime.desc())
			.fetch();
	}

	public Double getTodayEmotionAvg(Senior senior) {
		LocalDate today = LocalDate.now();
		return queryFactory.select(conversation.avgScore.avg())
			.from(conversation)
			.where(conversation.senior.eq(senior)
				.and(conversation.startDate.eq(today)))
			.fetchOne();
	}
}
