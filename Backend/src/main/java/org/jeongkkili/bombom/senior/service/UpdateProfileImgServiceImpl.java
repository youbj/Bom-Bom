package org.jeongkkili.bombom.senior.service;

import org.jeongkkili.bombom.senior.domain.Senior;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;

@Service
@RequiredArgsConstructor
@Transactional
@Slf4j
public class UpdateProfileImgServiceImpl implements UpdateProfileImgService {

	@Override
	public void uploadProfileImg(String imgUrl, Senior senior) {
		senior.updateProfileImg(imgUrl);
	}
}
