package org.jeongkkili.bombom.core.jwt.exception;

import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.ResponseStatus;

@ResponseStatus(HttpStatus.UNAUTHORIZED)
public class ExpiredJwtException extends RuntimeException {

	public ExpiredJwtException() {
	}

	public ExpiredJwtException(String message) {
		super(message);
	}

	public ExpiredJwtException(String message, Throwable cause) {
		super(message, cause);
	}

	public ExpiredJwtException(Throwable cause) {
		super(cause);
	}

	public ExpiredJwtException(String message, Throwable cause, boolean enableSuppression,
		boolean writableStackTrace) {
		super(message, cause, enableSuppression, writableStackTrace);
	}
}