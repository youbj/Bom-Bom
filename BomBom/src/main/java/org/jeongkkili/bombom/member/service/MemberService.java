package org.jeongkkili.bombom.member.service;

import org.jeongkkili.bombom.member.controller.request.LoginReq;
import org.jeongkkili.bombom.member.controller.request.RegistMemberReq;
import org.jeongkkili.bombom.member.domain.Member;
import org.jeongkkili.bombom.member.service.dto.LoginDto;

public interface MemberService {

	void registMember(RegistMemberReq req);

	LoginDto login(LoginReq req);

	boolean checkAlreadyExistId(String loginId);

	Member getMemberById(Long memberId);
}
