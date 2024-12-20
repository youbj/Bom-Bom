package org.jeongkkili.bombom.entry.exception;

import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.ResponseStatus;

@ResponseStatus(HttpStatus.NOT_FOUND)
public class LatestExitHistoryNotFoundException extends RuntimeException {

	public LatestExitHistoryNotFoundException() {
	}

	public LatestExitHistoryNotFoundException(String message) {
		super(message);
	}

	public LatestExitHistoryNotFoundException(String message, Throwable cause) {
		super(message, cause);
	}

	public LatestExitHistoryNotFoundException(Throwable cause) {
		super(cause);
	}

	protected LatestExitHistoryNotFoundException(String message, Throwable cause, boolean enableSuppression,
		boolean writableStackTrace) {
		super(message, cause, enableSuppression, writableStackTrace);
	}
}
