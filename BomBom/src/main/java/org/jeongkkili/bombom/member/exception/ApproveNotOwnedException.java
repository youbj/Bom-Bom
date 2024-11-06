package org.jeongkkili.bombom.member.exception;

public class ApproveNotOwnedException extends RuntimeException {

	public ApproveNotOwnedException() {
	}

	public ApproveNotOwnedException(String message) {
		super(message);
	}

	public ApproveNotOwnedException(String message, Throwable cause) {
		super(message, cause);
	}

	public ApproveNotOwnedException(Throwable cause) {
		super(cause);
	}

	protected ApproveNotOwnedException(String message, Throwable cause, boolean enableSuppression,
		boolean writableStackTrace) {
		super(message, cause, enableSuppression, writableStackTrace);
	}
}
