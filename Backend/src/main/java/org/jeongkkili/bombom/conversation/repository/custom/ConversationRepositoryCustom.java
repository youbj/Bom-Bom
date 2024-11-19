package org.jeongkkili.bombom.conversation.repository.custom;

import static org.jeongkkili.bombom.conversation.domain.QConversation.*;

import java.time.LocalDate;
import java.time.LocalDateTime;
import java.time.LocalTime;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import org.jeongkkili.bombom.conversation.service.dto.GetConvListDto;
import org.jeongkkili.bombom.senior.domain.Senior;
import org.springframework.stereotype.Repository;

import com.querydsl.core.Tuple;
import com.querydsl.core.types.Projections;
import com.querydsl.jpa.impl.JPAQueryFactory;

import lombok.RequiredArgsConstructor;

@RequiredArgsConstructor
@Repository
public class ConversationRepositoryCustom {

	private final JPAQueryFactory queryFactory;

	public List<GetConvListDto> getConversationList(Senior senior) {
		LocalDate endDate = LocalDate.now();
		LocalDate startDate = endDate.minusDays(6);
		return queryFactory.select(Projections.constructor(GetConvListDto.class,
			conversation.avgScore,
			conversation.startDate,
			conversation.endTime
			))
			.from(conversation)
			.where(conversation.senior.eq(senior)
				.and(conversation.startDate.between(startDate, endDate)))
			.orderBy(conversation.startDate.desc(), conversation.endTime.desc())
			.fetch();
	}

	public List<Double> getAvgScoresForLastWeek(Senior senior) {
		LocalDate endDate = LocalDate.now();
		LocalDate startDate = endDate.minusDays(6);
		List<Tuple> results = queryFactory
			.select(conversation.startDate, conversation.avgScore.avg())
			.from(conversation)
			.where(conversation.senior.eq(senior)
				.and(conversation.startDate.between(startDate, endDate)))
			.groupBy(conversation.startDate)
			.orderBy(conversation.startDate.asc())
			.fetch();
		Map<LocalDate, Double> scoreMap = new HashMap<>();
		for (Tuple result : results) {
			LocalDate date = result.get(conversation.startDate);
			Double avgScore = result.get(conversation.avgScore.avg());
			scoreMap.put(date, avgScore);
		}
		List<Double> avgScores = new ArrayList<>();
		for (LocalDate date = startDate; !date.isAfter(endDate); date = date.plusDays(1)) {
			Double avgScore = scoreMap.get(date);
			avgScores.add(avgScore);
		}
		return avgScores;
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
