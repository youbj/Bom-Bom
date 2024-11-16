package org.jeongkkili.bombom.schedule.repository.custom;

import static org.jeongkkili.bombom.schedule.domain.QSchedule.schedule;

import java.time.LocalDate;
import java.time.LocalDateTime;
import java.util.List;

import org.jeongkkili.bombom.schedule.service.dto.ScheduleMonthDto;
import org.jeongkkili.bombom.schedule.service.dto.ScheduleTodayDto;
import org.jeongkkili.bombom.senior.domain.Senior;
import org.springframework.stereotype.Repository;

import com.querydsl.core.types.Projections;
import com.querydsl.core.types.dsl.BooleanExpression;
import com.querydsl.core.types.dsl.Expressions;
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
				schedule.startAt,
				schedule.endAt))
			.from(schedule)
			.where(
				schedule.senior.eq(senior),
				getMonth(year, month)
			)
			.orderBy(schedule.startAt.asc())
			.fetch();
	}

	public List<ScheduleTodayDto> findTodayScheduleBySeniorId(Senior senior) {
		LocalDateTime todayStart = LocalDate.now().atStartOfDay();
		LocalDateTime todayEnd = todayStart.plusDays(1).minusSeconds(1);
		return queryFactory
			.select(Projections.constructor(ScheduleTodayDto.class,
				schedule.memo,
				Expressions.stringTemplate(
					"CASE WHEN HOUR({0}) < 12 THEN '오전 ' ELSE '오후 ' END || DATE_FORMAT({0}, '%l시 %i분')",
					schedule.startAt
				)
			))
			.from(schedule)
			.where(
				schedule.senior.eq(senior),
				schedule.startAt.between(todayStart, todayEnd)
			)
			.orderBy(schedule.startAt.asc())
			.fetch();
	}

	private BooleanExpression getMonth(Integer year, Integer month)  {
		LocalDateTime startDate = LocalDateTime.of(year, month, 1, 0, 0);
		LocalDateTime endDate = startDate.plusMonths(1).minusNanos(1);
		return schedule.startAt.between(startDate, endDate)
			.or(schedule.endAt.between(startDate, endDate))
			.or(schedule.startAt.before(startDate).and(schedule.endAt.after(endDate)));
	}

}
