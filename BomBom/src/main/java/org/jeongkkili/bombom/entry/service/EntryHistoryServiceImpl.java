package org.jeongkkili.bombom.entry.service;

import java.time.Duration;
import java.time.LocalDateTime;

import org.jeongkkili.bombom.entry.domain.EntryHistory;
import org.jeongkkili.bombom.entry.repository.EntryHistoryRepository;
import org.jeongkkili.bombom.exit.domain.ExitHistory;
import org.jeongkkili.bombom.exit.repository.ExitHistoryRepository;
import org.jeongkkili.bombom.senior.domain.Senior;
import org.jeongkkili.bombom.senior.service.GetSeniorService;
import org.springframework.stereotype.Service;

import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;

@Service
@RequiredArgsConstructor
@Slf4j
public class EntryHistoryServiceImpl implements EntryHistoryService {

	private final GetSeniorService getSeniorService;
	private final EntryHistoryRepository entryHistoryRepository;
	private final ExitHistoryRepository exitHistoryRepository;

	@Override
	public void addEntryHistory(Long seniorId) {
		Senior senior = getSeniorService.getSeniorById(seniorId);
		ExitHistory latestExitHistory = exitHistoryRepository.getLatestOrThrow(senior);
		// TODO: 장소에 대한 정보를 스피커를 통해 입력 받고 db에 저장
		String place = "";

		entryHistoryRepository.save(EntryHistory.builder()
				.senior(senior)
				.place(place)
				.durationTime(getDurationTime(latestExitHistory))
				.build());
	}

	@Override
	public void addEntryHistory(Long seniorId, String place) {
		Senior senior = getSeniorService.getSeniorById(seniorId);
		ExitHistory latestExitHistory = exitHistoryRepository.getLatestOrThrow(senior);

		entryHistoryRepository.save(EntryHistory.builder()
			.senior(senior)
			.place(place)
			.durationTime(getDurationTime(latestExitHistory))
			.build());
	}

	private Long getDurationTime(ExitHistory latestExitHistory) {
		return  Duration.between(latestExitHistory.getExitAt(), LocalDateTime.now()).getSeconds();
	}
}
