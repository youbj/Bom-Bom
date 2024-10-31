package org.jeongkkili.bombom.member.service;

import org.jeongkkili.bombom.core.jwt.JwtProvider;
import org.jeongkkili.bombom.core.jwt.dto.Jwtoken;
import org.jeongkkili.bombom.member.controller.request.LoginReq;
import org.jeongkkili.bombom.member.domain.Member;
import org.jeongkkili.bombom.member.domain.Type;
import org.jeongkkili.bombom.member.controller.request.RegistMemberReq;
import org.jeongkkili.bombom.member.exception.AlreadyExistIdException;
import org.jeongkkili.bombom.member.exception.MemberNotFoundException;
import org.jeongkkili.bombom.member.exception.WrongPasswordException;
import org.jeongkkili.bombom.member.repository.MemberRepository;
import org.jeongkkili.bombom.member.service.dto.LoginDto;
import org.mindrot.jbcrypt.BCrypt;
import org.springframework.stereotype.Service;

import jakarta.transaction.Transactional;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;

@Service
@RequiredArgsConstructor
@Slf4j
public class MemberServiceImpl implements MemberService {

	private final MemberRepository memberRepository;
	private final JwtProvider jwtProvider;

	@Override
	@Transactional
	public void registMember(RegistMemberReq req) {
		if(checkAlreadyExistId(req.getLoginId())) {
			throw new AlreadyExistIdException("Already Exist Id: " + req.getLoginId());
		}

		Member member = memberRepository.save(Member.builder()
			.loginId(req.getLoginId())
			.password(hashPassword(req.getPassword()))
			.name(req.getName())
			.phoneNumber(req.getPhoneNumber())
			.type(Type.valueOf(req.getType()))
			.build());

		if(req.getType().equals("SOCIAL_WORKER")) {
			StringBuilder sb = new StringBuilder();
			String memberId = String.valueOf(member.getId());
			sb.append("SW");
			sb.append("0".repeat(8 - memberId.length()));
			sb.append(memberId);
			member.updateCi(sb.toString());
		}
	}

	@Override
	public LoginDto login(LoginReq req) {
		Member member = memberRepository.findByLoginId(req.getLoginId());
		if(member == null) throw new MemberNotFoundException("Member not found with ID: " + req.getLoginId());
		if(!checkPassword(req.getPassword(), member.getPassword())) throw new WrongPasswordException("Wrong password with ID: " + req.getLoginId());
		Jwtoken jwtoken = jwtProvider.createToken(member.getId());
		return LoginDto.builder()
			.loginId(member.getLoginId())
			.name(member.getName())
			.phoneNumber(member.getPhoneNumber())
			.type(member.getType())
			.accessToken(jwtoken.getAccessToken())
			.refreshToken(jwtoken.getRefreshToken())
			.build();
	}

	@Override
	public boolean checkAlreadyExistId(String loginId) {
		return memberRepository.findByLoginId(loginId) != null;
	}

	private String hashPassword(String plainPassword) {
		return BCrypt.hashpw(plainPassword, BCrypt.gensalt());
	}

	private boolean checkPassword(String plainPassword, String hashedPassword) {
		return BCrypt.checkpw(plainPassword, hashedPassword);
	}
}
