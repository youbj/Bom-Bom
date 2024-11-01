package org.jeongkkili.bombom.entry.service;

import java.time.Duration;
import java.time.LocalDateTime;

import org.jeongkkili.bombom.entry.domain.EntryHistory;
import org.jeongkkili.bombom.entry.exception.LatestExitHistoryNotFoundException;
import org.jeongkkili.bombom.entry.repository.EntryHistoryRepository;
import org.jeongkkili.bombom.entry.service.dto.PlaceDto;
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
public class EntryHistoryServiceImpl implements EntryHistoryService {

	private final SeniorRepository seniorRepository;
	private final EntryHistoryRepository entryHistoryRepository;
	private final ExitHistoryRepository exitHistoryRepository;

	@Override
	public void addEntryHistory(Long seniorId) {
		Senior senior = getSeniorBySeniorId(seniorId);
		ExitHistory latestExitHistory = getLatestExitHistoryBySeniorId(senior);
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
		Senior senior = getSeniorBySeniorId(seniorId);
		ExitHistory latestExitHistory = getLatestExitHistoryBySeniorId(senior);

		entryHistoryRepository.save(EntryHistory.builder()
			.senior(senior)
			.place(place)
			.durationTime(getDurationTime(latestExitHistory))
			.build());
	}

	@Override
	public PlaceDto predictPlaceByDurationTime(Long seniorId) {
		Senior senior = getSeniorBySeniorId(seniorId);
		ExitHistory latestExitHistory = getLatestExitHistoryBySeniorId(senior);
		Long durationTime = getDurationTime(latestExitHistory);
		// TODO: 모델에 seniorId와 durationTime을 전송하여 예상되는 방문 장소를 리턴하여 스피커로 전송
		String place = "";
		return PlaceDto.builder()
			.place(place)
			.build();
	}

	private Senior getSeniorBySeniorId(Long seniorId) {
		return seniorRepository.findById(seniorId)
			.orElseThrow(() -> new SeniorNotFoundException("Senior not found by ID: " + seniorId));
	}

	private ExitHistory getLatestExitHistoryBySeniorId(Senior senior) {
		return exitHistoryRepository.findTopBySeniorOrderByExitAtDesc(senior)
			.orElseThrow(() -> new LatestExitHistoryNotFoundException("Latest Exit History Not Found"));
	}

	private Long getDurationTime(ExitHistory latestExitHistory) {
		return  Duration.between(latestExitHistory.getExitAt(), LocalDateTime.now()).getSeconds();
	}
}
