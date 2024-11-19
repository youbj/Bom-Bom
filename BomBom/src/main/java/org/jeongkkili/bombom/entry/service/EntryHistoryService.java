package org.jeongkkili.bombom.entry.service;

public interface EntryHistoryService {

	void addEntryHistory(Long seniorId);

	void addEntryHistory(Long seniorId, String place);
}
