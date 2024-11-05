package org.jeongkkili.bombom.member.service;

import java.util.List;

import org.jeongkkili.bombom.member.controller.request.ApproveRequestReq;
import org.jeongkkili.bombom.member.domain.ApproveRequest;
import org.jeongkkili.bombom.member.domain.Member;
import org.jeongkkili.bombom.member.repository.ApproveRequestRepository;
import org.jeongkkili.bombom.member_senior.service.MemberSeniorService;
import org.jeongkkili.bombom.senior.domain.Senior;
import org.jeongkkili.bombom.senior.service.GetSeniorService;
import org.springframework.stereotype.Service;

import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;

@Service
@RequiredArgsConstructor
@Slf4j
public class ApproveRequestServiceImpl implements ApproveRequestService {

	private final NotificationService notificationService;
	private final ApproveRequestRepository approveRequestRepository;
	private final GetSeniorService getSeniorService;
	private final MemberSeniorService memberSeniorService;
	private final MemberService memberService;

	@Override
	public void addApproveRequest(ApproveRequestReq req, Long memberId) {
		Senior senior = getSeniorService.getSeniorByNameAndPhoneNumber(req.getSeniorName(), req.getSeniorPhoneNumber());
		Member socialWorker = memberSeniorService.getSocialWorker(senior);
		Member family = memberService.getMemberById(memberId);
		approveRequestRepository.save(ApproveRequest.builder()
				.member(socialWorker)
				.familyId(family.getId())
				.familyName(family.getName())
				.seniorId(senior.getId())
				.seniorName(senior.getName())
			.build());
		notificationService.notifyUser(socialWorker.getId(), "새로운 승인 요청", "새로운 보호자 승인 요청이 도착했습니다.");
	}

	@Override
	public List<ApproveRequest> getApproveRequests(Long memberId) {
		Member member = memberService.getMemberById(memberId);
		return approveRequestRepository.findByMemberOrderByCreatedAtDesc(member);
	}
}
