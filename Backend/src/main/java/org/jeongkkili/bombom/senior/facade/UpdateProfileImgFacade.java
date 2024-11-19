package org.jeongkkili.bombom.senior.facade;

import org.jeongkkili.bombom.infra.s3.S3ImageService;
import org.jeongkkili.bombom.infra.s3.dto.FileMetaInfo;
import org.jeongkkili.bombom.member.domain.Member;
import org.jeongkkili.bombom.member.service.MemberService;
import org.jeongkkili.bombom.member_senior.service.MemberSeniorService;
import org.jeongkkili.bombom.senior.domain.Senior;
import org.jeongkkili.bombom.senior.service.GetSeniorService;
import org.jeongkkili.bombom.senior.service.UpdateProfileImgService;
import org.springframework.stereotype.Component;
import org.springframework.transaction.annotation.Transactional;
import org.springframework.web.multipart.MultipartFile;

import lombok.RequiredArgsConstructor;

@Transactional
@RequiredArgsConstructor
@Component
public class UpdateProfileImgFacade {

	private final MemberService memberService;
	private final GetSeniorService getSeniorService;
	private final MemberSeniorService memberSeniorService;
	private final S3ImageService s3ImageService;
	private final UpdateProfileImgService updateProfileImgService;

	public void updateProfileImg(MultipartFile profileImg, Long seniorId, Long memberId) {
		Member member = memberService.getMemberById(memberId);
		Senior senior = getSeniorService.getSeniorById(seniorId);
		memberSeniorService.checkAssociation(member, senior);
		String imgUrl = uploadProfileImg(profileImg, seniorId);
		updateProfileImgService.uploadProfileImg(imgUrl, senior);
	}

	private String uploadProfileImg(MultipartFile profileImg, Long seniorId) {
		FileMetaInfo fileMetaInfo = s3ImageService.uploadSeniorProfileImg(profileImg, seniorId);
		return fileMetaInfo.getUrl();
	}
}
