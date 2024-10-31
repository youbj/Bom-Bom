package org.jeongkkili.bombom.exit.service;

import org.jeongkkili.bombom.exit.domain.ExitHistory;
import org.jeongkkili.bombom.exit.repository.ExitHistoryRepository;
import org.jeongkkili.bombom.senior.domain.Senior;
import org.jeongkkili.bombom.senior.exception.SeniorNotFoundException;
import org.jeongkkili.bombom.senior.repository.SeniorRepository;
import org.springframework.stereotype.Service;

import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;

@Service
@RequiredArgsConstructor
@Slf4j
public class ExitHistoryServiceImpl implements ExitHistoryService {

	private final SeniorRepository seniorRepository;
	private final ExitHistoryRepository exitHistoryRepository;

	@Override
	public void addExitHistory(Long seniorId) {
		Senior senior = seniorRepository.findById(seniorId)
			.orElseThrow(() -> new SeniorNotFoundException("Senior not found with ID: " + seniorId));
		exitHistoryRepository.save(ExitHistory.builder().senior(senior).build());
	}
}
