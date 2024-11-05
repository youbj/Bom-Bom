package org.jeongkkili.bombom.member.service;

import java.util.List;

import org.jeongkkili.bombom.member.controller.request.ApproveRequestReq;
import org.jeongkkili.bombom.member.domain.ApproveRequest;

public interface ApproveRequestService {

	void addApproveRequest(ApproveRequestReq req, Long memberId);

	List<ApproveRequest> getApproveRequests(Long memberId);
}
