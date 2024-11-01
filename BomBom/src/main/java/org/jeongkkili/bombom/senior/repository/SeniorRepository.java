package org.jeongkkili.bombom.senior.repository;

import org.jeongkkili.bombom.senior.domain.Senior;
import org.jeongkkili.bombom.senior.exception.SeniorNotFoundException;
import org.springframework.data.jpa.repository.JpaRepository;

public interface SeniorRepository extends JpaRepository<Senior, Long> {

	default Senior getOrThrow(Long id) {
		return findById(id).orElseThrow(() -> new SeniorNotFoundException("Senior not found with ID: " + id));
	}
}
