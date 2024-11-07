package org.jeongkkili.bombom.conversation.controller;

import org.jeongkkili.bombom.conversation.controller.request.RegistConvReq;
import org.jeongkkili.bombom.conversation.service.RegistConvService;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RestController;

import lombok.RequiredArgsConstructor;

@RequiredArgsConstructor
@RestController
public class RegistConvController extends ConversationController {

	private final RegistConvService registConvService;

	@PostMapping("/regist")
	public ResponseEntity<Void> registConv(@RequestBody RegistConvReq req) {
		registConvService.registConv(req);
		return ResponseEntity.ok().build();
	}
}
