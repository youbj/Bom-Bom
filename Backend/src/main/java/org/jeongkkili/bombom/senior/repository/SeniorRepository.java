package org.jeongkkili.bombom.senior.repository;

import java.util.Optional;

import org.jeongkkili.bombom.senior.domain.Senior;
import org.jeongkkili.bombom.senior.exception.SeniorNotFoundException;
import org.springframework.data.jpa.repository.JpaRepository;

public interface SeniorRepository extends JpaRepository<Senior, Long> {

	Optional<Senior> findByNameAndPhoneNumber(String name, String phoneNumber);

	default Senior getOrThrow(Long id) {
		return findById(id).orElseThrow(() -> new SeniorNotFoundException("Senior not found with ID: " + id));
	}

	default Senior getByNameAndPhoneNumberOrThrow(String name, String phoneNumber) {
		return findByNameAndPhoneNumber(name, phoneNumber).orElseThrow(() -> new SeniorNotFoundException("Senior not found with name: " + name));
	}
}
