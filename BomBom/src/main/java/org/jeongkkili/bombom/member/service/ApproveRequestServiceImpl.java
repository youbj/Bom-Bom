package org.jeongkkili.bombom.member.service;

import java.util.List;

import org.jeongkkili.bombom.member.controller.request.ApproveRequestReq;
import org.jeongkkili.bombom.member.domain.ApproveRequest;
import org.jeongkkili.bombom.member.domain.ApproveType;
import org.jeongkkili.bombom.member.domain.Member;
import org.jeongkkili.bombom.member.exception.AlreadyExistAssociationException;
import org.jeongkkili.bombom.member.exception.AlreadyExistRequestException;
import org.jeongkkili.bombom.member.exception.ApproveNotOwnedException;
import org.jeongkkili.bombom.member.repository.ApproveRequestRepository;
import org.jeongkkili.bombom.member.repository.custom.ApproveRequestRepositoryCustom;
import org.jeongkkili.bombom.member.service.dto.ApproveRequestDto;
import org.jeongkkili.bombom.member_senior.service.MemberSeniorService;
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
public class ApproveRequestServiceImpl implements ApproveRequestService {

	private final NotificationService notificationService;
	private final ApproveRequestRepository approveRequestRepository;
	private final ApproveRequestRepositoryCustom approveRequestRepositoryCustom;
	private final GetSeniorService getSeniorService;
	private final MemberSeniorService memberSeniorService;
	private final MemberService memberService;

	@Override
	public void addApproveRequest(ApproveRequestReq req, Long memberId) {
		Senior senior = getSeniorService.getSeniorByNameAndPhoneNumber(req.getSeniorName(), req.getSeniorPhoneNumber());
		Member socialWorker = memberSeniorService.getSocialWorker(senior);
		Member family = memberService.getMemberById(memberId);
		if(memberSeniorService.existAssociation(family, senior)) {
			throw new AlreadyExistAssociationException("Already exist association with member id " + memberId + " and senior id " + senior.getId());
		}
		if(approveRequestRepositoryCustom.getRequestByFamilyIdAndSeniorId(memberId, senior.getId()) != null) {
			throw new AlreadyExistRequestException("Already exist request with member id " + memberId + " and senior id " + senior.getId());
		}
		approveRequestRepository.save(ApproveRequest.builder()
				.member(socialWorker)
				.familyId(family.getId())
				.familyName(family.getName())
				.familyPhoneNumber(family.getPhoneNumber())
				.seniorId(senior.getId())
				.seniorName(senior.getName())
				.seniorPhoneNumber(senior.getPhoneNumber())
				.seniorBirth(senior.getBirth())
			.build());
		// notificationService.notifyUser(socialWorker.getId(), "새로운 승인 요청", "새로운 보호자 승인 요청이 도착했습니다.");
	}

	@Override
	public List<ApproveRequestDto> getApproveRequests(Long memberId) {
		Member member = memberService.getMemberById(memberId);
		return approveRequestRepositoryCustom.getRequestList(member);
	}

	@Override
	public void approveRequest(Long reqId, Long memberId) {
		ApproveRequest req = approveRequestRepository.getOrThrow(reqId);
		Member member = memberService.getMemberById(memberId);
		if(member.getId() != req.getMember().getId()) {
			throw new ApproveNotOwnedException("Approve Not Owned with memberId: " + memberId + " about reqId: " + reqId);
		}
		Member family = memberService.getMemberById(req.getFamilyId());
		Senior senior = getSeniorService.getSeniorById(req.getSeniorId());
		req.changeType(ApproveType.APPROVED);
		memberSeniorService.addAssociation(member, senior);
		// notificationService.notifyUser(family.getId(), "승인 완료", "보호자 승인 요청이 승인되었습니다.");
	}

	@Override
	public void rejectRequest(Long reqId, Long memberId) {
		ApproveRequest req = approveRequestRepository.getOrThrow(reqId);
		Member member = memberService.getMemberById(memberId);
		if(member.getId() != req.getMember().getId()) {
			throw new ApproveNotOwnedException("Approve Not Owned with memberId: " + memberId + " about reqId: " + reqId);
		}
		Member family = memberService.getMemberById(req.getFamilyId());
		req.changeType(ApproveType.REJECTED);
		// notificationService.notifyUser(family.getId(), "승인 거절", "보호자 승인 요청이 거절되었습니다.");
	}
}
