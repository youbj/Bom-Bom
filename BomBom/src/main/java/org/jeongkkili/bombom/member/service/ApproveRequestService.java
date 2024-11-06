package org.jeongkkili.bombom.member.service;

import java.util.List;

import org.jeongkkili.bombom.member.controller.request.ApproveRequestReq;
import org.jeongkkili.bombom.member.service.dto.ApproveRequestDto;

public interface ApproveRequestService {

	void addApproveRequest(ApproveRequestReq req, Long memberId);

	List<ApproveRequestDto> getApproveRequests(Long memberId);

	void approveRequest(Long reqId, Long memberId);

	void rejectRequest(Long reqId, Long memberId);
}
