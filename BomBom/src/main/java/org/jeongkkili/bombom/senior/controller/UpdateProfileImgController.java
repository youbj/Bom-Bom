package org.jeongkkili.bombom.senior.controller;

import org.jeongkkili.bombom.core.aop.annotation.RequireJwtoken;
import org.jeongkkili.bombom.core.aop.member.MemberContext;
import org.jeongkkili.bombom.senior.facade.UpdateProfileImgFacade;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RequestPart;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.multipart.MultipartFile;

import lombok.RequiredArgsConstructor;

@RequiredArgsConstructor
@RestController
public class UpdateProfileImgController extends SeniorController {

	private final UpdateProfileImgFacade updateProfileImgFacade;

	@RequireJwtoken
	@PostMapping("/profile")
	public ResponseEntity<Void> updateProfileImg(
		@RequestPart(name = "profileImg", required = false) MultipartFile profileImg,
		@RequestParam("senior-id") Long seniorId
	) {
		Long memberId = MemberContext.getMemberId();
		updateProfileImgFacade.updateProfileImg(profileImg, seniorId, memberId);
		return ResponseEntity.ok().build();
	}

}
