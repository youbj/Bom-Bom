package org.jeongkkili.bombom.schedule.repository.custom;

import static org.jeongkkili.bombom.schedule.domain.QSchedule.schedule;

import java.time.LocalDateTime;
import java.util.List;

import org.jeongkkili.bombom.schedule.service.dto.ScheduleMonthDto;
import org.jeongkkili.bombom.senior.domain.Senior;
import org.springframework.stereotype.Repository;

import com.querydsl.core.types.Projections;
import com.querydsl.core.types.dsl.BooleanExpression;
import com.querydsl.jpa.impl.JPAQueryFactory;

import lombok.RequiredArgsConstructor;

@RequiredArgsConstructor
@Repository
public class ScheduleRepositoryCustom {

	private final JPAQueryFactory queryFactory;

	public List<ScheduleMonthDto> findMonthlyScheduleBySeniorId(Senior senior, Integer year, Integer month) {
		return queryFactory
			.select(Projections.constructor(ScheduleMonthDto.class,
				schedule.scheduleId,
				schedule.memo,
				schedule.scheduleAt))
			.from(schedule)
			.where(
				schedule.senior.eq(senior),
				getMonth(year, month)
			)
			.orderBy(schedule.scheduleAt.asc())
			.fetch();
	}

	private BooleanExpression getMonth(Integer year, Integer month)  {
		LocalDateTime startDate = LocalDateTime.of(year, month, 1, 0, 0);
		LocalDateTime endDate = startDate.plusMonths(1).minusNanos(1);
		return schedule.scheduleAt.between(startDate, endDate);
	}

}
