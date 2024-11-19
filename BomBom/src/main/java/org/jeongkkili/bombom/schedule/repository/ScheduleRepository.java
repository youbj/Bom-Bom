package org.jeongkkili.bombom.schedule.repository;

import org.jeongkkili.bombom.schedule.domain.Schedule;
import org.jeongkkili.bombom.schedule.exception.ScheduleNotFoundException;
import org.springframework.data.jpa.repository.JpaRepository;

public interface ScheduleRepository extends JpaRepository<Schedule, Long>  {

	default Schedule getOrThrow(Long id) {
		return findById(id).orElseThrow(() -> new ScheduleNotFoundException("schedule not found"));
	}
}
