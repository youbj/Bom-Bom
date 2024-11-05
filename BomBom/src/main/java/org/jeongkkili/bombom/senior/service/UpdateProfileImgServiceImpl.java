package org.jeongkkili.bombom.senior.service;

import org.jeongkkili.bombom.senior.domain.Senior;
import org.springframework.stereotype.Service;

import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;

@Service
@RequiredArgsConstructor
@Slf4j
public class UpdateProfileImgServiceImpl implements UpdateProfileImgService {

	@Override
	public void uploadProfileImg(String imgUrl, Senior senior) {
		System.out.println(imgUrl + " updateservice");
		senior.updateProfileImg(imgUrl);
	}
}
