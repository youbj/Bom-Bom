package org.jeongkkili.bombom.conversation.service;

import org.jeongkkili.bombom.conversation.repository.custom.ConversationRepositoryCustom;
import org.jeongkkili.bombom.senior.domain.Senior;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;

@Service
@RequiredArgsConstructor
@Transactional
@Slf4j
public class GetEmotionServiceImpl implements GetEmotionService {

	private final ConversationRepositoryCustom convRepositoryCustom;

	@Override
	public Double getTodayEmotionAvg(Senior senior) {
		return convRepositoryCustom.getTodayEmotionAvg(senior);
	}
}
