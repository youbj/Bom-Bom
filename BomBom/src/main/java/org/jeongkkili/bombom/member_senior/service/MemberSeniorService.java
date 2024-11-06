package org.jeongkkili.bombom.member_senior.service;

import java.util.List;

import org.jeongkkili.bombom.member.domain.Member;
import org.jeongkkili.bombom.member_senior.domain.MemberSenior;
import org.jeongkkili.bombom.senior.domain.Senior;

public interface MemberSeniorService {

	void addAssociation(List<MemberSenior> associations);

	void addAssociation(Member member, Senior senior);

	void checkAssociation(Member member, Senior senior);

	Member getSocialWorker(Senior senior);

	boolean existAssociation(Member member, Senior senior);
}
