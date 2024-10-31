package org.jeongkkili.bombom.entry.repository;

import org.jeongkkili.bombom.entry.domain.EntryHistory;
import org.springframework.data.jpa.repository.JpaRepository;

public interface EntryHistoryRepository extends JpaRepository<EntryHistory, Long> {
}
