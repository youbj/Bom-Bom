package org.jeongkkili.bombom.qualify.service;

import org.jeongkkili.bombom.qualify.exception.QualifyNumMissingException;
import org.jeongkkili.bombom.qualify.repository.QualifyNumRepository;
import org.springframework.stereotype.Service;

import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;

@Service
@RequiredArgsConstructor
@Slf4j
public class QualifyServiceImpl implements QualifyService {

	private final QualifyNumRepository qualifyNumRepository;

	@Override
	public boolean verifyQualifyNumber(String qualifyNumber) {
		if(qualifyNumber == null || qualifyNumber.isEmpty()) throw new QualifyNumMissingException("Qualify number is empty");
		return qualifyNumRepository.findByQualifyNumber(qualifyNumber) != null;
	}
}
