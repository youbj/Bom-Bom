package org.jeongkkili.bombom.schedule.exception;

import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.ResponseStatus;

@ResponseStatus(HttpStatus.NOT_FOUND)
public class ScheduleNotFoundException extends RuntimeException {

	public ScheduleNotFoundException() {
	}

	public ScheduleNotFoundException(String message) {
		super(message);
	}

	public ScheduleNotFoundException(String message, Throwable cause) {
		super(message, cause);
	}

	public ScheduleNotFoundException(Throwable cause) {
		super(cause);
	}

	protected ScheduleNotFoundException(String message, Throwable cause, boolean enableSuppression,
		boolean writableStackTrace) {
		super(message, cause, enableSuppression, writableStackTrace);
	}
}
