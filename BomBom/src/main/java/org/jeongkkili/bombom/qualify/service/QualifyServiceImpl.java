package org.jeongkkili.bombom.qualify.service;

import org.jeongkkili.bombom.qualify.domain.QualifyNum;
import org.jeongkkili.bombom.qualify.exception.QualifyNumMissingException;
import org.jeongkkili.bombom.qualify.repository.QualifyNumRepository;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;

@Service
@RequiredArgsConstructor
@Transactional
@Slf4j
public class QualifyServiceImpl implements QualifyService {

	private final QualifyNumRepository qualifyNumRepository;

	@Override
	public boolean verifyQualifyNumber(String qualifyNumber) {
		if(qualifyNumber == null || qualifyNumber.isEmpty()) throw new QualifyNumMissingException("Qualify number is empty");
		QualifyNum qualifyNum = qualifyNumRepository.findByQualifyNumber(qualifyNumber);
		return qualifyNum != null && !qualifyNum.getInUse();
	}

	@Override
	public QualifyNum getQualifyNum(String qualifyNumber) {
		return qualifyNumRepository.findByQualifyNumber(qualifyNumber);
	}
}
