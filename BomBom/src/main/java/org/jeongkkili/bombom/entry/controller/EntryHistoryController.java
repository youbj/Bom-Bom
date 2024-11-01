package org.jeongkkili.bombom.entry.controller;

import org.jeongkkili.bombom.entry.controller.request.EntryReq;
import org.jeongkkili.bombom.entry.controller.request.SaveEntryReq;
import org.jeongkkili.bombom.entry.service.EntryHistoryService;
import org.jeongkkili.bombom.entry.service.dto.PlaceDto;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import lombok.RequiredArgsConstructor;

@RequiredArgsConstructor
@RestController
@RequestMapping("/api/v1/entry")
public class EntryHistoryController {

	private final EntryHistoryService entryHistoryService;

	@PostMapping("/end")
	public ResponseEntity<Void> addEntryHistory(@RequestBody EntryReq req) {
		entryHistoryService.addEntryHistory(req.getSeniorId());
		return ResponseEntity.ok().build();
	}

	@PostMapping("/predict")
	public ResponseEntity<PlaceDto> getPredictPlace(@RequestBody EntryReq req) {
		return ResponseEntity.ok(entryHistoryService.predictPlaceByDurationTime(req.getSeniorId()));
	}

	@PostMapping("/save")
	public ResponseEntity<Void> saveEntryHistory(@RequestBody SaveEntryReq req) {
		entryHistoryService.addEntryHistory(req.getSeniorId(), req.getPlace());
		return ResponseEntity.ok().build();
	}
}
