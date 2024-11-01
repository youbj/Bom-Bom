package org.jeongkkili.bombom.exit.repository;

import java.util.Optional;

import org.jeongkkili.bombom.exit.domain.ExitHistory;
import org.jeongkkili.bombom.senior.domain.Senior;
import org.springframework.data.jpa.repository.JpaRepository;

public interface ExitHistoryRepository extends JpaRepository<ExitHistory, Long>  {

	Optional<ExitHistory> findTopBySeniorOrderByExitAtDesc(Senior senior);
}
