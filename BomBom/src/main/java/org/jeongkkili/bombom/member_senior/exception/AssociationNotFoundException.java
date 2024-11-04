package org.jeongkkili.bombom.member_senior.exception;

public class AssociationNotFoundException extends RuntimeException {

	public AssociationNotFoundException() {
	}

	public AssociationNotFoundException(String message) {
		super(message);
	}

	public AssociationNotFoundException(String message, Throwable cause) {
		super(message, cause);
	}

	public AssociationNotFoundException(Throwable cause) {
		super(cause);
	}

	protected AssociationNotFoundException(String message, Throwable cause, boolean enableSuppression,
		boolean writableStackTrace) {
		super(message, cause, enableSuppression, writableStackTrace);
	}
}
