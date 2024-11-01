package org.jeongkkili.bombom.core.aop.member;

public class MemberContext {

	private static final ThreadLocal<Long> memberIdHolder = new ThreadLocal<>();

	/**
	 * 현재 스레드의 memberId를 설정합니다.
	 *
	 * @param memberId 설정할 memberId 값
	 */
	public static void setMemberId(Long memberId) {
		memberIdHolder.set(memberId);
	}

	/**
	 * 현재 스레드의 memberId를 반환합니다.
	 *
	 * @return 현재 스레드에 설정된 memberId 값, 없으면 null
	 */
	public static Long getMemberId() {
		return memberIdHolder.get();
	}

	/**
	 * 현재 스레드의 memberId 값을 제거합니다.
	 * 이를 통해 메모리 누수를 방지할 수 있습니다.
	 */
	public static void clear() {
		memberIdHolder.remove();
	}
}
