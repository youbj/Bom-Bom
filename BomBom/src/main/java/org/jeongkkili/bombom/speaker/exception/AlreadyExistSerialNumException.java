package org.jeongkkili.bombom.speaker.exception;

import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.ResponseStatus;

@ResponseStatus(HttpStatus.CONFLICT)
public class AlreadyExistSerialNumException extends RuntimeException {

	public AlreadyExistSerialNumException() {
	}

	public AlreadyExistSerialNumException(String message) {
		super(message);
	}

	public AlreadyExistSerialNumException(String message, Throwable cause) {
		super(message, cause);
	}

	public AlreadyExistSerialNumException(Throwable cause) {
		super(cause);
	}

	protected AlreadyExistSerialNumException(String message, Throwable cause, boolean enableSuppression,
		boolean writableStackTrace) {
		super(message, cause, enableSuppression, writableStackTrace);
	}
}
