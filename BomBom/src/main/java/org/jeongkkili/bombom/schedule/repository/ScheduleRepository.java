package org.jeongkkili.bombom.schedule.repository;

import org.jeongkkili.bombom.schedule.domain.Schedule;
import org.springframework.data.jpa.repository.JpaRepository;

public interface ScheduleRepository extends JpaRepository<Schedule, Long>  {

}
