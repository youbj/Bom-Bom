package org.jeongkkili.bombom.schedule.exception;

import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.ResponseStatus;

@ResponseStatus(HttpStatus.BAD_REQUEST)
public class InvalidDateRangeException extends RuntimeException {

	public InvalidDateRangeException() {
	}

	public InvalidDateRangeException(String message) {
		super(message);
	}

	public InvalidDateRangeException(String message, Throwable cause) {
		super(message, cause);
	}

	public InvalidDateRangeException(Throwable cause) {
		super(cause);
	}

	protected InvalidDateRangeException(String message, Throwable cause, boolean enableSuppression,
		boolean writableStackTrace) {
		super(message, cause, enableSuppression, writableStackTrace);
	}
}
