package org.jeongkkili.bombom.speaker.repository;

import org.jeongkkili.bombom.speaker.domain.Speaker;
import org.springframework.data.jpa.repository.JpaRepository;

public interface SpeakerRepository extends JpaRepository<Speaker, Long> {

	Speaker findBySerialNum(String serialNum);
}
