package org.jeongkkili.bombom.core.jwt.exception;

public class UnSupportedJwtException extends RuntimeException {

	public UnSupportedJwtException() {
	}

	public UnSupportedJwtException(String message) {
		super(message);
	}

	public UnSupportedJwtException(String message, Throwable cause) {
		super(message, cause);
	}

	public UnSupportedJwtException(Throwable cause) {
		super(cause);
	}

	public UnSupportedJwtException(String message, Throwable cause, boolean enableSuppression,
		boolean writableStackTrace) {
		super(message, cause, enableSuppression, writableStackTrace);
	}
}
