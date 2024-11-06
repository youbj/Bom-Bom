package org.jeongkkili.bombom.member.exception;

public class AlreadyExistRequestException extends RuntimeException {

	public AlreadyExistRequestException() {
	}

	public AlreadyExistRequestException(String message) {
		super(message);
	}

	public AlreadyExistRequestException(String message, Throwable cause) {
		super(message, cause);
	}

	public AlreadyExistRequestException(Throwable cause) {
		super(cause);
	}

	protected AlreadyExistRequestException(String message, Throwable cause, boolean enableSuppression,
		boolean writableStackTrace) {
		super(message, cause, enableSuppression, writableStackTrace);
	}
}
