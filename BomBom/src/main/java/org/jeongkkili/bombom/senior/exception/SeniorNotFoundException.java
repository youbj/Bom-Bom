package org.jeongkkili.bombom.senior.exception;

public class SeniorNotFoundException extends RuntimeException {

	public SeniorNotFoundException() {
	}

	public SeniorNotFoundException(String message) {
		super(message);
	}

	public SeniorNotFoundException(String message, Throwable cause) {
		super(message, cause);
	}

	public SeniorNotFoundException(Throwable cause) {
		super(cause);
	}

	protected SeniorNotFoundException(String message, Throwable cause, boolean enableSuppression,
		boolean writableStackTrace) {
		super(message, cause, enableSuppression, writableStackTrace);
	}
}
