package org.jeongkkili.bombom.exit.service;

import org.jeongkkili.bombom.exit.domain.ExitHistory;
import org.jeongkkili.bombom.exit.repository.ExitHistoryRepository;
import org.jeongkkili.bombom.senior.domain.Senior;
import org.jeongkkili.bombom.senior.service.GetSeniorService;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;

@Service
@RequiredArgsConstructor
@Transactional
@Slf4j
public class ExitHistoryServiceImpl implements ExitHistoryService {

	private final GetSeniorService getSeniorService;
	private final ExitHistoryRepository exitHistoryRepository;

	@Override
	public void addExitHistory(Long seniorId) {
		Senior senior = getSeniorService.getSeniorById(seniorId);
		exitHistoryRepository.save(ExitHistory.builder().senior(senior).build());
	}
}
