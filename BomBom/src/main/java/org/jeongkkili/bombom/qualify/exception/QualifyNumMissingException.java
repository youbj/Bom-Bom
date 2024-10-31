package org.jeongkkili.bombom.qualify.exception;

public class QualifyNumMissingException extends RuntimeException {

	public QualifyNumMissingException() {
	}

	public QualifyNumMissingException(String message) {
		super(message);
	}

	public QualifyNumMissingException(String message, Throwable cause) {
		super(message, cause);
	}

	public QualifyNumMissingException(Throwable cause) {
		super(cause);
	}

	protected QualifyNumMissingException(String message, Throwable cause, boolean enableSuppression,
		boolean writableStackTrace) {
		super(message, cause, enableSuppression, writableStackTrace);
	}
}
