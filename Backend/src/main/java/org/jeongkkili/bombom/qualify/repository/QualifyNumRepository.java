package org.jeongkkili.bombom.qualify.repository;

import org.jeongkkili.bombom.qualify.domain.QualifyNum;
import org.springframework.data.jpa.repository.JpaRepository;

public interface QualifyNumRepository extends JpaRepository<QualifyNum, Long>  {

	QualifyNum findByQualifyNumber(String qualifyNum);
}
