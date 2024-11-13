package org.jeongkkili.bombom.speaker.service;

import org.jeongkkili.bombom.senior.domain.Senior;
import org.jeongkkili.bombom.senior.service.GetSeniorService;
import org.jeongkkili.bombom.speaker.controller.request.RegistSpeakerReq;
import org.jeongkkili.bombom.speaker.domain.Speaker;
import org.jeongkkili.bombom.speaker.exception.AlreadyExistSerialNumException;
import org.jeongkkili.bombom.speaker.repository.SpeakerRepository;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;

@Service
@RequiredArgsConstructor
@Transactional
@Slf4j
public class RegistSpeakerServiceImpl implements RegistSpeakerService {

	private final SpeakerRepository speakerRepository;
	private final GetSeniorService getSeniorService;

	@Override
	public void registSpeaker(RegistSpeakerReq req) {
		Senior senior = getSeniorService.getSeniorById(req.getSeniorId());
		if(speakerRepository.findBySerialNum(req.getSerialNum()) != null) {
			throw new AlreadyExistSerialNumException("Serial number already exist");
		}
		speakerRepository.save(Speaker.builder()
				.senior(senior)
				.serialNum(req.getSerialNum())
			.build());
	}
}
