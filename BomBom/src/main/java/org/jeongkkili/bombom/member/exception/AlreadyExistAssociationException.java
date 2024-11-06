package org.jeongkkili.bombom.member.exception;

public class AlreadyExistAssociationException extends RuntimeException {

	public AlreadyExistAssociationException() {
	}

	public AlreadyExistAssociationException(String message) {
		super(message);
	}

	public AlreadyExistAssociationException(String message, Throwable cause) {
		super(message, cause);
	}

	public AlreadyExistAssociationException(Throwable cause) {
		super(cause);
	}

	protected AlreadyExistAssociationException(String message, Throwable cause, boolean enableSuppression,
		boolean writableStackTrace) {
		super(message, cause, enableSuppression, writableStackTrace);
	}
}
