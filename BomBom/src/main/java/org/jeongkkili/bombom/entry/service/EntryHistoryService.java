package org.jeongkkili.bombom.entry.service;

import org.jeongkkili.bombom.entry.service.dto.PlaceDto;

public interface EntryHistoryService {

	void addEntryHistory(Long seniorId);

	void addEntryHistory(Long seniorId, String place);

	PlaceDto predictPlaceByDurationTime(Long seniorId);
}
