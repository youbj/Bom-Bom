package org.jeongkkili.bombom.qualify.service;

import org.jeongkkili.bombom.qualify.domain.QualifyNum;

public interface QualifyService {

	boolean verifyQualifyNumber(String qualifyNumber);

	QualifyNum getQualifyNum(String qualifyNumber);
}
