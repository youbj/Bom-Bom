package org.jeongkkili.bombom.conversation.service;

import org.jeongkkili.bombom.conversation.controller.request.RegistConvReq;
import org.jeongkkili.bombom.conversation.domain.Conversation;
import org.jeongkkili.bombom.conversation.repository.ConversationRepository;
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
public class RegistConvServiceImpl implements RegistConvService {

	private final GetSeniorService getSeniorService;
	private final ConversationRepository convRepository;

	@Override
	public void registConv(RegistConvReq req) {
		Senior senior = getSeniorService.getSeniorById(req.getSeniorId());
		convRepository.save(Conversation.builder()
			.senior(senior)
			.summary(req.getSummary())
			.emotion(req.getEmotion())
			.build());
	}
}
