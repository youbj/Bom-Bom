package org.jeongkkili.bombom.speaker.controller;

import org.jeongkkili.bombom.speaker.controller.request.RegistSpeakerReq;
import org.jeongkkili.bombom.speaker.service.RegistSpeakerService;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RestController;

import lombok.RequiredArgsConstructor;

@RequiredArgsConstructor
@RestController
public class RegistSpeakerController extends SpeakerController {

	private final RegistSpeakerService registSpeakerService;

	@PostMapping("/regist")
	public ResponseEntity<Void> registSpeaker(RegistSpeakerReq req) {
		registSpeakerService.registSpeaker(req);
		return ResponseEntity.ok().build();
	}
}
