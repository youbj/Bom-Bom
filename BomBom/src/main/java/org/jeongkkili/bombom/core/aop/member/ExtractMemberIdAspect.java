package org.jeongkkili.bombom.core.aop.member;

import org.aspectj.lang.ProceedingJoinPoint;
import org.aspectj.lang.annotation.Around;
import org.aspectj.lang.annotation.Aspect;
import org.jeongkkili.bombom.core.aop.annotation.RequireJwtoken;
import org.jeongkkili.bombom.core.jwt.JwtProvider;
import org.springframework.boot.task.ThreadPoolTaskExecutorBuilder;
import org.springframework.stereotype.Component;
import org.springframework.web.context.request.RequestContextHolder;
import org.springframework.web.context.request.ServletRequestAttributes;

import jakarta.servlet.http.HttpServletRequest;
import lombok.RequiredArgsConstructor;

@Aspect
@RequiredArgsConstructor
@Component
public class ExtractMemberIdAspect {

	private final String AUTHORIZATION_HEADER = "Authorization";
	private final JwtProvider jwtProvider;
	private final ThreadPoolTaskExecutorBuilder threadPoolTaskExecutorBuilder;

	@Around("@annotation(requireJwtoken)")
	public Object before(ProceedingJoinPoint pjp, RequireJwtoken requireJwtoken) throws Throwable {
		HttpServletRequest request = ((ServletRequestAttributes)RequestContextHolder.currentRequestAttributes()).getRequest();
		String accessToken = request.getHeader(AUTHORIZATION_HEADER);
		Long memberId = jwtProvider.getMemberId(accessToken);
		MemberContext.setMemberId(memberId);
		try {
			return pjp.proceed();
		} catch (Throwable e) {
			throw e;
		} finally {
			MemberContext.clear();
		}
	}

}
